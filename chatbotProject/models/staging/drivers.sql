
with base as (
    select
        _id as company_id,
        jsonb_array_elements(drivers) as driver
    from {{ source('public', 'synthetic_data') }}
)

select
    company_id,
    driver ->> '_id' as driver_id,
    driver ->> 'name' as driver_name,
    driver -> 'license' ->> 'class' as license_class,
    driver -> 'license' ->> 'expiry' as license_expiry
from base
