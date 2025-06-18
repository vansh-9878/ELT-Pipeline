with weekly as (
    select
        driver_id,
        week_start,
        week_end,
        avg_seat_belt_compliance_pct,
        total_speeding_events,
        total_harsh_braking_events
    from {{ ref('stg_weekly_summary') }}
),

daily as (
    select
        driver_id,
        route_id,
        seat_belt_compliance_pct,
        speeding_events,
        harsh_braking_events
    from {{ ref('stg_daily_safety') }}
),

summary as (
    select
        w.driver_id,
        w.week_start,
        w.week_end,

        w.avg_seat_belt_compliance_pct,
        w.total_speeding_events,
        w.total_harsh_braking_events,

        avg(d.seat_belt_compliance_pct) as avg_daily_seatbelt_pct,
        sum(d.speeding_events) as total_daily_speeding_events,
        sum(d.harsh_braking_events) as total_daily_harsh_braking_events,

        count(d.route_id) as route_days
    from weekly w
    left join daily d
        on w.driver_id = d.driver_id
    group by w.driver_id, w.week_start, w.week_end,
             w.avg_seat_belt_compliance_pct, w.total_speeding_events, w.total_harsh_braking_events
)

select * from summary
