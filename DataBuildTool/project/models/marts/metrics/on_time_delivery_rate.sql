select
    route_date,
    driver_id,
    route_id,
    sum(num_successful_deliveries)::float / nullif(sum(deliveries), 0) as on_time_delivery_rate
from {{ ref('fct_route_performance') }}
group by route_date, driver_id, route_id
