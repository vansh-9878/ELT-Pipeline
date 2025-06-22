
select
    vehicle_id,
    count(*) as failed_checklist_items
from {{ ref('inspection_checklist') }}
where status != 'pass'
group by vehicle_id
