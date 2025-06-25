-- snapshots/driver_shifts_snapshot.sql

{% snapshot driver_shifts_snapshot %}
{{
  config(
    target_schema='snapshots',
    unique_key='driver_id',
    strategy='check',
    check_cols=['shift_start', 'shift_end']
  )
}}

with shifts as (
    select
        driver_id,
        driver_name,
        calendar_date,
        shift_start,
        shift_end
    from {{ ref('dim_driver_schedule') }} 
)

select * from shifts

{% endsnapshot %}
