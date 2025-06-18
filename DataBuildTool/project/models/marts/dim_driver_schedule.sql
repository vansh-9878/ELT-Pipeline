with daily_routes as (
    select
        driver_id,
        route_id,
        route_date
    from {{ ref('stg_daily_routes') }}
)

select
    route_date as date,
    driver_id,
    route_id
from daily_routes
