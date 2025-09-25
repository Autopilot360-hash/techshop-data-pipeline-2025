#!/bin/bash
# airflow_docker_fixed.sh - Script de gestion Airflow Docker pour TechShop 2025

# Détecter quelle version de docker compose utiliser
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "❌ Docker Compose non trouvé !"
    exit 1
fi

echo "🐳 Utilisation de : $DOCKER_COMPOSE"

case "$1" in
    start)
        echo "🚀 Démarrage d'Airflow TechShop avec Docker..."
        export AIRFLOW_UID=$(id -u)
        echo "AIRFLOW_UID=$AIRFLOW_UID" > .env
        $DOCKER_COMPOSE up -d
        echo "✅ Airflow démarré !"
        echo "📊 Interface web : http://localhost:8080"
        echo "👤 Login: admin / Mot de passe: admin123"
        echo ""
        echo "⏳ Attendez ~2 minutes que tous les services démarrent..."
        ;;
    stop)
        echo "🛑 Arrêt d'Airflow..."
        $DOCKER_COMPOSE down
        echo "✅ Airflow arrêté !"
        ;;
    restart)
        echo "🔄 Redémarrage d'Airflow..."
        $DOCKER_COMPOSE down
        export AIRFLOW_UID=$(id -u)
        echo "AIRFLOW_UID=$AIRFLOW_UID" > .env
        $DOCKER_COMPOSE up -d
        echo "✅ Airflow redémarré !"
        ;;
    logs)
        echo "📋 Logs Airflow..."
        $DOCKER_COMPOSE logs -f
        ;;
    status)
        echo "📊 Status des services Airflow..."
        $DOCKER_COMPOSE ps
        ;;
    *)
        echo "🚀 Script de gestion Airflow TechShop 2025"
        echo ""
        echo "Usage: $0 {start|stop|restart|logs|status}"
        echo ""
        echo "Commandes :"
        echo "  start   - Démarrer Airflow"
        echo "  stop    - Arrêter Airflow" 
        echo "  restart - Redémarrer Airflow"
        echo "  logs    - Voir les logs en temps réel"
        echo "  status  - Voir le statut des services"
        echo ""
        exit 1
        ;;
esac
