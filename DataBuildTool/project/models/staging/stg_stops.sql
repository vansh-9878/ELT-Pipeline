with raw as (
    select 
        data ->> 'driverId' as driver_id,
        jsonb_array_elements(data -> 'weeklyStats') as week
    from {{ source('public', 'data') }}
), routes as (
    select
        driver_id,
        jsonb_array_elements(week -> 'dailyRoutes') as route
    from raw
), stops as (
    select
        driver_id,
        route ->> 'routeId' as route_id,
        jsonb_array_elements(route -> 'stops') as stop
    from routes
)

select
    driver_id,
    route_id,
    (stop ->> 'stopNumber')::int as stop_number,
    stop ->> 'address' as address,
    (stop -> 'coordinates' ->> 'lat')::numeric as lat,
    (stop -> 'coordinates' ->> 'lon')::numeric as lon,
    (stop ->> 'deliveredCount')::int as delivered_count,
    (stop ->> 'attempts')::int as attempts,
    stop ->> 'scanTime' as scan_time
from stops
