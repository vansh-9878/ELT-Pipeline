with source as (
    select *
    from {{ source('public', 'data') }}
),


devices as (
SELECT
    data -> 'device' ->> 'model' as model,
    data -> 'driverId' as driver_id,
    data -> 'device' ->> 'osVersion' as os_version
from source
)

SELECT * from devices