import psycopg2,os
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta
load_dotenv()



def newRecord(vehicle_id, address, date_str):
    conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
    cur = conn.cursor()
    event_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    route_id = f"rte_{random.randint(1000, 9999)}"
    package_id = f"pkg_{random.randint(200, 999)}"
    event = random.choice(['arrival', 'departure'])

    random_time = timedelta(
    hours=random.randint(0, 23),
    minutes=random.randint(0, 59),
    seconds=random.randint(0, 59)
)
    timestamp = datetime.combine(event_date, datetime.min.time()) + random_time


    cur.execute("""
    SELECT stop_id FROM stops WHERE address = %s LIMIT 1
""", (address,))
    row = cur.fetchone()

    if row:
        stop_id = row[0]
    else:
        stop_id = f"stop_{random.randint(100, 999)}"

    cur.execute("""
    INSERT INTO stops (vehicle_id, route_id, stop_id, package_id, address, event, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (vehicle_id, route_id, stop_id, package_id, address, event, timestamp))

    conn.commit()
    cur.close()
    conn.close()

    print("Row inserted successfully.")

vehicle_id = 'veh_1415'
address = '31818 Andrea Valleys Apt. 646, South Abigail, WA 72153'
date_str = '2025-06-24'

# newRecord(vehicle_id, address, date_str)
