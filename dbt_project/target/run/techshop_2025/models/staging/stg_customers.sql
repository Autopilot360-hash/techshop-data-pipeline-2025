

  create or replace view `techshop-data-pipeline-2025`.`analytics_staging`.`stg_customers`
  OPTIONS()
  as -- dbt_project/models/staging/stg_customers.sql


SELECT 
  customer_id,
  first_name,
  last_name,
  LOWER(email) as email,
  UPPER(country) as country_code,
  city,
  created_at,
  customer_segment,
  ROUND(lifetime_value, 2) as lifetime_value,
  ROUND(avg_order_value, 2) as avg_order_value,
  order_frequency,
  SPLIT(preferred_categories, ',') as preferred_categories_array,
  is_vip,
  newsletter_subscriber,
  mobile_app_user,
  last_active_date,
  
  -- Calculs dérivés
  DATE_DIFF(CURRENT_DATE(), created_at, DAY) as days_since_signup,
  DATE_DIFF(CURRENT_DATE(), last_active_date, DAY) as days_since_last_active,
  
  -- Segmentation par ancienneté
  CASE 
    WHEN DATE_DIFF(CURRENT_DATE(), created_at, DAY) <= 30 THEN 'New (0-30 days)'
    WHEN DATE_DIFF(CURRENT_DATE(), created_at, DAY) <= 90 THEN 'Recent (31-90 days)' 
    WHEN DATE_DIFF(CURRENT_DATE(), created_at, DAY) <= 365 THEN 'Established (91-365 days)'
    ELSE 'Veteran (1+ years)'
  END as customer_tenure_segment,
  
  -- Statut d'activité
  CASE 
    WHEN DATE_DIFF(CURRENT_DATE(), last_active_date, DAY) <= 30 THEN 'Active'
    WHEN DATE_DIFF(CURRENT_DATE(), last_active_date, DAY) <= 90 THEN 'At Risk'
    ELSE 'Inactive' 
  END as activity_status

FROM `techshop-data-pipeline-2025`.`raw_data`.`customers`;

