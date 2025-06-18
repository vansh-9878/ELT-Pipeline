import psycopg2
import json
import os
from psycopg2.extras import execute_batch
from dotenv import load_dotenv
load_dotenv()


conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
cursor = conn.cursor()

cursor.execute("SELECT data FROM data")
records = cursor.fetchall()
print("Started Loading data")



# Prepare batches
drivers_data = []
dsps_data = []
vehicles_data = []
devices_data = []
employments_data = []

# First loop: batch load top-level data
print("batch started")
for record in records:
    data = record[0]
    drivers_data.append((data["driverId"], data["name"]))

    dsp = data.get("dsp", {})
    dsps_data.append((dsp.get("dspId"), data["driverId"], dsp.get("name"), dsp.get("region")))

    vehicle = data.get("vehicle", {})
    vehicles_data.append((vehicle.get("vehicleId"), data["driverId"], vehicle.get("make"), vehicle.get("model"), vehicle.get("mileage")))

    device = data.get("device", {})
    devices_data.append((data["driverId"], device.get("model"), device.get("osVersion")))

    employment = data.get("employment", {})
    employments_data.append((data["driverId"], employment.get("hireDate"), employment.get("status")))

# Batch insert
execute_batch(cursor, """
    INSERT INTO drivers (driver_id, name) VALUES (%s, %s)
    ON CONFLICT (driver_id) DO NOTHING
""", drivers_data)

execute_batch(cursor, """
    INSERT INTO dsps (dsp_id, driver_id, name, region) VALUES (%s, %s, %s, %s)
    ON CONFLICT (dsp_id) DO NOTHING
""", dsps_data)

execute_batch(cursor, """
    INSERT INTO vehicles (vehicle_id, driver_id, make, model, mileage) VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (vehicle_id) DO NOTHING
""", vehicles_data)

print("halfway through..")

execute_batch(cursor, """
    INSERT INTO devices (driver_id, model, os_version) VALUES (%s, %s, %s)
    ON CONFLICT (driver_id) DO NOTHING
""", devices_data)

execute_batch(cursor, """
    INSERT INTO employments (driver_id, hire_date, status) VALUES (%s, %s, %s)
    ON CONFLICT (driver_id) DO NOTHING
""", employments_data)
print("batch ended")



conn.commit()
print("✅ All data successfully migrated to PostgreSQL!")

cursor.close()
conn.close()
