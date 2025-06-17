from pymongo import MongoClient
import json,os
from schema import getSchema

client=MongoClient(os.getenv("MONGO_URI"))

db=client["chatbot"]

schema=getSchema()

collection_opts = {
    "validator": {"$jsonSchema": schema},
    "validationLevel": "strict",
    "validationAction": "error"
}

if "dsp_driver" not in db.list_collection_names():
    db.create_collection("dsp_driver", **collection_opts)

collection=db["dsp_driver"]

with open("amazon_dsp_driver_dataset_200_multiweek 1.json","r",encoding="utf-8") as f:
    data=json.load(f)
try:
    result = collection.insert_many(data)
    print(f"✅ Inserted {len(result.inserted_ids)} documents.")
except Exception as e:
    print("❌ Insert failed:", e)

    
