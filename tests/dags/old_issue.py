from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from time import sleep

from airflow import DAG
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.dates import days_ago

from airflow.sensors.external_task_sensor import ExternalTaskSensor

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2018, 10, 31),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}
dag_name = 'master_dag'

with DAG(
    dag_name,
    default_args=default_args,
    schedule_interval='*/3 * * * *',
    catchup=False,
    max_active_runs=5,
    tags=['start'],
    is_paused_upon_creation=False,
) as dag:
    start = DummyOperator(
        task_id=f'start'
    )

with DAG(
    'target_dag',
    default_args=default_args,
    schedule_interval='*/3 * * * *',
    catchup=False,
    max_active_runs=5,
    tags=['start'],
    is_paused_upon_creation=False,
) as dag2:
    wait = ExternalTaskSensor(
        task_id='wait-task',
        external_dag_id=dag_name,
        external_task_id='start',
        poke_interval=60 * 5,
        mode='reschedule'
    )


class DummySensor(BaseSensorOperator):
    def __init__(self, t=0, **kwargs):
        self.t = t
        super().__init__(**kwargs)

    def poke(self, context):
        sleep(self.t)
        return False


with DAG(
    "other_dag",
    start_date=days_ago(1),
    schedule_interval="*/2 * * * *",
    catchup=False
) as dag3:
    DummySensor(
        task_id='wait-task',
        poke_interval=60 * 5,
        mode='reschedule'
    )
