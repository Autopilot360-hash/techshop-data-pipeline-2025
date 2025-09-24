#!/bin/bash
# setup.sh - Configuration initiale du projet TechShop 2025

echo "🚀 Setting up TechShop Data Pipeline 2025"
echo "========================================"

# Créer les dossiers nécessaires
echo "📁 Creating project structure..."
mkdir -p data
mkdir -p scripts  
mkdir -p sql
mkdir -p dbt_project/models/staging
mkdir -p dbt_project/models/marts
mkdir -p dbt_project/macros
mkdir -p airflow/dags
mkdir -p config

# Installer l'environnement virtuel Python
echo "🐍 Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Configuration BigQuery
echo "☁️  Setting up BigQuery..."
if [ ! -f "$HOME/.config/gcloud/application_default_credentials.json" ]; then
    echo "⚠️  Please run 'gcloud auth application-default login' to setup BigQuery access"
    echo "⚠️  Also run 'gcloud config set project techshop-data-pipeline-2025'"
else
    echo "✅ Google Cloud credentials found"
fi

# Créer les datasets BigQuery (si gcloud est configuré)
echo "📊 Creating BigQuery datasets..."
if command -v bq &> /dev/null; then
    bq query --use_legacy_sql=false < sql/create_datasets.sql 2>/dev/null || echo "  ⚠️  Run this manually: bq query --use_legacy_sql=false < sql/create_datasets.sql"
    bq query --use_legacy_sql=false < sql/create_tables.sql 2>/dev/null || echo "  ⚠️  Run this manually: bq query --use_legacy_sql=false < sql/create_tables.sql"
else
    echo "  ⚠️  bq command not found. Install Google Cloud CLI first."
fi

echo ""
echo "✅ Setup completed!"
echo ""
echo "🎯 Next steps:"
echo "1. Run: source venv/bin/activate"
echo "2. Configure Google Cloud: gcloud auth application-default login" 
echo "3. Set project: gcloud config set project techshop-data-pipeline-2025"
echo "4. Generate data: python scripts/generate_customers_2025.py" 
echo "5. Upload to BigQuery: python scripts/upload_to_bigquery.py"
echo "6. Run dbt: cd dbt_project && dbt run"
echo ""
echo "🎉 Happy analyzing!"
