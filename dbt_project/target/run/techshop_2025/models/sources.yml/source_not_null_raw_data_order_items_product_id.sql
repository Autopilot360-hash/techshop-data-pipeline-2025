
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select product_id
from `techshop-data-pipeline-2025`.`raw_data`.`order_items`
where product_id is null



  
  
      
    ) dbt_internal_test