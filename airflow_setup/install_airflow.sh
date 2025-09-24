#!/bin/bash
echo "🔄 Installation et configuration Airflow pour TechShop 2025"

# Configuration des variables
export AIRFLOW_HOME=~/airflow
export AIRFLOW_VERSION=2.8.0
export PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Activer l'environnement virtuel
source ../venv3/bin/activate

# Installer Airflow
echo "📦 Installation d'Airflow..."
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
pip install apache-airflow-providers-google

# Initialiser la base de données
echo "🗄️ Initialisation de la base de données Airflow..."
airflow db init

# Créer l'utilisateur admin
echo "👤 Création de l'utilisateur admin..."
airflow users create \
    --username admin \
    --firstname TechShop \
    --lastname Admin \
    --role Admin \
    --email admin@techshop.com \
    --password admin123

# Créer le dossier des DAGs
mkdir -p ~/airflow/dags

echo "✅ Installation terminée !"
echo "🎯 Prochaines étapes :"
echo "1. Copier les DAGs : cp ~/airflow/dags/"
echo "2. Lancer : bash start_airflow.sh"
