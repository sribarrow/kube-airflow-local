from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'sri',
    'start_date': datetime(year:2024, month:3, day:20),
    'catchup': False
}

dag = DAG(
    dag_id = 'my-first-dag',
    default_args = default_args,
    schedule = timedelta(days=1)
)
start = EmptyOperator(task_id='start')
end = EmptyOperator(task_id='end')

t2 = BashOperator(
    task_id = 'example',
    bash_command= 'echo "Hello from Kubernetes with airflow"',
    dag = dag
)

start >> t2 >> end