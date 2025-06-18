with weekly as (
    select 
        data ->> 'driverId' as driver_id,
        jsonb_array_elements(data -> 'weeklyStats') as week
    from {{ source('public', 'data') }}
), routes as (
    select
        driver_id,
        week ->> 'weekStart' as week_start,
        week ->> 'weekEnd' as week_end,
        jsonb_array_elements(week -> 'dailyRoutes') as route
    from weekly
)

select
    driver_id,
    week_start,
    week_end,
    route ->> 'routeId' as route_id,
    route ->> 'date' as route_date,
    route ->> 'shiftStart' as shift_start,
    route ->> 'shiftEnd' as shift_end,
    (route ->> 'onRoadTimeMin')::int as on_road_time_min,
    (route ->> 'routeScore')::numeric as route_score,
    (route ->> 'deliveries')::int as deliveries
from routes
