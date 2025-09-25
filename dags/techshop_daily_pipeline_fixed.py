from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator, BigQueryInsertJobOperator
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
    'techshop_daily_pipeline_fixed',
    default_args=default_args,
    description='TechShop daily data pipeline',
    schedule_interval='0 6 * * *',
    catchup=False,
    tags=['techshop', 'daily', 'production']
)

PROJECT_ID = 'techshop-data-pipeline-2025'

# Morning startup
morning_check = BashOperator(
    task_id='morning_startup_check',
    bash_command='echo "Starting TechShop pipeline at $(date)"',
    dag=dag
)

# Data availability check
check_data = BigQueryCheckOperator(
    task_id='check_raw_data',
    sql=f"""
    SELECT COUNT(*) as count
    FROM `{PROJECT_ID}.raw_data.sales_data`
    WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    """,
    use_legacy_sql=False,
    dag=dag
)

def create_daily_metrics():
    from google.cloud import bigquery
    client = bigquery.Client(project=PROJECT_ID)
    
    query = f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.analytics.daily_metrics` AS
    SELECT 
        CURRENT_DATE() as report_date,
        COUNT(*) as total_orders,
        SUM(total_amount) as total_revenue,
        COUNT(DISTINCT customer_id) as unique_customers,
        AVG(total_amount) as avg_order_value
    FROM `{PROJECT_ID}.raw_data.sales_data`
    WHERE date = CURRENT_DATE()
    """
    
    job = client.query(query)
    job.result()
    print("Daily metrics updated successfully")

update_metrics = PythonOperator(
    task_id='update_daily_metrics',
    python_callable=create_daily_metrics,
    dag=dag
)

completion_notification = BashOperator(
    task_id='completion_notification',
    bash_command='echo "TechShop pipeline completed at $(date)"',
    dag=dag
)

# Task flow
morning_check >> check_data >> update_metrics >> completion_notification
