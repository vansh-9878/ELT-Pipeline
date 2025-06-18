with source as (
    select *
    from {{ source('public', 'data') }}
),

dsps as (
SELECT
    data -> 'dsp' ->> 'dspId' as dsp_id,
    data -> 'driverId' as driver_id,
    data -> 'dsp' ->> 'name' as name,
    data -> 'dsp' ->> 'region' as region
from source
)

SELECT * from dsps