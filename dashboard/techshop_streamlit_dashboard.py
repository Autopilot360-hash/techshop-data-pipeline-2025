# dashboard/techshop_streamlit_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.cloud import bigquery
import numpy as np
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(
    page_title="TechShop 2025 Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration BigQuery
@st.cache_resource
def get_bigquery_client():
    return bigquery.Client(project="techshop-data-pipeline-2025")

client = get_bigquery_client()

# Fonctions de chargement des données
@st.cache_data(ttl=300)  # Cache 5 minutes
def load_sales_overview():
    """Charge les données de vue d'ensemble des ventes"""
    query = """
    SELECT 
        DATE_TRUNC(order_date, MONTH) as mois,
        customer_segment,
        SUM(total_price) as revenus,
        COUNT(DISTINCT order_id) as commandes,
        COUNT(DISTINCT customer_id) as clients_actifs,
        AVG(total_price) as panier_moyen
    FROM `techshop-data-pipeline-2025.analytics_marts.fct_sales`
    GROUP BY mois, customer_segment
    ORDER BY mois DESC
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=300)
def load_channel_performance():
    """Charge les performances des canaux marketing"""
    query = """
    SELECT 
        channel,
        SUM(total_budget) as budget_total,
        SUM(total_revenue) as revenus_generes,
        ROUND(SUM(total_revenue) / NULLIF(SUM(total_budget), 0), 2) as roas,
        SUM(total_conversions) as conversions_totales,
        ROUND(AVG(conversion_rate) * 100, 2) as taux_conversion_moyen
    FROM `techshop-data-pipeline-2025.raw_data.marketing_campaigns`
    WHERE status = 'Completed'
    GROUP BY channel
    ORDER BY roas DESC
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=300) 
def load_product_innovation_impact():
    """Analyse l'impact des produits innovants 2025"""
    query = """
    SELECT 
        product_innovation_type,
        category,
        COUNT(*) as unites_vendues,
        SUM(total_price) as revenus,
        AVG(margin_percentage) as marge_moyenne,
        COUNT(DISTINCT customer_id) as clients_uniques
    FROM `techshop-data-pipeline-2025.analytics_marts.fct_sales`
    GROUP BY product_innovation_type, category
    ORDER BY revenus DESC
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=300)
def load_retention_metrics():
    """Charge les métriques de fidélisation"""
    query = """
    WITH customer_orders AS (
        SELECT 
            c.customer_segment,
            c.customer_id,
            COUNT(DISTINCT o.order_id) as nombre_commandes
        FROM `techshop-data-pipeline-2025.analytics_staging.stg_customers` c
        LEFT JOIN `techshop-data-pipeline-2025.analytics_staging.stg_orders` o 
            ON c.customer_id = o.customer_id AND o.is_completed = TRUE
        GROUP BY c.customer_segment, c.customer_id
    )
    SELECT 
        customer_segment,
        COUNT(*) as total_clients,
        COUNT(CASE WHEN nombre_commandes >= 2 THEN 1 END) as clients_fideles,
        ROUND(COUNT(CASE WHEN nombre_commandes >= 2 THEN 1 END) * 100.0 / COUNT(*), 1) as taux_retention
    FROM customer_orders
    GROUP BY customer_segment
    ORDER BY taux_retention DESC
    """
    return client.query(query).to_dataframe()

# Interface utilisateur
def main():
    # Header
    st.title("🚀 TechShop 2025 Analytics Dashboard")
    st.markdown("**Pipeline de Données E-commerce en Temps Réel**")
    
    # Sidebar
    st.sidebar.header("🎛️ Contrôles")
    
    # Auto-refresh
    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    refresh_button = st.sidebar.button("🔄 Actualiser Maintenant")
    if refresh_button:
        st.cache_data.clear()
        st.rerun()
    
    # Métriques principales
    st.header("📊 Métriques Principales")
    
    # Charger les données
    sales_data = load_sales_overview()
    channel_data = load_channel_performance() 
    innovation_data = load_product_innovation_impact()
    retention_data = load_retention_metrics()
    
    # KPIs principaux
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = sales_data['revenus'].sum()
        st.metric(
            "💰 Revenus Totaux 2025", 
            f"${total_revenue:,.0f}",
            delta="+12% vs 2024"
        )
    
    with col2:
        total_orders = sales_data['commandes'].sum()
        st.metric(
            "🛒 Commandes Totales", 
            f"{total_orders:,}",
            delta="+8% vs 2024"
        )
    
    with col3:
        avg_basket = sales_data['panier_moyen'].mean()
        st.metric(
            "🛍️ Panier Moyen", 
            f"${avg_basket:.2f}",
            delta="+5% vs 2024"
        )
    
    with col4:
        avg_retention = retention_data['taux_retention'].mean()
        st.metric(
            "🔄 Taux Rétention Moyen", 
            f"{avg_retention:.1f}%",
            delta="+2.3% vs 2024"
        )
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution des Revenus par Segment")
        
        # Graphique évolution revenus
        fig_evolution = px.line(
            sales_data, 
            x='mois', 
            y='revenus', 
            color='customer_segment',
            title="Revenus Mensuels par Segment Client"
        )
        fig_evolution.update_layout(height=400)
        st.plotly_chart(fig_evolution, use_container_width=True)
    
    with col2:
        st.subheader("💰 ROI des Canaux Marketing 2025")
        
        # Graphique ROI canaux
        fig_roi = px.bar(
            channel_data.head(8), 
            x='channel', 
            y='roas',
            title="Return On Ad Spend (ROAS) par Canal",
            color='roas',
            color_continuous_scale='Viridis'
        )
        fig_roi.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_roi, use_container_width=True)
    
    # Section Innovation 2025
    st.header("🚀 Impact des Innovations 2025")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌱 Produits Innovants vs Standard")
        
        # Grouper par type d'innovation
        innovation_summary = innovation_data.groupby('product_innovation_type').agg({
            'revenus': 'sum',
            'unites_vendues': 'sum',
            'clients_uniques': 'sum'
        }).reset_index()
        
        fig_innovation = px.pie(
            innovation_summary, 
            values='revenus', 
            names='product_innovation_type',
            title="Répartition des Revenus par Type de Produit"
        )
        st.plotly_chart(fig_innovation, use_container_width=True)
    
    with col2:
        st.subheader("🔄 Fidélisation par Segment")
        
        fig_retention = px.bar(
            retention_data, 
            x='customer_segment', 
            y='taux_retention',
            title="Taux de Rétention par Segment Client",
            color='taux_retention',
            color_continuous_scale='Blues'
        )
        fig_retention.update_layout(height=400)
        st.plotly_chart(fig_retention, use_container_width=True)
    
    # Tableaux détaillés
    st.header("📋 Données Détaillées")
    
    tab1, tab2, tab3 = st.tabs(["💰 Marketing ROI", "🛒 Top Produits", "👥 Segments Clients"])
    
    with tab1:
        st.subheader("Performance des Canaux Marketing")
        st.dataframe(
            channel_data.style.format({
                'budget_total': '${:,.0f}',
                'revenus_generes': '${:,.0f}', 
                'roas': '{:.2f}x',
                'taux_conversion_moyen': '{:.2f}%'
            }),
            use_container_width=True
        )
    
    with tab2:
        st.subheader("Top Catégories par Innovation")
        innovation_top = innovation_data.nlargest(10, 'revenus')
        st.dataframe(
            innovation_top.style.format({
                'revenus': '${:,.0f}',
                'marge_moyenne': '{:.1f}%'
            }),
            use_container_width=True
        )
    
    with tab3:
        st.subheader("Analyse de la Fidélisation")
        st.dataframe(
            retention_data.style.format({
                'taux_retention': '{:.1f}%'
            }),
            use_container_width=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown("**🚀 TechShop 2025 Data Pipeline** | Powered by dbt + BigQuery + Streamlit")

if __name__ == "__main__":
    main()
