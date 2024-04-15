select id as product_id,
       title,
       created_at,
       updated_at
from {{ source('food_store', 'products') }}