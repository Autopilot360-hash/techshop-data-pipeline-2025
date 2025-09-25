#!/bin/bash
echo "🚀 Démarrage d'Airflow TechShop 2025"

export AIRFLOW_HOME=~/airflow
source ../venv3/bin/activate

echo "🌐 Démarrage du webserver Airflow..."
echo "📊 Interface web disponible sur : http://localhost:8080"
echo "👤 Login: admin / Mot de passe: admin123"
echo ""
echo "⚠️  Pour démarrer le scheduler, ouvrez un nouveau terminal et exécutez :"
echo "   cd /opt/app/bigquery-projects/techshop-data-pipeline-2025/airflow_setup"
echo "   source ../venv3/bin/activate"
echo "   export AIRFLOW_HOME=~/airflow"
echo "   airflow scheduler"
echo ""

# Lancer le webserver
airflow webserver --port 8080
