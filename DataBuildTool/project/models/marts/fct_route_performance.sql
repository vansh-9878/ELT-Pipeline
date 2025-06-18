with routes as (
    select 
        route_id,
        driver_id,
        route_date,
        shift_start,
        shift_end,
        on_road_time_min,
        route_score,
        deliveries
    from {{ ref('stg_daily_routes') }}
),

stops as (
    select 
        route_id,
        count(*) as num_stops,
        sum(delivered_count) as num_successful_deliveries
    from {{ ref('stg_stops') }}
    group by route_id
)

select
    r.route_id,
    r.driver_id,
    r.route_date,
    r.shift_start,
    r.shift_end,
    r.on_road_time_min,
    r.route_score,
    r.deliveries,
    coalesce(s.num_stops, 0) as num_stops,
    coalesce(s.num_successful_deliveries, 0) as num_successful_deliveries
from routes r
left join stops s on r.route_id = s.route_id
