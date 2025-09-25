from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG(
    'techshop_test',
    description='Test DAG TechShop',
    schedule_interval='@daily',
    start_date=datetime(2025, 9, 24),
    catchup=False
)

test_task = BashOperator(
    task_id='test_task',
    bash_command='echo "TechShop Pipeline is working!"',
    dag=dag
)
