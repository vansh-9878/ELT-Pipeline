from pymongo import MongoClient
import os, json, time

print("🔗 Connecting to MongoDB...")
client = MongoClient(os.getenv("MONGO_URI"))

db = client["chatbot"]
collection = db["dsp_driver"]
print(f"📂 Using collection: {collection.full_name}")

print("📂 Loading JSON...")
with open("amazon_dsp_driver_dataset_200_multiweek 1.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(f"✅ Loaded {len(data)} records from file.")

print("📤 Inserting into MongoDB...")
result = collection.insert_many(data)
print(f"✅ Inserted {len(result.inserted_ids)} documents")

# Let the write settle
time.sleep(1)

# Confirm write
count = collection.count_documents({})
print(f"📊 Documents in collection now: {count}")
