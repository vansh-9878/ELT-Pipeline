select
    date,
    driver_id,
    count(route_id) as route_count
from {{ ref('dim_driver_schedule') }}
group by date, driver_id
