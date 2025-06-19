
select
    vehicle_id,
    sum(task_cost) as total_maintenance_cost
from {{ ref('vehicle_maintenance_tasks') }}
group by vehicle_id
