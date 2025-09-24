-- sql/analysis_queries.sql
-- Requêtes d'analyse pour TechShop 2025

-- 1. Vue d'ensemble des ventes 2025
SELECT 
  DATE_TRUNC(order_date, MONTH) as month,
  COUNT(*) as total_orders,
  SUM(total_amount) as total_revenue,
  AVG(total_amount) as avg_order_value,
  COUNT(DISTINCT customer_id) as unique_customers
FROM `techshop-data-pipeline-2025.raw_data.orders`
WHERE order_status = 'Completed'
  AND order_date >= '2025-01-01'
GROUP BY month
ORDER BY month;

-- 2. Performance par catégorie 2025
SELECT 
  p.category,
  COUNT(DISTINCT o.order_id) as total_orders,
  SUM(oi.total_price) as total_revenue,
  SUM(oi.quantity) as total_units_sold,
  AVG(p.avg_rating) as avg_category_rating
FROM `techshop-data-pipeline-2025.raw_data.orders` o
JOIN `techshop-data-pipeline-2025.raw_data.order_items` oi ON o.order_id = oi.order_id
JOIN `techshop-data-pipeline-2025.raw_data.products` p ON oi.product_id = p.product_id
WHERE o.order_status = 'Completed'
  AND o.order_date >= '2025-01-01'
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 3. Analyse des clients par segment 2025
SELECT 
  c.customer_segment,
  COUNT(*) as customer_count,
  AVG(c.lifetime_value) as avg_lifetime_value,
  COUNT(o.order_id) as total_orders,
  SUM(o.total_amount) as total_spent,
  AVG(o.total_amount) as avg_order_value
FROM `techshop-data-pipeline-2025.raw_data.customers` c
LEFT JOIN `techshop-data-pipeline-2025.raw_data.orders` o 
  ON c.customer_id = o.customer_id 
  AND o.order_date >= '2025-01-01'
  AND o.order_status = 'Completed'
GROUP BY c.customer_segment
ORDER BY total_spent DESC;

-- 4. ROI des campagnes marketing 2025
SELECT 
  channel,
  COUNT(*) as num_campaigns,
  SUM(total_budget) as total_spent,
  SUM(total_revenue) as total_revenue,
  SUM(total_revenue) / SUM(total_budget) as overall_roas,
  AVG(conversion_rate) as avg_conversion_rate
FROM `techshop-data-pipeline-2025.raw_data.marketing_campaigns`
WHERE start_date >= '2025-01-01'
  AND status = 'Completed'
GROUP BY channel
ORDER BY overall_roas DESC;

-- 5. Tendances des produits eco-friendly 2025
SELECT 
  DATE_TRUNC(o.order_date, QUARTER) as quarter,
  p.is_eco_friendly,
  COUNT(oi.product_id) as units_sold,
  SUM(oi.total_price) as revenue,
  AVG(p.price) as avg_price
FROM `techshop-data-pipeline-2025.raw_data.orders` o
JOIN `techshop-data-pipeline-2025.raw_data.order_items` oi ON o.order_id = oi.order_id
JOIN `techshop-data-pipeline-2025.raw_data.products` p ON oi.product_id = p.product_id
WHERE o.order_status = 'Completed'
  AND o.order_date >= '2025-01-01'
GROUP BY quarter, p.is_eco_friendly
ORDER BY quarter, p.is_eco_friendly;

-- 6. Top produits par ventes 2025
SELECT 
  p.product_name,
  p.category,
  p.brand,
  p.price,
  SUM(oi.quantity) as total_units_sold,
  SUM(oi.total_price) as total_revenue,
  COUNT(DISTINCT o.customer_id) as unique_customers,
  AVG(p.avg_rating) as rating
FROM `techshop-data-pipeline-2025.raw_data.products` p
JOIN `techshop-data-pipeline-2025.raw_data.order_items` oi ON p.product_id = oi.product_id
JOIN `techshop-data-pipeline-2025.raw_data.orders` o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
  AND o.order_date >= '2025-01-01'
GROUP BY p.product_id, p.product_name, p.category, p.brand, p.price, p.avg_rating
ORDER BY total_revenue DESC
LIMIT 20;
