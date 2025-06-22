with base as (
    select
        _id as company_id,
        name as company_name,
        region as region
    from {{ source('public', 'synthetic_data') }}
)

select * from base
