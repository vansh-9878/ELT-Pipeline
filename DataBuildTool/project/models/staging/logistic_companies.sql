with base as (
    select
        data ->> '_id' as company_id,
        data ->> 'name' as company_name,
        data ->> 'region' as region
    from {{ source('public', 'synthetic_data') }}
)

select * from base
