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
        jsonb_array_elements(route -> 'stops') as stop
    from routes
), packages as (
    select
        driver_id,
        jsonb_array_elements(stop -> 'packages') as package
    from stops
)

select
    driver_id,
    package ->> 'trackingId' as tracking_id,
    (package ->> 'weightKg')::numeric as weight_kg,
    (package -> 'dimensionsCm' ->> 'l')::int as length_cm,
    (package -> 'dimensionsCm' ->> 'w')::int as width_cm,
    (package -> 'dimensionsCm' ->> 'h')::int as height_cm,
    (package ->> 'hazmat')::boolean as hazmat
from packages
