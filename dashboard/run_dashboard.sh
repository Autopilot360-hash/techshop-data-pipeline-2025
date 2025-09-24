#!/bin/bash
echo "🚀 Lancement du Dashboard TechShop 2025"

# Activer l'environnement virtuel
source ../venv3/bin/activate

# Installer les dépendances
pip install -r requirements_dashboard.txt

# Lancer Streamlit
echo "📊 Dashboard accessible sur : http://localhost:8501"
streamlit run techshop_streamlit_dashboard.py --server.port 8501
