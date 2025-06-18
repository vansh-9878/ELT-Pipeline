{% snapshot snap_driver_employment_status %}

{{
  config(
    target_schema='snapshots',
    unique_key='driver_id',
    strategy='check',
    check_cols=['status']
  )
}}

select
  data ->> 'driverId' as driver_id,
  data -> 'employment' ->> 'hire_date' as hire_date,
  data -> 'employment' ->> 'status' as status
from {{ source('public', 'data') }}

{% endsnapshot %}
