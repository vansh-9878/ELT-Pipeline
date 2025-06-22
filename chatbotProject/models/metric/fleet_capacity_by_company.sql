
select
    company_id,
    sum(capacity_packages) as total_capacity_packages
from {{ ref('vehicles') }}
group by company_id
