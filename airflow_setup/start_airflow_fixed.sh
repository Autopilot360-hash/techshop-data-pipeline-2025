#!/bin/bash
echo "🚀 Démarrage d'Airflow TechShop 2025"

# Chemin CORRECT vers l'environnement virtuel
VENV_PATH="/opt/app/bigquery-projects/venv3"

echo "📂 Utilisation de l'environnement virtuel : $VENV_PATH"

# Configuration
export AIRFLOW_HOME=~/airflow
source $VENV_PATH/bin/activate

# Vérifier qu'Airflow est installé
if ! command -v airflow &> /dev/null; then
    echo "❌ Airflow non installé. Exécutez d'abord :"
    echo "   bash install_airflow_fixed.sh"
    exit 1
fi

echo "🌐 Démarrage du webserver Airflow..."
echo "📊 Interface web : http://localhost:8080"
echo "👤 Login: admin / Mot de passe: admin123"
echo ""
echo "⚠️  Pour le scheduler, ouvrez un nouveau terminal :"
echo "   cd $(pwd)"
echo "   source $VENV_PATH/bin/activate"
echo "   export AIRFLOW_HOME=~/airflow"  
echo "   airflow scheduler"
echo ""

# Lancer le webserver
airflow webserver --port 8080
