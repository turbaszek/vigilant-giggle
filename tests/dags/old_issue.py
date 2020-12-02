from airflow import models
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

from airflow.sensors.external_task_sensor import ExternalTaskSensor

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2018, 10, 31),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}
dag_name = 'master_dag'

with models.DAG(
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

with models.DAG(
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
