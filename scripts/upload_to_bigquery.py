# scripts/upload_to_bigquery.py
from google.cloud import bigquery
import pandas as pd
from datetime import datetime
import os

def upload_to_bigquery():
    """Upload toutes les données générées vers BigQuery"""
    
    print("🚀 Uploading data to BigQuery...")
    
    # Configuration
    project_id = "techshop-data-pipeline-2025"
    dataset_id = "raw_data"
    
    # Client BigQuery
    try:
        client = bigquery.Client(project=project_id)
        print("✅ BigQuery client initialized")
    except Exception as e:
        print(f"❌ Error initializing BigQuery client: {e}")
        return False
    
    # Tables à uploader
    tables_config = {
        'customers': {
            'file': 'data/customers_2025.csv',
            'table_id': 'customers',
            'partition_field': 'created_at'
        },
        'products': {
            'file': 'data/products_2025.csv', 
            'table_id': 'products',
            'partition_field': 'launch_date'
        },
        'orders': {
            'file': 'data/orders_2025.csv',
            'table_id': 'orders', 
            'partition_field': 'order_date'
        },
        'order_items': {
            'file': 'data/order_items_2025.csv',
            'table_id': 'order_items',
            'partition_field': None
        },
        'marketing_campaigns': {
            'file': 'data/marketing_data_2025.csv',
            'table_id': 'marketing_campaigns',
            'partition_field': 'start_date'
        }
    }
    
    success_count = 0
    
    for table_name, config in tables_config.items():
        print(f"\n📊 Processing {table_name}...")
        
        # Vérifier que le fichier existe
        if not os.path.exists(config['file']):
            print(f"❌ File not found: {config['file']}")
            continue
        
        # Charger les données
        try:
            df = pd.read_csv(config['file'])
            print(f"  Loaded {len(df)} rows from {config['file']}")
        except Exception as e:
            print(f"❌ Error loading file {config['file']}: {e}")
            continue
        
        # Configuration de la table
        table_ref = client.dataset(dataset_id).table(config['table_id'])
        
        # Configuration du job
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.autodetect = True
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        
        # Partition si spécifiée
        if config['partition_field']:
            job_config.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field=config['partition_field']
            )
        
        # Upload
        try:
            with open(config['file'], 'rb') as source_file:
                load_job = client.load_table_from_file(
                    source_file, 
                    table_ref, 
                    job_config=job_config
                )
            
            # Attendre la fin du job
            load_job.result()
            
            # Vérifier le résultat
            table = client.get_table(table_ref)
            print(f"  ✅ Successfully loaded {table.num_rows} rows to {table_name}")
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ Error loading {table_name}: {e}")
    
    print(f"\n🎉 Upload completed! {success_count}/{len(tables_config)} tables uploaded successfully.")
    
    # Statistiques finales
    if success_count > 0:
        print(f"\n📊 Final Statistics:")
        for table_name in tables_config.keys():
            try:
                table_ref = client.dataset(dataset_id).table(tables_config[table_name]['table_id'])
                table = client.get_table(table_ref)
                print(f"  {table_name}: {table.num_rows:,} rows")
            except:
                print(f"  {table_name}: Not found")
    
    return success_count > 0

if __name__ == "__main__":
    upload_to_bigquery()
