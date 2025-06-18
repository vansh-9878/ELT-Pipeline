with source as (
    select *
    from {{ source('public', 'data') }}
),


employments as (
SELECT
    data -> 'employment' ->> 'hireDate' as hire_date,
    data -> 'driverId' as driver_id,
    data -> 'employment' ->> 'status' as status
from {{ source('public', 'data') }}
)

SELECT * from employments