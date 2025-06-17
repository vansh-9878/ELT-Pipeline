# nested_data_loader.py
import json
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
cursor = conn.cursor()

with open("nested_data.json") as f:
    nested_data = json.load(f)

CHUNK_SIZE = 50

for i in range(201, len(nested_data), CHUNK_SIZE):
    chunk = nested_data[i:i+CHUNK_SIZE]
    print(f"🚀 Processing chunk {i//CHUNK_SIZE + 1}...")
    count=1
    for entry in chunk:
        driver_id = entry["driverId"]
        week = entry["week"]

        cursor.execute("""
            INSERT INTO weekly_stats (driver_id, week_start, week_end)
            VALUES (%s, %s, %s) RETURNING id
        """, (driver_id, week["weekStart"], week["weekEnd"]))
        weekly_stat_id = cursor.fetchone()[0]

        for route in week.get("dailyRoutes", []):
            cursor.execute("""
                INSERT INTO daily_routes (weekly_stat_id, route_id, date, shift_start, shift_end, on_road_time_min, route_score, deliveries)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """, (
                weekly_stat_id,
                route.get("routeId"),
                route.get("date"),
                route.get("shiftStart"),
                route.get("shiftEnd"),
                route.get("onRoadTimeMin"),
                route.get("routeScore"),
                route.get("deliveries")
            ))
            daily_route_id = cursor.fetchone()[0]

            safety = route.get("safety", {})
            cursor.execute("""
                INSERT INTO daily_safety (daily_route_id, seat_belt_compliance_pct, speeding_events, harsh_braking_events)
                VALUES (%s, %s, %s, %s)
            """, (
                daily_route_id,
                safety.get("seatBeltCompliancePct"),
                safety.get("speedingEvents"),
                safety.get("harshBrakingEvents")
            ))

            for stop in route.get("stops", []):
                cursor.execute("""
                    INSERT INTO stops (daily_route_id, stop_number, address, lat, lon, delivered_count, attempts, scan_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                """, (
                    daily_route_id,
                    stop.get("stopNumber"),
                    stop.get("address"),
                    stop.get("coordinates", {}).get("lat"),
                    stop.get("coordinates", {}).get("lon"),
                    stop.get("deliveredCount"),
                    stop.get("attempts"),
                    stop.get("scanTime")
                ))
                stop_id = cursor.fetchone()[0]

                for package in stop.get("packages", []):
                    dim = package.get("dimensionsCm", {})
                    cursor.execute("""
                        INSERT INTO packages (stop_id, tracking_id, weight_kg, l, w, h, hazmat)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        stop_id,
                        package.get("trackingId"),
                        package.get("weightKg"),
                        dim.get("l"),
                        dim.get("w"),
                        dim.get("h"),
                        package.get("hazmat")
                    ))

        summary = week.get("summary", {})
        feedback = summary.get("customerFeedback", {})
        safety = summary.get("safety", {})
        scorecard = summary.get("scorecard", {})

        cursor.execute("""
            INSERT INTO weekly_summary (
                weekly_stat_id, total_stops, successful_deliveries, rescans, late_deliveries,
                feedback_positive, feedback_negative,
                avg_seat_belt_compliance_pct, total_speeding_events, total_harsh_braking_events,
                efficiency_score, quality_score, on_time_score, overall_score
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (  
            weekly_stat_id,
            summary.get("totalStops"),
            summary.get("successfulDeliveries"),
            summary.get("rescans"),
            summary.get("lateDeliveries"),
            feedback.get("positive"),
            feedback.get("negative"),
            safety.get("avgSeatBeltCompliancePct"),
            safety.get("totalSpeedingEvents"),
            safety.get("totalHarshBrakingEvents"),
            scorecard.get("efficiencyScore"),
            scorecard.get("qualityScore"),
            scorecard.get("onTimeScore"),
            scorecard.get("overallScore")
        ))
        print(f"done {count}")
        count+=1

    conn.commit()
    print(f"✅ Chunk {i//CHUNK_SIZE + 1} committed")

cursor.close()
conn.close()
print("🎉 All nested data inserted successfully!")



# nested_data_extractor.py
# import json
# import psycopg2
# import os
# from dotenv import load_dotenv
# load_dotenv()

# conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
# cursor = conn.cursor()

# cursor.execute("SELECT data FROM data")
# records = cursor.fetchall()

# output = []

# for record in records:
#     data = record[0]
#     for week in data.get("weeklyStats", []):
#         output.append({
#             "driverId": data["driverId"],
#             "week": week
#         })

# with open("nested_data.json", "w") as f:
#     json.dump(output, f, indent=2)

# cursor.close()
# conn.close()
# print("✅ Nested data extracted to 'nested_data.json'")
