
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer_id
from `techshop-data-pipeline-2025`.`raw_data`.`customers`
where customer_id is null



  
  
      
    ) dbt_internal_test