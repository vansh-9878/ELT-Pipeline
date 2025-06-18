select
    week_start,
    driver_id,
    sum(total_daily_speeding_events) as total_speeding_events
from {{ ref('fct_inspection_summary') }}
group by week_start, driver_id
