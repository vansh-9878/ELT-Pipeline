import json
import random
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

fake = Faker()

NUM_COMPANIES = 100
NUM_VEHICLES_PER_COMPANY = 5
NUM_DRIVERS_PER_COMPANY = 5
NUM_ZONES = 15
NUM_STOPS = 70
NUM_INSPECTIONS = 40

output_dir = Path("synthetic_data")
output_dir.mkdir(exist_ok=True)


item_definitions = {
    "Brakes": [
        {"code": "BRK01", "description": "Brake pad wear"},
        {"code": "BRK02", "description": "Low brake fluid level"}
    ],
    "Lights": [
        {"code": "LGT01", "description": "Left headlight out"},
        {"code": "LGT02", "description": "Right taillight malfunction"}
    ],
    "Tires": [
        {"code": "TIR01", "description": "Tire tread below limit"},
        {"code": "TIR02", "description": "Tire pressure imbalance"}
    ],
    "Wipers": [
        {"code": "WPR01", "description": "Wiper blade damage"},
        {"code": "WPR02", "description": "Wipers leave streaks"}
    ],
    "Horn": [
        {"code": "HRN01", "description": "Horn non-functional"}
    ],
    "Mirrors": [
        {"code": "MRR01", "description": "Cracked mirror"},
        {"code": "MRR02", "description": "Loose mirror housing"}
    ]
}

# Notes for pass/fail
pass_notes = {
    "Brakes": "Brakes working normally, no issues found",
    "Lights": "All lights functional",
    "Tires": "Tires in good condition, pressure is optimal",
    "Wipers": "Wipers operate smoothly with no streaks",
    "Horn": "Horn sounds correctly",
    "Mirrors": "Mirrors properly adjusted and intact"
}

fail_notes = {
    "Brakes": "Brake performance poor, squealing noted",
    "Lights": "One or more lights not working",
    "Tires": "Uneven wear detected, pressure low",
    "Wipers": "Blades worn out, streaking visible",
    "Horn": "Horn not sounding when pressed",
    "Mirrors": "Cracks or instability in one or more mirrors"
}


def generate_drivers(company_id, count, start_index=0):
    drivers = []
    for i in range(start_index, start_index + count):
        driver_id = f"drv_{5000 + i}"
        drivers.append({
            "_id": driver_id,
            "name": fake.name(),
            "license": {
                "class": random.choice(["Class A", "Class B", "Class C"]),
                "expiry": fake.date_between(start_date="+1y", end_date="+3y").isoformat()
            },
            "certifications": [
                {
                    "type": random.choice(["Safety", "Hazmat"]),
                    "levels": random.sample(["Basic", "Advanced", "Expert"], k=random.randint(1, 2))
                }
            ],
            "weekly_schedule": [
                {
                    "day": day,
                    "shifts": [{"start": "08:00", "end": "16:00"}]
                } for day in random.sample(["Mon", "Tue", "Wed", "Thu", "Fri"], k=3)
            ]
        })
    return drivers

def generate_zones(count):
    zones = []
    for i in range(count):
        zone_id = f"zone_{chr(65+i)}"
        zones.append({
            "_id": zone_id,
            "name": f"{fake.city()} Zone",
            "boundaries": [[
                {"lat": float(fake.latitude()), "lng": float(fake.longitude())},
                {"lat": float(fake.latitude()), "lng": float(fake.longitude())},
                {"lat": float(fake.latitude()), "lng": float(fake.longitude())}
            ]],
            "subzones": [
                {"id": f"{zone_id}_1", "name": f"{fake.word().capitalize()} Subzone"}
            ]
        })
    return zones

def generate_stops(count):
    stops = []
    for i in range(count):
        stop_id = f"stop_{i+1}"
        stops.append({
            "_id": stop_id,
            "package_id": f"pkg_{200+i}",
            "address": fake.address().replace("\n", ", "),
            "events": [
                {"type": "arrival", "ts": fake.date_time_this_year().isoformat()},
                {
                "type": "delivery_attempts",
                "attempts": [
                    {
                        "ts": fake.date_time_this_year().isoformat(),
                        "status": "Delivered" if random.random() > 0.4 else "Exception",
                        "exception":  {
                            "code": None if random.random() > 0.4 else "NO_ACCESS",
                            "reason": None if random.random() > 0.4 else "Gate locked"
                        }
                    }
                ]
            }
            ],
            "customer_callbacks": [
                {
                    "callback_ts": fake.date_time_this_year().isoformat(),
                    "issues": [{"type": "missing_item", "detail": "Wrong SKU"}]
                }
            ] if random.random() > 0.5 else []
        })
    return stops

