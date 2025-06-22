
with base as (
    select
        jsonb_array_elements(fleet) as vehicle
    from {{ source('public', 'synthetic_data') }}
),

inspections as (
    select
        vehicle ->> '_id' as vehicle_id,
        jsonb_array_elements(vehicle -> 'inspections') as inspection
    from base
),

checklist as (
    select
        inspection ->> '_id' as inspection_id,
        vehicle_id,
        inspection ->> 'date' as inspection_date,
        inspection -> 'inspector' ->> 'id' as inspector_id,
        inspection -> 'inspector' ->> 'name' as inspector_name,
        jsonb_array_elements(inspection -> 'checklist') as item
    from inspections
)

select
    inspection_id,
    vehicle_id,
    inspection_date,
    inspector_id,
    inspector_name,
    item ->> 'item' as checklist_item,
    item ->> 'status' as status,
    item ->> 'notes' as notes
from checklist
