{{ config(materialized='table') }}

with companies as (

    select
        data as company,
        data ->> '_id' as company_id,
        data ->> 'name' as company_name
    from {{ source('public', 'synthetic_data') }}

),

-- Explode fleet per company
vehicles as (
    select
        company_id,
        company_name,
        jsonb_array_elements(company->'fleet') as vehicle
    from companies
),

-- Explode current_assignments per vehicle
assignments as (
    select
        company_id,
        company_name,
        vehicle->>'_id' as vehicle_id,
        jsonb_array_elements(vehicle->'current_assignments') as assignment
    from vehicles
),

-- Explode planned_stops_full per assignment
stops as (
    select
        company_id,
        company_name,
        vehicle_id,
        jsonb_array_elements(assignment->'details'->'planned_stops_full') as stop
    from assignments
),

-- Extract delivery_attempts per stop
attempts as (
    select
        company_id,
        company_name,
        vehicle_id,
        stop->>'_id' as stop_id,
        stop->>'package_id' as package_id,
        jsonb_array_elements(event->'attempts') as attempt
    from stops,
    lateral (
        select event
        from jsonb_array_elements(stop->'events') as event
        where event->>'type' = 'delivery_attempts'
    ) as filtered_event
    where jsonb_typeof(filtered_event.event->'attempts') = 'array'
)

select
    company_id,
    company_name,
    vehicle_id,
    stop_id,
    package_id,
    attempt->>'ts' as timestamp,
    attempt->>'status' as status,
    attempt->'exception'->>'code' as exception_code,
    attempt->'exception'->>'reason' as exception_reason
from attempts
