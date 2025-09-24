# scripts/fix_missing_tables.py - Diagnostique et corrige les tables manquantes
from google.cloud import bigquery
import os

def check_and_fix_tables():
    """Vérifie quelles tables existent et recrée les manquantes"""
    
    print("🔍 Checking existing tables and fixing missing ones...")
    
    project_id = "techshop-data-pipeline-2025"
    dataset_id = "raw_data"
    
    # Client BigQuery
    try:
        client = bigquery.Client(project=project_id)
        print("✅ BigQuery client initialized")
    except Exception as e:
        print(f"❌ Error initializing BigQuery client: {e}")
        return False
    
    # Tables attendues
    expected_tables = {
        'customers': 'data/customers_2025.csv',
        'products': 'data/products_2025.csv',
        'orders': 'data/orders_2025.csv', 
        'order_items': 'data/order_items_2025.csv',
        'marketing_campaigns': 'data/marketing_data_2025.csv'
    }
    
    # Vérifier quelles tables existent
    existing_tables = []
    missing_tables = []
    
    for table_name in expected_tables.keys():
        try:
            table_ref = client.dataset(dataset_id).table(table_name)
            table = client.get_table(table_ref)
            existing_tables.append(table_name)
            print(f"✅ {table_name}: {table.num_rows:,} rows")
        except Exception:
            missing_tables.append(table_name)
            print(f"❌ {table_name}: MISSING")
    
    if not missing_tables:
        print(f"\n🎉 All tables exist! No action needed.")
        return True
    
    print(f"\n🔧 Need to create {len(missing_tables)} missing tables:")
    for table in missing_tables:
        print(f"  - {table}")
    
    # Générer les commandes bq pour créer les tables manquantes
    print(f"\n📋 Run these commands to create missing tables:")
    print("=" * 60)
    
    if 'products' in missing_tables:
        print("""
bq mk --table \\
  --clustering_fields=category,brand \\
  --time_partitioning_field=launch_date \\
  --time_partitioning_type=DAY \\
  techshop-data-pipeline-2025:raw_data.products \\
  product_id:STRING,sku:STRING,product_name:STRING,category:STRING,subcategory:STRING,brand:STRING,price:FLOAT64,cost:FLOAT64,stock_quantity:INTEGER,avg_rating:FLOAT64,num_reviews:INTEGER,launch_date:DATE,weight:FLOAT64,is_eco_friendly:BOOLEAN,is_ai_enabled:BOOLEAN,is_bestseller:BOOLEAN,created_at:TIMESTAMP,updated_at:TIMESTAMP
""")
    
    if 'orders' in missing_tables:
        print("""
bq mk --table \\
  --clustering_fields=customer_id,order_status \\
  --time_partitioning_field=order_date \\
  --time_partitioning_type=DAY \\
  techshop-data-pipeline-2025:raw_data.orders \\
  order_id:STRING,customer_id:STRING,order_date:DATE,total_amount:FLOAT64,shipping_cost:FLOAT64,payment_method:STRING,order_status:STRING,sales_channel:STRING,num_items:INTEGER,shipped_date:DATE,delivered_date:DATE,created_at:TIMESTAMP
""")
    
    if 'marketing_campaigns' in missing_tables:
        print("""
bq mk --table \\
  --clustering_fields=channel,campaign_type \\
  --time_partitioning_field=start_date \\
  --time_partitioning_type=DAY \\
  techshop-data-pipeline-2025:raw_data.marketing_campaigns \\
  campaign_id:STRING,campaign_name:STRING,campaign_type:STRING,channel:STRING,objective:STRING,start_date:DATE,end_date:DATE,duration_days:INTEGER,daily_budget:FLOAT64,total_budget:FLOAT64,total_impressions:INTEGER,total_clicks:INTEGER,total_conversions:INTEGER,total_revenue:FLOAT64,avg_cpc:FLOAT64,cost_per_conversion:FLOAT64,conversion_rate:FLOAT64,roas:FLOAT64,status:STRING,uses_ai_optimization:BOOLEAN,is_sustainable_focused:BOOLEAN,targets_gen_z:BOOLEAN,created_at:TIMESTAMP
""")
    
    print("=" * 60)
    print(f"\n🚀 After running the commands above, re-run:")
    print(f"python scripts/upload_to_bigquery_simple.py")
    
    return len(missing_tables) == 0

def upload_missing_data():
    """Essaie d'uploader les données pour les tables qui ont 0 rows"""
    
    print("\n🔄 Attempting to upload data to tables with 0 rows...")
    
    project_id = "techshop-data-pipeline-2025"
    dataset_id = "raw_data"
    
    client = bigquery.Client(project=project_id)
    
    # Tables à vérifier pour re-upload
    tables_to_check = {
        'products': 'data/products_2025.csv',
        'orders': 'data/orders_2025.csv',
        'marketing_campaigns': 'data/marketing_data_2025.csv'
    }
    
    for table_name, csv_file in tables_to_check.items():
        try:
            table_ref = client.dataset(dataset_id).table(table_name)
            table = client.get_table(table_ref)
            
            if table.num_rows == 0:
                print(f"\n📊 Re-uploading {table_name}...")
                
                if not os.path.exists(csv_file):
                    print(f"  ❌ File not found: {csv_file}")
                    continue
                
                # Configuration d'upload
                job_config = bigquery.LoadJobConfig()
                job_config.source_format = bigquery.SourceFormat.CSV
                job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
                job_config.autodetect = True
                job_config.skip_leading_rows = 1
                
                # Upload
                with open(csv_file, 'rb') as source_file:
                    load_job = client.load_table_from_file(
                        source_file, 
                        table_ref, 
                        job_config=job_config
                    )
                
                # Attendre le résultat
                load_job.result()
                
                # Vérifier
                table = client.get_table(table_ref)
                print(f"  ✅ Uploaded {table.num_rows:,} rows to {table_name}")
            
        except Exception as e:
            print(f"  ❌ Error with {table_name}: {e}")

if __name__ == "__main__":
    # D'abord diagnostiquer
    check_and_fix_tables()
    
    # Puis essayer de re-uploader
    upload_missing_data()
    
    # Statistiques finales
    print(f"\n📊 Final Check:")
    client = bigquery.Client(project="techshop-data-pipeline-2025")
    
    tables = ['customers', 'products', 'orders', 'order_items', 'marketing_campaigns']
    total_rows = 0
    
    for table_name in tables:
        try:
            table_ref = client.dataset("raw_data").table(table_name)
            table = client.get_table(table_ref)
            rows = table.num_rows
            total_rows += rows
            status = "✅" if rows > 0 else "❌"
            print(f"  {status} {table_name}: {rows:,} rows")
        except:
            print(f"  ❌ {table_name}: NOT FOUND")
    
    print(f"\n🎯 Total rows: {total_rows:,}")
