-- sql/create_datasets.sql
-- Création des datasets pour TechShop 2025

-- Dataset pour données brutes
CREATE SCHEMA IF NOT EXISTS `techshop-data-pipeline-2025.raw_data`
OPTIONS (
  description='Raw data from various sources for TechShop 2025',
  location='US'
);

-- Dataset pour données staging/transformées
CREATE SCHEMA IF NOT EXISTS `techshop-data-pipeline-2025.staging`
OPTIONS (
  description='Staged and cleaned data for TechShop 2025',
  location='US'
);

-- Dataset pour données finales/marts
CREATE SCHEMA IF NOT EXISTS `techshop-data-pipeline-2025.marts`
OPTIONS (
  description='Final data marts and analytics tables for TechShop 2025',
  location='US'
);
