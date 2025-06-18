select
    route_date,
    driver_id,
    avg(route_score) as avg_route_score
from {{ ref('fct_route_performance') }}
group by route_date, driver_id
