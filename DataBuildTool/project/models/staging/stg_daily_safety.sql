with routes as (
    select 
        data ->> 'driverId' as driver_id,
        jsonb_array_elements(data -> 'weeklyStats') as week
    from {{ source('public', 'data') }}
), daily_routes as (
    select
        driver_id,
        jsonb_array_elements(week -> 'dailyRoutes') as route
    from routes
), safety as (
    select
        driver_id,
        route ->> 'routeId' as route_id,
        route -> 'safety' as safety
    from daily_routes
)

select
    driver_id,
    route_id,
    (safety ->> 'seatBeltCompliancePct')::numeric as seat_belt_compliance_pct,
    (safety ->> 'speedingEvents')::int as speeding_events,
    (safety ->> 'harshBrakingEvents')::int as harsh_braking_events
from safety
