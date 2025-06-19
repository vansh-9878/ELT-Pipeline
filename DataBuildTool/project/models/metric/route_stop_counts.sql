
select
    route_id,
    count(distinct stop_id) as stop_count
from {{ ref('fct_route_performance') }}
group by route_id