def generate_vehicles(company_id, driver_ids, stop_ids, start_index=0):
    vehicles = []
    for i in range(start_index, start_index + NUM_VEHICLES_PER_COMPANY):
        veh_id = f"veh_{1000 + i}"
        assignments = []
        if random.random() > 0.3:
            assignments.append({
                "route_id": f"rte_{9000+i}",
                "start_date": fake.date_this_year().isoformat(),
                "details": {
                    "planned_stops": random.sample(stop_ids, k=min(2, len(stop_ids))),
                    "backup_vehicles": []
                }
            })
        vehicles.append({
            "_id": veh_id,
            "company_id": company_id,
            "type": random.choice(["Van", "Truck"]),
            "capacity_packages": random.randint(100, 500),
            "maintenance_logs": [
                {
                    "service_date": fake.date_this_year().isoformat(),
                    "details": {
                        "km_reading": random.randint(10000, 80000),
                        "tasks": [
                            {"task": "Oil Change", "cost": random.randint(50, 150)},
                            {"task": "Brake Inspection", "cost": random.randint(50, 120)}
                        ]
                    }
                }
            ],
            "sensor_streams": [
                {
                    "stream_type": "gps",
                    "points": [[
                        {
                            "ts": fake.date_time_this_year().isoformat(),
                            "lat": float(fake.latitude()),
                            "lng": float(fake.longitude())
                        }
                        for _ in range(2)
                    ]]
                }
            ],
            "current_assignments": assignments
        })
    return vehicles

def generate_inspections(vehicle_ids, count):
    inspections = []
    for i in range(count):
        checklist = []
        issues_found = []

        for item, issues in item_definitions.items():
            status = random.choice(["Pass", "Fail"])
            entry = {
                "item": item,
                "status": status,
                "notes": pass_notes[item] if status == "Pass" else fail_notes[item]
            }

            checklist.append(entry)
            if status == "Fail":
                selected_issue = random.choice(issues)
                issues_found.append(selected_issue)
        inspections.append({
            "_id": f"insp_{1000+i}",
            "date": fake.date_this_year().isoformat(),
            "inspector": {
                "id": f"emp_{200+i}",
                "name": fake.name()
            },
            "vehicle_id": random.choice(vehicle_ids),
            "checklist":checklist,
            "issues_found": issues_found
        })
    return inspections

# Step 1: Generate shared zones and stops
zones = generate_zones(NUM_ZONES)
stops = generate_stops(NUM_STOPS)

# Step 2: Per-company generation
logistics_companies = []
drivers = []
vehicles = []

for i in range(NUM_COMPANIES):
    company_id = f"company_{random.randint(100,9999)}"
    start_driver_index = i * NUM_DRIVERS_PER_COMPANY
    start_vehicle_index = i * NUM_VEHICLES_PER_COMPANY

    # Generate drivers and vehicles for this company
    company_drivers = generate_drivers(company_id, NUM_DRIVERS_PER_COMPANY, start_driver_index)
    company_vehicles = generate_vehicles(
        company_id,
        [d["_id"] for d in company_drivers],
        [s["_id"] for s in stops],
        start_vehicle_index
    )

    drivers.extend(company_drivers)
    vehicles.extend(company_vehicles)

    # Create the company object
    logistics_companies.append({
        "_id": company_id,
        "name": fake.company(),
        "region": fake.state(),
        "fleet": [v["_id"] for v in company_vehicles],
        "drivers": [d["_id"] for d in company_drivers],
        "active_zones": random.sample([z["_id"] for z in zones], k=2)
    })
    print("Generated vehicles with company_id:")
    for v in vehicles:
        print(v["_id"], "->", v["company_id"])

# Step 3: Generate inspections across all vehicles
inspections = generate_inspections([v["_id"] for v in vehicles], NUM_INSPECTIONS)

# Step 4: Save to JSON files
json_outputs = {
    "drivers.json": drivers,
    "zones.json": zones,
    "stops.json": stops,
    "vehicles.json": vehicles,
    "inspections.json": inspections,
    "logistics_companies.json": logistics_companies
}

for filename, content in json_outputs.items():
    with open(output_dir / filename, 'w') as f:
        json.dump(content, f, indent=2)

print(f"✅ Synthetic data generated in: {output_dir.resolve()}")
