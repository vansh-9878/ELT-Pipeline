
with base as (
    select
        data ->> '_id' as company_id,
        jsonb_array_elements(data -> 'fleet') as vehicle
    from {{ source('public', 'synthetic_data') }}
),

vehicle_logs as (
    select
        vehicle ->> '_id' as vehicle_id,
        jsonb_array_elements(vehicle -> 'maintenance_logs') as log
    from base
),

tasks as (
    select
        vehicle_id,
        log ->> 'service_date' as service_date,
        jsonb_array_elements(log -> 'details' -> 'tasks') as task
    from vehicle_logs
)

select
    vehicle_id,
    service_date,
    task ->> 'task' as task_name,
    (task ->> 'cost')::int as task_cost
from tasks
