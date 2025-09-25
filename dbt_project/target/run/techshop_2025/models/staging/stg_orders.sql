

  create or replace view `techshop-data-pipeline-2025`.`staging`.`stg_orders`
  OPTIONS()
  as -- dbt_project/models/staging/stg_orders.sql


SELECT 
  order_id,
  customer_id,
  order_date,
  ROUND(total_amount, 2) as total_amount,
  ROUND(shipping_cost, 2) as shipping_cost,
  ROUND(total_amount - shipping_cost, 2) as subtotal,
  payment_method,
  order_status,
  sales_channel,
  num_items,
  shipped_date,
  delivered_date,
  created_at,
  
  -- Calculs temporels
  DATE_DIFF(shipped_date, order_date, DAY) as days_to_ship,
  DATE_DIFF(delivered_date, shipped_date, DAY) as days_in_transit,
  DATE_DIFF(delivered_date, order_date, DAY) as total_fulfillment_days,
  
  -- Segmentation par montant
  CASE 
    WHEN total_amount < 50 THEN 'Low Value (<$50)'
    WHEN total_amount < 150 THEN 'Medium Value ($50-$150)'
    WHEN total_amount < 300 THEN 'High Value ($150-$300)'
    ELSE 'Premium Value ($300+)'
  END as order_value_segment,
  
  -- Indicateurs temporels 2025
  EXTRACT(YEAR FROM order_date) as order_year,
  EXTRACT(QUARTER FROM order_date) as order_quarter,
  EXTRACT(MONTH FROM order_date) as order_month,
  EXTRACT(DAYOFWEEK FROM order_date) as order_day_of_week,
  FORMAT_DATE('%A', order_date) as order_day_name,
  
  -- Indicateurs saisonniers
  CASE 
    WHEN EXTRACT(MONTH FROM order_date) IN (12, 1, 2) THEN 'Winter'
    WHEN EXTRACT(MONTH FROM order_date) IN (3, 4, 5) THEN 'Spring'
    WHEN EXTRACT(MONTH FROM order_date) IN (6, 7, 8) THEN 'Summer'
    ELSE 'Fall'
  END as season,
  
  -- Indicateurs de performance
  shipping_cost = 0 as is_free_shipping,
  order_status = 'Completed' as is_completed,
  sales_channel = 'Mobile App' as is_mobile_order

FROM `techshop-data-pipeline-2025`.`raw_data`.`orders`
WHERE order_date >= '2025-01-01'
  AND order_date <= '2025-12-31';

