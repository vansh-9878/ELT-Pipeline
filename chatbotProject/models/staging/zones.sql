

with base as (
    select
        _id as company_id,
        jsonb_array_elements(active_zones) as zone
    from {{ source('public', 'synthetic_data') }}
),

boundaries as (
    select
        company_id,
        zone ->> '_id' as zone_id,
        zone ->> 'name' as zone_name,
        jsonb_array_elements(zone -> 'boundaries') as boundary_set
    from base
),

points as (
    select
        company_id,
        zone_id,
        zone_name,
        jsonb_array_elements(boundary_set) as point
    from boundaries
)

select
    company_id,
    zone_id,
    zone_name,
    (point ->> 'lat')::float as lat,
    (point ->> 'lng')::float as lng
from points
