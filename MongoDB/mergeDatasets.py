import json
from pathlib import Path
from collections import defaultdict

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def mergeIntoOne():
    files = {
    "drivers": "./synthetic_data/drivers.json",
    "inspections": "./synthetic_data/inspections.json",
    "logistics_companies": "./synthetic_data/logistics_companies.json",
    "stops": "./synthetic_data/stops.json",
    "vehicles": "./synthetic_data/vehicles.json",
    "zones": "./synthetic_data/zones.json"
}

    data = {key: load_json(path) for key, path in files.items()}

    drivers_by_id = {d["_id"]: d for d in data["drivers"]}
    vehicles_by_id = {v["_id"]: v for v in data["vehicles"]}
    zones_by_id = {z["_id"]: z for z in data["zones"]}
    stops_by_id = {s["_id"]: s for s in data["stops"]}

    inspections_by_vehicle = defaultdict(list)
    for insp in data["inspections"]:
        inspections_by_vehicle[insp["vehicle_id"]].append(insp)

    merged_companies = []

    for company in data["logistics_companies"]:
        company_drivers = [drivers_by_id[drv_id] for drv_id in company["drivers"] if drv_id in drivers_by_id]
    
        company_zones = [zones_by_id[zone_id] for zone_id in company["active_zones"] if zone_id in zones_by_id]
    
        company_vehicles = []
        for veh_id in company["fleet"]:
            if veh_id not in vehicles_by_id:
                continue
            vehicle = vehicles_by_id[veh_id].copy()
        
            vehicle["inspections"] = inspections_by_vehicle.get(veh_id, [])

            for assignment in vehicle.get("current_assignments", []):
                if "details" in assignment and "planned_stops" in assignment["details"]:
                    assignment["details"]["planned_stops_full"] = [
                    stops_by_id[stop_id] for stop_id in assignment["details"]["planned_stops"]
                    if stop_id in stops_by_id
                ]

            company_vehicles.append(vehicle)

        merged_companies.append({
        **company,
        "drivers": company_drivers,
        "fleet": company_vehicles,
        "active_zones": company_zones
    })

    output_path = "merged_logistics.json"
    with open(output_path, 'w') as f:
        json.dump(merged_companies, f, indent=2)

    print(f"Merged JSON written to {output_path}")


