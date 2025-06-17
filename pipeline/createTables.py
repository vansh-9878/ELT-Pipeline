import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
cur = conn.cursor()



cur.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
    driver_id TEXT PRIMARY KEY,
    name TEXT
);
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS dsps (
    dsp_id TEXT PRIMARY KEY,
    driver_id TEXT REFERENCES drivers(driver_id),
    name TEXT,
    region TEXT
);
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id TEXT PRIMARY KEY,
    driver_id TEXT REFERENCES drivers(driver_id),
    make TEXT,
    model TEXT,
    mileage INT
);
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS devices (
    driver_id TEXT PRIMARY KEY REFERENCES drivers(driver_id),
    model TEXT,
    os_version TEXT
);
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS employments (
    driver_id TEXT PRIMARY KEY REFERENCES drivers(driver_id),
    hire_date TIMESTAMPTZ,
    status TEXT CHECK (status IN ('active', 'on-leave', 'terminated', 'cancelled'))
);
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS weekly_stats (
    id SERIAL PRIMARY KEY,
    driver_id TEXT REFERENCES drivers(driver_id),
    week_start TIMESTAMPTZ,
    week_end TIMESTAMPTZ
);
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_routes (
    id SERIAL PRIMARY KEY,
    weekly_stat_id INT REFERENCES weekly_stats(id),
    route_id TEXT,
    date TIMESTAMPTZ,
    shift_start TEXT,
    shift_end TEXT,
    on_road_time_min INT,
    route_score DOUBLE PRECISION,
    deliveries INT
);
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS stops (
    id SERIAL PRIMARY KEY,
    daily_route_id INT REFERENCES daily_routes(id),
    stop_number INT,
    address TEXT,
    lat DOUBLE PRECISION,
    lon DOUBLE PRECISION,
    delivered_count INT,
    attempts INT,
    scan_time TEXT
);

""")


cur.execute("""
    DROP TABLE packages;
    CREATE TABLE packages (
    id SERIAL PRIMARY KEY,
    stop_id INT REFERENCES stops(id),
    tracking_id TEXT,
    weight_kg DOUBLE PRECISION,
    l INT,
    w INT,
    h INT,
    hazmat BOOLEAN
);

""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_safety (
    daily_route_id INT PRIMARY KEY REFERENCES daily_routes(id),
    seat_belt_compliance_pct DOUBLE PRECISION,
    speeding_events INT,
    harsh_braking_events INT
);


""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS weekly_summary (
    weekly_stat_id INT PRIMARY KEY REFERENCES weekly_stats(id),
    total_stops INT,
    successful_deliveries INT,
    rescans INT,
    late_deliveries INT,
    feedback_positive INT,
    feedback_negative INT,
    avg_seat_belt_compliance_pct DOUBLE PRECISION,
    total_speeding_events INT,
    total_harsh_braking_events INT,
    efficiency_score INT,
    quality_score INT,
    on_time_score INT,
    overall_score DOUBLE PRECISION
);

""")



conn.commit()
cur.close()
conn.close()
