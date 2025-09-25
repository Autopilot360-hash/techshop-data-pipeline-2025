from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'techshop-data-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 24),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'techshop_simple_pipeline',
    default_args=default_args,
    description='Simple TechShop pipeline',
    schedule_interval='@daily',
    catchup=False,
    tags=['techshop', 'simple']
)

# Test task
test_connection = BashOperator(
    task_id='test_connection',
    bash_command='echo "Testing TechShop pipeline connection"',
    dag=dag
)

# Simple data check
def check_data_exists():
    from google.cloud import bigquery
    client = bigquery.Client(project='techshop-data-pipeline-2025')
    
    query = """
    SELECT COUNT(*) as count
    FROM `techshop-data-pipeline-2025.raw_data.sales_data`
    LIMIT 1
    """
    
    try:
        result = client.query(query).result()
        for row in result:
            print(f"Data check: {row.count} rows found")
        return True
    except Exception as e:
        print(f"Data check failed: {e}")
        return False

data_check = PythonOperator(
    task_id='data_check',
    python_callable=check_data_exists,
    dag=dag
)

test_connection >> data_check
