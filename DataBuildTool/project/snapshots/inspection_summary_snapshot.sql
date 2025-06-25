{% snapshot inspection_summary_snapshot %}
{{
  config(
    target_schema='snapshots',
    unique_key='vehicle_id || inspection_date',
    strategy='check',
    check_cols=['total_items', 'passed', 'failed', 'failed_with_notes']
  )
}}

with summary as (
    select
        vehicle_id,
        inspection_date,
        total_items,
        passed,
        failed,
        failed_with_notes
    from {{ ref('fct_inspection_summary') }} 
)

select * from summary

{% endsnapshot %}
