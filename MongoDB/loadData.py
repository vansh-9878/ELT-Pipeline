from pymongo import MongoClient
import json,os

client=MongoClient(os.getenv("MONGO_URI"))

db=client["chatbot"]

collection=db["synthetic_data"]
collection.delete_many({}) 
with open("merged_logistics.json","r",encoding="utf-8") as f:
    data=json.load(f)
try:
    result = collection.insert_many(data)
    print(f"✅ Inserted {len(result.inserted_ids)} documents.")
except Exception as e:
    print("❌ Insert failed:", e)

