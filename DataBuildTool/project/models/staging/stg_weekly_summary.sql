with raw as (
    select 
        data ->> 'driverId' as driver_id,
        jsonb_array_elements(data -> 'weeklyStats') as week
    from {{ source('public', 'data') }}
), summaries as (
    select
        driver_id,
        week ->> 'weekStart' as week_start,
        week ->> 'weekEnd' as week_end,
        week -> 'summary' as summary
    from raw
)

select
    driver_id,
    week_start,
    week_end,
    (summary ->> 'totalStops')::int as total_stops,
    (summary ->> 'successfulDeliveries')::int as successful_deliveries,
    (summary ->> 'rescans')::int as rescans,
    (summary ->> 'lateDeliveries')::int as late_deliveries,

    (summary -> 'customerFeedback' ->> 'positive')::int as feedback_positive,
    (summary -> 'customerFeedback' ->> 'negative')::int as feedback_negative,

    (summary -> 'safety' ->> 'avgSeatBeltCompliancePct')::numeric as avg_seat_belt_compliance_pct,
    (summary -> 'safety' ->> 'totalSpeedingEvents')::int as total_speeding_events,
    (summary -> 'safety' ->> 'totalHarshBrakingEvents')::int as total_harsh_braking_events,

    (summary -> 'scorecard' ->> 'efficiencyScore')::numeric as efficiency_score,
    (summary -> 'scorecard' ->> 'qualityScore')::numeric as quality_score,
    (summary -> 'scorecard' ->> 'onTimeScore')::numeric as on_time_score,
    (summary -> 'scorecard' ->> 'overallScore')::numeric as overall_score
from summaries
