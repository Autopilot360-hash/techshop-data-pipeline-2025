#!/bin/bash
echo "🔄 Installation et configuration Airflow pour TechShop 2025"

# Chemin CORRECT vers votre environnement virtuel
VENV_PATH="/opt/app/bigquery-projects/venv3"

echo "📂 Utilisation de l'environnement virtuel : $VENV_PATH"

# Vérifier que le chemin existe
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Environnement virtuel non trouvé à : $VENV_PATH"
    echo "Recherche automatique..."
    find /opt -name "venv3" -type d 2>/dev/null | head -5
    exit 1
fi

# Configuration des variables
export AIRFLOW_HOME=~/airflow
export AIRFLOW_VERSION=2.8.0

# Activer l'environnement virtuel
echo "🐍 Activation de l'environnement virtuel..."
source $VENV_PATH/bin/activate

# Installer Airflow
echo "📦 Installation d'Airflow..."
pip install "apache-airflow==${AIRFLOW_VERSION}"
pip install apache-airflow-providers-google

# Initialiser la base de données
echo "🗄️ Initialisation de la base de données..."
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
echo "🚀 Pour démarrer Airflow :"
echo "   bash start_airflow_fixed.sh"
