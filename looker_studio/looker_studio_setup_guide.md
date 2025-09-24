# 📊 Guide de Configuration Looker Studio

## 1. Connexion à BigQuery
1. Aller sur https://lookerstudio.google.com
2. Créer un nouveau rapport
3. Sélectionner "BigQuery" comme source
4. Projet : `techshop-data-pipeline-2025`
5. Dataset : `analytics_marts`

## 2. Sources de Données Recommandées
- **Vue principale** : `looker_sales_overview` (pour KPIs et tendances)
- **Marketing** : `looker_marketing_roi` (pour ROI des campagnes)  
- **Fidélisation** : `looker_customer_retention` (pour métriques clients)

## 3. Visualisations à Créer

### Page 1 : Executive Dashboard
- **Scorecard** : Revenus totaux, Commandes, Clients actifs
- **Time Series** : Évolution mensuelle des revenus
- **Pie Chart** : Répartition par segment client
- **Bar Chart** : Top 5 catégories

### Page 2 : Marketing ROI
- **Scorecard** : ROAS global, Budget total
- **Bar Chart** : ROI par canal marketing
- **Scatter Plot** : Budget vs Revenus générés
- **Table** : Détail des campagnes

### Page 3 : Innovation 2025
- **Donut Chart** : Eco-friendly vs Standard
- **Bar Chart** : Performance produits IA
- **Geographic Map** : Adoption par pays
- **Trend Line** : Évolution adoption innovations

## 4. Filtres Recommandés
- Date Range : Période d'analyse
- Segment Client : Premium, Regular, Budget, Enterprise
- Canal de Vente : Website, Mobile App, Physical Store
- Type Innovation : Standard, Eco-friendly, AI-Enabled, Eco-AI

## 5. Partage et Collaboration
- Partager avec l'équipe business
- Programmer des rapports automatiques
- Intégrer dans Google Workspace
