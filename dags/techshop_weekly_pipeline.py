from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'techshop-data-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 24),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'techshop_weekly_reports',
    default_args=default_args,
    description='Weekly TechShop business reports',
    schedule_interval='0 8 * * 1',  # Monday at 8 AM
    catchup=False,
    tags=['techshop', 'weekly', 'reports']
)

# Weekly cohort analysis
weekly_cohorts = BigQueryInsertJobOperator(
    task_id='generate_weekly_cohorts',
    configuration={
        'query': {
            'query': '''
            CREATE OR REPLACE TABLE `techshop-data-pipeline-2025.analytics.weekly_cohorts` AS
            WITH first_orders AS (
              SELECT 
                customer_id,
                MIN(DATE_TRUNC(date, WEEK)) as cohort_week
              FROM `techshop-data-pipeline-2025.staging.processed_sales`
              GROUP BY customer_id
            ),
            customer_activity AS (
              SELECT 
                s.customer_id,
                fo.cohort_week,
                DATE_TRUNC(s.date, WEEK) as activity_week,
                SUM(s.total_amount) as weekly_revenue
              FROM `techshop-data-pipeline-2025.staging.processed_sales` s
              JOIN first_orders fo ON s.customer_id = fo.customer_id
              WHERE s.date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 WEEK)
              GROUP BY 1,2,3
            )
            SELECT 
              cohort_week,
              activity_week,
              COUNT(DISTINCT customer_id) as active_customers,
              SUM(weekly_revenue) as cohort_revenue,
              ROUND(AVG(weekly_revenue), 2) as avg_customer_revenue
            FROM customer_activity
            GROUP BY 1,2
            ORDER BY cohort_week, activity_week
            ''',
            'useLegacySql': False
        }
    },
    dag=dag
)
