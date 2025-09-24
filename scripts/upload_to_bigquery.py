# scripts/upload_to_bigquery.py - VERSION CORRIGÉE
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
            'partition_field': 'created_at',
            'cluster_fields': ['customer_segment', 'country']
        },
        'products': {
            'file': 'data/products_2025.csv', 
            'table_id': 'products',
            'partition_field': 'launch_date',
            'cluster_fields': ['category', 'brand']
        },
        'orders': {
            'file': 'data/orders_2025.csv',
            'table_id': 'orders', 
            'partition_field': 'order_date',
            'cluster_fields': ['customer_id', 'order_status']
        },
        'order_items': {
            'file': 'data/order_items_2025.csv',
            'table_id': 'order_items',
            'partition_field': None,
            'cluster_fields': ['order_id', 'product_id']
        },
        'marketing_campaigns': {
            'file': 'data/marketing_data_2025.csv',
            'table_id': 'marketing_campaigns',
            'partition_field': 'start_date',
            'cluster_fields': ['channel', 'campaign_type']
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
        
        # Référence de la table
        table_ref = client.dataset(dataset_id).table(config['table_id'])
        
        try:
            # ÉTAPE 1 : Supprimer la table existante si elle existe
            try:
                client.delete_table(table_ref)
                print(f"  🗑️  Deleted existing table {config['table_id']}")
            except Exception:
                print(f"  ℹ️  Table {config['table_id']} doesn't exist yet")
            
            # ÉTAPE 2 : Recréer la table avec la bonne structure
            print(f"  🔧 Creating table with partitioning and clustering...")
            
            # Définir les schémas selon la table
            if table_name == 'customers':
                schema = [
                    bigquery.SchemaField("customer_id", "STRING"),
                    bigquery.SchemaField("first_name", "STRING"),
                    bigquery.SchemaField("last_name", "STRING"),
                    bigquery.SchemaField("email", "STRING"),
                    bigquery.SchemaField("country", "STRING"),
                    bigquery.SchemaField("city", "STRING"),
                    bigquery.SchemaField("created_at", "DATE"),
                    bigquery.SchemaField("customer_segment", "STRING"),
                    bigquery.SchemaField("lifetime_value", "FLOAT64"),
                    bigquery.SchemaField("avg_order_value", "FLOAT64"),
                    bigquery.SchemaField("order_frequency", "FLOAT64"),
                    bigquery.SchemaField("preferred_categories", "STRING"),
                    bigquery.SchemaField("is_vip", "BOOLEAN"),
                    bigquery.SchemaField("newsletter_subscriber", "BOOLEAN"),
                    bigquery.SchemaField("mobile_app_user", "BOOLEAN"),
                    bigquery.SchemaField("last_active_date", "DATE")
                ]
            elif table_name == 'products':
                schema = [
                    bigquery.SchemaField("product_id", "STRING"),
                    bigquery.SchemaField("sku", "STRING"),
                    bigquery.SchemaField("product_name", "STRING"),
                    bigquery.SchemaField("category", "STRING"),
                    bigquery.SchemaField("subcategory", "STRING"),
                    bigquery.SchemaField("brand", "STRING"),
                    bigquery.SchemaField("price", "FLOAT64"),
                    bigquery.SchemaField("cost", "FLOAT64"),
                    bigquery.SchemaField("stock_quantity", "INTEGER"),
                    bigquery.SchemaField("avg_rating", "FLOAT64"),
                    bigquery.SchemaField("num_reviews", "INTEGER"),
                    bigquery.SchemaField("launch_date", "DATE"),
                    bigquery.SchemaField("weight", "FLOAT64"),
                    bigquery.SchemaField("is_eco_friendly", "BOOLEAN"),
                    bigquery.SchemaField("is_ai_enabled", "BOOLEAN"),
                    bigquery.SchemaField("is_bestseller", "BOOLEAN"),
                    bigquery.SchemaField("created_at", "TIMESTAMP"),
                    bigquery.SchemaField("updated_at", "TIMESTAMP")
                ]
            elif table_name == 'orders':
                schema = [
                    bigquery.SchemaField("order_id", "STRING"),
                    bigquery.SchemaField("customer_id", "STRING"),
                    bigquery.SchemaField("order_date", "DATE"),
                    bigquery.SchemaField("total_amount", "FLOAT64"),
                    bigquery.SchemaField("shipping_cost", "FLOAT64"),
                    bigquery.SchemaField("payment_method", "STRING"),
                    bigquery.SchemaField("order_status", "STRING"),
                    bigquery.SchemaField("sales_channel", "STRING"),
                    bigquery.SchemaField("num_items", "INTEGER"),
                    bigquery.SchemaField("shipped_date", "DATE"),
                    bigquery.SchemaField("delivered_date", "DATE"),
                    bigquery.SchemaField("created_at", "TIMESTAMP")
                ]
            elif table_name == 'order_items':
                schema = [
                    bigquery.SchemaField("order_id", "STRING"),
                    bigquery.SchemaField("product_id", "STRING"),
                    bigquery.SchemaField("product_name", "STRING"),
                    bigquery.SchemaField("category", "STRING"),
                    bigquery.SchemaField("quantity", "INTEGER"),
                    bigquery.SchemaField("unit_price", "FLOAT64"),
                    bigquery.SchemaField("total_price", "FLOAT64")
                ]
            elif table_name == 'marketing_campaigns':
                schema = [
                    bigquery.SchemaField("campaign_id", "STRING"),
                    bigquery.SchemaField("campaign_name", "STRING"),
                    bigquery.SchemaField("campaign_type", "STRING"),
                    bigquery.SchemaField("channel", "STRING"),
                    bigquery.SchemaField("objective", "STRING"),
                    bigquery.SchemaField("start_date", "DATE"),
                    bigquery.SchemaField("end_date", "DATE"),
                    bigquery.SchemaField("duration_days", "INTEGER"),
                    bigquery.SchemaField("daily_budget", "FLOAT64"),
                    bigquery.SchemaField("total_budget", "FLOAT64"),
                    bigquery.SchemaField("total_impressions", "INTEGER"),
                    bigquery.SchemaField("total_clicks", "INTEGER"),
                    bigquery.SchemaField("total_conversions", "INTEGER"),
                    bigquery.SchemaField("total_revenue", "FLOAT64"),
                    bigquery.SchemaField("avg_cpc", "FLOAT64"),
                    bigquery.SchemaField("cost_per_conversion", "FLOAT64"),
                    bigquery.SchemaField("conversion_rate", "FLOAT64"),
                    bigquery.SchemaField("roas", "FLOAT64"),
                    bigquery.SchemaField("status", "STRING"),
                    bigquery.SchemaField("uses_ai_optimization", "BOOLEAN"),
                    bigquery.SchemaField("is_sustainable_focused", "BOOLEAN"),
                    bigquery.SchemaField("targets_gen_z", "BOOLEAN"),
                    bigquery.SchemaField("created_at", "TIMESTAMP")
                ]
            
            # Créer la table avec le bon schéma
            table = bigquery.Table(table_ref, schema=schema)
            
            # Ajouter partitioning si spécifié
            if config['partition_field']:
                table.time_partitioning = bigquery.TimePartitioning(
                    type_=bigquery.TimePartitioningType.DAY,
                    field=config['partition_field']
                )
            
            # Ajouter clustering si spécifié
            if config['cluster_fields']:
                table.clustering_fields = config['cluster_fields']
            
            # Créer la table
            table = client.create_table(table)
            print(f"  ✅ Created table {config['table_id']} with partitioning and clustering")
            
            # ÉTAPE 3 : Uploader les données
            job_config = bigquery.LoadJobConfig()
            job_config.source_format = bigquery.SourceFormat.CSV
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
            job_config.schema = schema  # Utiliser le schéma défini
            job_config.skip_leading_rows = 1  # Ignorer l'en-tête CSV
            
            # Upload
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
            print(f"  ❌ Error processing {table_name}: {e}")
    
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
                print(f"  {table_name}: Error reading table info")
    
    return success_count > 0

if __name__ == "__main__":
    upload_to_bigquery()
