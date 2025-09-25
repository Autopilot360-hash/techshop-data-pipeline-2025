

  create or replace view `techshop-data-pipeline-2025`.`staging`.`stg_products`
  OPTIONS()
  as -- dbt_project/models/staging/stg_products.sql


SELECT 
  product_id,
  sku,
  product_name,
  category,
  subcategory,
  brand,
  ROUND(price, 2) as price,
  ROUND(cost, 2) as cost,
  ROUND(price - cost, 2) as margin_amount,
  ROUND((price - cost) / price * 100, 2) as margin_percentage,
  stock_quantity,
  ROUND(avg_rating, 2) as avg_rating,
  num_reviews,
  launch_date,
  weight,
  is_eco_friendly,
  is_ai_enabled,
  is_bestseller,
  created_at,
  updated_at,
  
  -- Segmentation par prix
  CASE 
    WHEN price < 50 THEN 'Budget (<$50)'
    WHEN price < 150 THEN 'Mid-Range ($50-$150)'
    WHEN price < 300 THEN 'Premium ($150-$300)'
    ELSE 'Luxury ($300+)'
  END as price_segment,
  
  -- Statut de popularité
  CASE 
    WHEN num_reviews >= 100 AND avg_rating >= 4.5 THEN 'Top Rated'
    WHEN num_reviews >= 50 AND avg_rating >= 4.0 THEN 'Well Rated'
    WHEN num_reviews >= 10 THEN 'Some Reviews'
    ELSE 'New/Few Reviews'
  END as review_status,
  
  -- Indicateurs 2025
  EXTRACT(YEAR FROM launch_date) = 2025 as is_new_2025,
  DATE_DIFF(CURRENT_DATE(), launch_date, DAY) as days_since_launch,
  stock_quantity <= 10 as is_low_stock,
  
  -- Catégorisation avancée
  CASE 
    WHEN is_eco_friendly AND is_ai_enabled THEN 'Eco-AI Product'
    WHEN is_eco_friendly THEN 'Eco-Friendly'
    WHEN is_ai_enabled THEN 'AI-Enabled'
    ELSE 'Standard'
  END as product_innovation_type

FROM `techshop-data-pipeline-2025`.`raw_data`.`products`;

