with source_data as (
    select 
        data ->> 'driverId' as driver_id,
        jsonb_array_elements(data -> 'weeklyStats') as week
    from {{ source('public', 'data') }}
)

select
    driver_id,
    week ->> 'weekStart' as week_start,
    week ->> 'weekEnd' as week_end
from source_data
