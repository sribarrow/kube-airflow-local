from datetime import datetime, timedelta
import json

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
import requests
import pandas as pd

def get_data(**kwargs):
    url = 'https://raw.githubusercontent.com/airscholar/ApacheFlink-SalesAnalytics/main/output/new-output.csv'
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(url, header=None, names=['Category', 'Price', "Qty"])
        # df to string for xcom
        json_data = df.to_json(orient='records')
        kwargs['ti'].xcom_push(key='raw_to_json_data', value=json_data)
    else:
        raise Exception(f'{response.status_code} - Unable to read file.')

def view_data(**kwargs):
    json_data = kwargs['ti'].xcom_pull(key='raw_to_json_data', task_id='get_data')
    print(json_data)
    if json_data:
        data = json.loads(json_data)
    else:
        raise ValueError('No data.')
    # calculate sales
    df = pd.DataFrame(data)
    df['Total'] = df["Price"] * df["Qty"] 
    df = df.groupby(by='Category', as_index=False).agg({'Qty':'sum', 'Total':'sum'})
    # sort by total
    df = df.sort_values(by='Total', ascending=False)
    json_data = df.to_json(orient='records')
    kwargs['ti'].xcom_push(key='transformed_json_data', value=json_data)

default_args = {
    'owner': 'sri',
    'start_date': datetime(year=2024, month=3, day=20),
    'catchup': False
}

dag = DAG(
    dag_id = 'read_and_preview_csv',
    default_args = default_args,
    schedule = timedelta(days=1)
)

start = EmptyOperator(task_id='start')
end = EmptyOperator(task_id='end')

get_data = PythonOperator(
    task_id = 'get_data',
    python_callable=get_data,
    dag = dag
)

view_data = PythonOperator(
    task_id = 'view_data',
    python_callable=view_data,
    dag = dag
)

start >> get_data >> view_data >> end