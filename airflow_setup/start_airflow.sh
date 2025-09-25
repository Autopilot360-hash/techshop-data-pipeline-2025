# Remplacer airflow_setup/start_airflow.sh  
cat > airflow_setup/start_airflow.sh << 'EOF'
#!/bin/bash
echo "🚀 Démarrage d'Airflow TechShop 2025"

# Détecter le bon chemin vers l'environnement virtuel
if [ -d "/opt/app/bigquery-projects/venv3" ]; then
    VENV_PATH="/opt/app/bigquery-projects/venv3"
elif [ -d "../venv3" ]; then
    VENV_PATH="../venv3"
elif [ -d "../../venv3" ]; then
    VENV_PATH="../../venv3"
else
    echo "❌ Environnement virtuel non trouvé !"
    exit 1
fi

echo "📂 Utilisation de l'environnement virtuel : $VENV_PATH"

# Configuration
export AIRFLOW_HOME=~/airflow
source $VENV_PATH/bin/activate

# Vérifier qu'Airflow est installé
if ! command -v airflow &> /dev/null; then
    echo "❌ Airflow non installé. Exécutez d'abord :"
    echo "   bash install_airflow.sh"
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
EOF

chmod +x airflow_setup/start_airflow.sh
