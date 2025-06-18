with raw as (
    select data
    from {{ source('public', 'data') }}
)

select
    data ->> 'driverId' as driver_id,
    data ->> 'name' as name
from raw
