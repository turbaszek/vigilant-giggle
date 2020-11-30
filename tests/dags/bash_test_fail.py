import datetime
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {'wait_for_downstream': True, 'provide_context': False}

with DAG(
    "bash_test_fail_shrubbery",
    start_date=datetime.datetime.now() - datetime.timedelta(days=1),
    schedule_interval='*/2 * * * *',
    default_args=default_args,
    max_active_runs=1
) as dag:
    for target_date in range(0, 10):
        bash_cmd_j001 = BashOperator(
            task_id='bash_cmd_j001_' + str(target_date),
            bash_command='echo "bash_cmd_001"',
            trigger_rule='all_success', dag=dag)
        bash_cmd_j002 = BashOperator(
            task_id='bash_cmd_j002_' + str(target_date),
            bash_command='echo "bash_cmd_002"',
            trigger_rule='all_success', dag=dag)
        bash_cmd_j003 = BashOperator(
            task_id='bash_cmd_j003_' + str(target_date),
            bash_command='echo "bash_cmd_003"',
            trigger_rule='all_success', dag=dag)
        bash_cmd_j004 = BashOperator(
            task_id='bash_cmd_j004_' + str(target_date),
            bash_command='echo "bash_cmd_004"',
            trigger_rule='all_success', dag=dag)
        bash_cmd_j005 = BashOperator(
            task_id='bash_cmd_j005_' + str(target_date),
            bash_command='echo "bash_cmd_005"',
            trigger_rule='all_success', dag=dag)
        if (target_date % 2) == 0:
            bash_cmd_j001 >> bash_cmd_j002 >> bash_cmd_j003 >> bash_cmd_j004 >> bash_cmd_j005
        else:
            bash_cmd_j001 >> bash_cmd_j005 >> bash_cmd_j004 >> bash_cmd_j003 >> bash_cmd_j002
