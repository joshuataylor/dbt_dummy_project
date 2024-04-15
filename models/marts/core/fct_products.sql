select product_id,
       42           as sales
from {{ ref('stg_products') }}

