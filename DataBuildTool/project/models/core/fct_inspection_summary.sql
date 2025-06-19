{{ config(materialized='table') }}

with checklist as (
    select *
    from {{ ref('inspection_checklist') }}
),

summary as (
    select
        vehicle_id,
        inspection_date,
        count(*) as total_items,
        count(*) filter (where status = 'Pass') as passed,
        count(*) filter (where status = 'Fail') as failed,
        count(*) filter (where status = 'Fail' and notes is not null) as failed_with_notes
    from checklist
    group by vehicle_id, inspection_date
)

select *
from summary
