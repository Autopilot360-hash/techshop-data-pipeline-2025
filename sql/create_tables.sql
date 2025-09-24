-- sql/create_tables.sql
-- Création des tables BigQuery pour TechShop 2025

-- Table customers
CREATE TABLE IF NOT EXISTS `techshop-data-pipeline-2025.raw_data.customers` (
  customer_id STRING,
  first_name STRING,
  last_name STRING,
  email STRING,
  country STRING,
  city STRING,
  created_at DATE,
  customer_segment STRING,
  lifetime_value FLOAT64,
  avg_order_value FLOAT64,
  order_frequency FLOAT64,
  preferred_categories STRING,
  is_vip BOOLEAN,
  newsletter_subscriber BOOLEAN,
  mobile_app_user BOOLEAN,
  last_active_date DATE
)
PARTITION BY created_at
CLUSTER BY customer_segment, country;

-- Table products
CREATE TABLE IF NOT EXISTS `techshop-data-pipeline-2025.raw_data.products` (
  product_id STRING,
  sku STRING,
  product_name STRING,
  category STRING,
  subcategory STRING,
  brand STRING,
  price FLOAT64,
  cost FLOAT64,
  stock_quantity INTEGER,
  avg_rating FLOAT64,
  num_reviews INTEGER,
  launch_date DATE,
  weight FLOAT64,
  is_eco_friendly BOOLEAN,
  is_ai_enabled BOOLEAN,
  is_bestseller BOOLEAN,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY launch_date
CLUSTER BY category, brand;

-- Table orders
CREATE TABLE IF NOT EXISTS `techshop-data-pipeline-2025.raw_data.orders` (
  order_id STRING,
  customer_id STRING,
  order_date DATE,
  total_amount FLOAT64,
  shipping_cost FLOAT64,
  payment_method STRING,
  order_status STRING,
  sales_channel STRING,
  num_items INTEGER,
  shipped_date DATE,
  delivered_date DATE,
  created_at TIMESTAMP
)
PARTITION BY order_date
CLUSTER BY customer_id, order_status;

-- Table order_items
CREATE TABLE IF NOT EXISTS `techshop-data-pipeline-2025.raw_data.order_items` (
  order_id STRING,
  product_id STRING,
  product_name STRING,
  category STRING,
  quantity INTEGER,
  unit_price FLOAT64,
  total_price FLOAT64
)
CLUSTER BY order_id, product_id;

-- Table marketing_campaigns
CREATE TABLE IF NOT EXISTS `techshop-data-pipeline-2025.raw_data.marketing_campaigns` (
  campaign_id STRING,
  campaign_name STRING,
  campaign_type STRING,
  channel STRING,
  objective STRING,
  start_date DATE,
  end_date DATE,
  duration_days INTEGER,
  daily_budget FLOAT64,
  total_budget FLOAT64,
  total_impressions INTEGER,
  total_clicks INTEGER,
  total_conversions INTEGER,
  total_revenue FLOAT64,
  avg_cpc FLOAT64,
  cost_per_conversion FLOAT64,
  conversion_rate FLOAT64,
  roas FLOAT64,
  status STRING,
  uses_ai_optimization BOOLEAN,
  is_sustainable_focused BOOLEAN,
  targets_gen_z BOOLEAN,
  created_at TIMESTAMP
)
PARTITION BY start_date
CLUSTER BY channel, campaign_type;
