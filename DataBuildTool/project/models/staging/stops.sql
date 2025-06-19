with base as (
    select
        data ->> '_id' as company_id,
        jsonb_array_elements(data -> 'fleet') as vehicle
    from {{ source('public', 'synthetic_data') }}
),

assignments as (
    select
        vehicle ->> '_id' as vehicle_id,
        jsonb_array_elements(vehicle -> 'current_assignments') as assignment
    from base
),

stops as (
    select
        vehicle_id,
        assignment ->> 'route_id' as route_id,
        jsonb_array_elements(assignment -> 'details' -> 'planned_stops_full') as stop
    from assignments
),

events as (
    select
        vehicle_id,
        route_id,
        stop ->> '_id' as stop_id,
        stop ->> 'package_id' as package_id,
        stop ->> 'address' as address,
        jsonb_array_elements(stop -> 'events') as event
    from stops
),

pivoted as (
    select
        vehicle_id,
        route_id,
        stop_id,
        package_id,
        address,
        max(case when event ->> 'type' = 'arrival' then event ->> 'ts' end) as arrival_timestamp,
        max(case when event ->> 'type' = 'arrival' then event ->> 'ts' end) as delivery_attempts_timestamp
    from events
    where event ->> 'type' in ('arrival', 'delivery_attempts')
    group by vehicle_id, route_id, stop_id, package_id, address
)

select
    vehicle_id,
    route_id,
    stop_id,
    package_id,
    address,
    'arrival' as event,
    arrival_timestamp as timestamp
from pivoted
