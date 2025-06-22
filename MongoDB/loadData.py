from pymongo import MongoClient
import json, os
from pymongo.errors import DuplicateKeyError

client = MongoClient(os.getenv("MONGO_URI"))
db = client["chatbot"]
collection = db["synthetic_data"]

with open("merged_logistics.json", "r", encoding="utf-8") as f:
    data = json.load(f)

inserted_count = 0
skipped_count = 0

for doc in data:
    try:
        collection.insert_one(doc)
        inserted_count += 1
    except DuplicateKeyError:
        skipped_count += 1
    except Exception as e:
        print("❌ Unexpected error:", e)

print(f"✅ Inserted {inserted_count} documents.")
print(f"⚠️ Skipped {skipped_count} documents due to duplicate _id.")
