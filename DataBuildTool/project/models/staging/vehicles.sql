
with base as (
    select
        data ->> '_id' as company_id,
        jsonb_array_elements(data -> 'fleet') as vehicle
    from {{ source('public', 'synthetic_data') }}
)

select
    company_id,
    vehicle ->> '_id' as vehicle_id,
    vehicle ->> 'type' as vehicle_type,
    (vehicle ->> 'capacity_packages')::int as capacity_packages
from base
