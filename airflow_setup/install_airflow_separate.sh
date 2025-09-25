#!/bin/bash
# airflow_setup/install_airflow_separate.sh
echo "🔄 Installation Airflow dans un environnement séparé"

# Aller dans le dossier principal
cd /opt/app/bigquery-projects/techshop-data-pipeline-2025

# Créer un environnement virtuel séparé pour Airflow
echo "🐍 Création d'un environnement virtuel dédié à Airflow..."
python -m venv venv_airflow

# Activer le nouvel environnement
echo "📂 Activation de l'environnement Airflow..."
source venv_airflow/bin/activate

# Configuration Airflow
export AIRFLOW_HOME=~/airflow
export AIRFLOW_VERSION=2.8.0
export PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Installation propre
echo "📦 Installation d'Airflow ${AIRFLOW_VERSION}..."
pip install --upgrade pip
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
pip install apache-airflow-providers-google

# Vérifier l'installation
echo "🔍 Vérification de l'installation..."
which airflow
airflow version

# Initialisation
echo "🗄️ Initialisation de la base de données..."
airflow db init

# Créer utilisateur admin
echo "👤 Création de l'utilisateur admin..."
airflow users create \
    --username admin \
    --firstname TechShop \
    --lastname Admin \
    --role Admin \
    --email admin@techshop.com \
    --password admin123

# Créer dossier DAGs
mkdir -p ~/airflow/dags

echo "✅ Installation terminée !"
echo "🎯 Pour démarrer Airflow, utilisez :"
echo "   bash airflow_setup/start_airflow_separate.sh"
