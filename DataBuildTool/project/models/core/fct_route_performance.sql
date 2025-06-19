with assignments as (
    select
        data ->> '_id' as company_id,
        data ->> 'name' as company_name,
        vehicle ->> '_id' as vehicle_id,
        assignment ->> 'route_id' as route_id,
        assignment ->> 'start_date' as route_start_date,
        jsonb_array_elements(assignment -> 'details' -> 'planned_stops_full') as stop
    from {{ source('public', 'synthetic_data') }},
    lateral jsonb_array_elements(data -> 'fleet') as vehicle,
    lateral jsonb_array_elements(vehicle -> 'current_assignments') as assignment
),

stops_with_events as (
    select
        a.*,
        stop ->> '_id' as stop_id,
        stop ->> 'package_id' as package_id,
        stop ->> 'address' as address,
        event
    from assignments a,
    lateral jsonb_array_elements(stop -> 'events') as event
),

delivery_attempts as (
    select
        s.*,
        attempt,
        attempt ->> 'status' as status,
        attempt -> 'exception' ->> 'code' as exception_code,
        attempt -> 'exception' ->> 'reason' as exception_reason
    from stops_with_events s,
    lateral jsonb_array_elements(s.event -> 'attempts') as attempt
    where s.event ->> 'type' = 'delivery_attempts'
)

select
    company_id,
    company_name,
    route_id,
    route_start_date,
    vehicle_id,
    stop_id,
    package_id,
    address,
    status,
    exception_code,
    exception_reason
from delivery_attempts
