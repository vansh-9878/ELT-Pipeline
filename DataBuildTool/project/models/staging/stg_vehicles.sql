with raw as (
    select data from {{source('public','data')}}
)

SELECT
    data -> 'vehicle' ->> 'vehicleId' as vehicle_id,
    data -> 'driverId' as driver_id,
    data -> 'vehicle' ->> 'make' as make,
    data -> 'vehicle' ->> 'model' as model,
    (data -> 'vehicle' ->> 'mileage')::int as mileage
from raw
