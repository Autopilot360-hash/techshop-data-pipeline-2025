-- Requêtes optimisées pour Looker Studio

-- 1. Vue principale pour dashboards
CREATE OR REPLACE VIEW `techshop-data-pipeline-2025.analytics_marts.looker_sales_overview` AS
SELECT 
    order_date,
    EXTRACT(YEAR FROM order_date) as year,
    EXTRACT(MONTH FROM order_date) as month,
    EXTRACT(QUARTER FROM order_date) as quarter,
    customer_segment,
    category,
    subcategory,
    brand,
    sales_channel,
    country_code,
    product_innovation_type,
    is_eco_friendly,
    is_ai_enabled,
    total_price as revenue,
    total_margin as profit,
    quantity,
    unit_price,
    1 as order_count,
    1 as item_count
FROM `techshop-data-pipeline-2025.analytics_marts.fct_sales`;

-- 2. Métriques marketing pour Looker
CREATE OR REPLACE VIEW `techshop-data-pipeline-2025.analytics_marts.looker_marketing_roi` AS
SELECT 
    channel,
    campaign_type,
    DATE(start_date) as campaign_date,
    EXTRACT(MONTH FROM start_date) as campaign_month,
    total_budget as budget,
    total_revenue as revenue,
    roas,
    conversion_rate,
    total_impressions as impressions,
    total_clicks as clicks,
    total_conversions as conversions,
    uses_ai_optimization,
    targets_gen_z,
    is_sustainable_focused
FROM `techshop-data-pipeline-2025.raw_data.marketing_campaigns`
WHERE status = 'Completed';

-- 3. Métriques de fidélisation pour Looker
CREATE OR REPLACE VIEW `techshop-data-pipeline-2025.analytics_marts.looker_customer_retention` AS
WITH customer_stats AS (
    SELECT 
        c.customer_id,
        c.customer_segment,
        c.country_code,
        c.is_vip,
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(o.total_amount) as total_spent,
        MIN(o.order_date) as first_order_date,
        MAX(o.order_date) as last_order_date
    FROM `techshop-data-pipeline-2025.analytics_staging.stg_customers` c
    LEFT JOIN `techshop-data-pipeline-2025.analytics_staging.stg_orders` o 
        ON c.customer_id = o.customer_id AND o.is_completed = TRUE
    GROUP BY c.customer_id, c.customer_segment, c.country_code, c.is_vip
)
SELECT 
    customer_segment,
    country_code,
    is_vip,
    COUNT(*) as total_customers,
    COUNT(CASE WHEN total_orders >= 2 THEN 1 END) as loyal_customers,
    ROUND(COUNT(CASE WHEN total_orders >= 2 THEN 1 END) * 100.0 / COUNT(*), 2) as retention_rate,
    AVG(total_spent) as avg_customer_value,
    AVG(total_orders) as avg_orders_per_customer
FROM customer_stats
GROUP BY customer_segment, country_code, is_vip;
