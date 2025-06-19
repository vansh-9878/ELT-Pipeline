
select
    company_id,
    count(*) as driver_count
from {{ ref('drivers') }}
group by company_id
