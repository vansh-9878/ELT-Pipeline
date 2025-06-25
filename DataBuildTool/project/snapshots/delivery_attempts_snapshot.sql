{% snapshot delivery_attempts_snapshot %}
{{
  config(
    target_schema='snapshots',
    unique_key='package_id',
    strategy='check',
    check_cols=['status', 'exception_code', 'exception_reason']
  )
}}

with attempts as (
    select
        company_id,
        company_name,
        route_id,
        route_start_date,
        vehicle_id,
        stop_id,
        package_id,
        address,
        status,
        exception_code,
        exception_reason
    from {{ ref('fct_route_performance') }}  
)

select * from attempts

{% endsnapshot %}
