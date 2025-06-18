select
    week_start,
    driver_id,
    avg(avg_daily_seatbelt_pct) as avg_seatbelt_compliance_pct
from {{ ref('fct_inspection_summary') }}
group by week_start, driver_id
