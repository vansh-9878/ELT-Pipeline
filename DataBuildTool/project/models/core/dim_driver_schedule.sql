{{ config(materialized='table') }}

with drivers as (
    select
        driver ->> '_id' as driver_id,
        driver ->> 'name' as driver_name,
        jsonb_array_elements(driver -> 'weekly_schedule') as schedule
    from {{ source('public', 'synthetic_data') }},
    lateral jsonb_array_elements(data -> 'drivers') as driver
),

expanded_schedule as (
    -- generate calendar days for the next 3 weeks
    select
        generate_series(current_date, current_date + interval '21 days', interval '1 day')::date as calendar_date
),

driver_dates as (
    select
        d.*,
        e.calendar_date
    from drivers d
    join expanded_schedule e
        on trim(to_char(e.calendar_date, 'Dy')) = d.schedule ->> 'day'
),

shifts as (
    select
        driver_id,
        driver_name,
        calendar_date,
        shift ->> 'start' as shift_start,
        shift ->> 'end' as shift_end
    from driver_dates,
    lateral jsonb_array_elements(schedule -> 'shifts') as shift
)

select *
from shifts
order by driver_id, calendar_date
