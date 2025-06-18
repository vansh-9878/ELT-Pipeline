with dates as (
    select
        generate_series(
            date '2025-01-01',
            date '2025-12-31',
            interval '1 day'
        )::date as date
)

select
    date,
    to_char(date, 'Day') as weekday_name,
    extract(dow from date) as weekday_number
from dates
