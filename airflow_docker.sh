#!/bin/bash
# Script de gestion Airflow Docker pour TechShop 2025

case "$1" in
    start)
        echo "🚀 Démarrage d'Airflow TechShop avec Docker..."
        export AIRFLOW_UID=$(id -u)
        docker-compose up -d
        echo "✅ Airflow démarré !"
        echo "📊 Interface web : http://localhost:8080"
        echo "👤 Login: admin / Mot de passe: admin123"
        echo ""
        echo "⏳ Attendez ~2 minutes que tous les services démarrent..."
        ;;
    stop)
        echo "🛑 Arrêt d'Airflow..."
        docker-compose down
        echo "✅ Airflow arrêté !"
        ;;
    restart)
        echo "🔄 Redémarrage d'Airflow..."
        docker-compose down
        export AIRFLOW_UID=$(id -u)
        docker-compose up -d
        echo "✅ Airflow redémarré !"
        ;;
    logs)
        echo "📋 Logs Airflow..."
        docker-compose logs -f
        ;;
    status)
        echo "📊 Status des services Airflow..."
        docker-compose ps
        ;;
    clean)
        echo "🧹 Nettoyage complet (ATTENTION: supprime toutes les données)..."
        read -p "Êtes-vous sûr ? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v
            docker system prune -f
            echo "✅ Nettoyage terminé !"
        else
            echo "❌ Nettoyage annulé"
        fi
        ;;
    *)
        echo "🚀 Script de gestion Airflow TechShop 2025"
        echo ""
        echo "Usage: $0 {start|stop|restart|logs|status|clean}"
        echo ""
        echo "Commandes :"
        echo "  start   - Démarrer Airflow"
        echo "  stop    - Arrêter Airflow" 
        echo "  restart - Redémarrer Airflow"
        echo "  logs    - Voir les logs en temps réel"
        echo "  status  - Voir le statut des services"
        echo "  clean   - Nettoyage complet (supprime tout)"
        echo ""
        exit 1
        ;;
esac
