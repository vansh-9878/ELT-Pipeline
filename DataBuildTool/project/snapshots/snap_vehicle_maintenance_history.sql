{% snapshot snap_vehicle_maintenance_history %}

{{
  config(
    target_schema='snapshots',
    unique_key='vehicle_id',
    strategy='check',
    check_cols=['mileage']
  )
}}

select 
  data -> 'vehicle' ->> 'vehicleId' as vehicle_id,
  (data -> 'vehicle' ->> 'mileage')::int as mileage,
  current_timestamp as snapshot_ts
from {{ source('public', 'data') }}

{% endsnapshot %}
