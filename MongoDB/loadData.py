from pymongo import MongoClient
import json,os

client=MongoClient(os.getenv("MONGO_URI"))

db=client["chatbot"]
collection=db["data"]

with open("amazon_dsp_driver_dataset_200_multiweek 1.json","r",encoding="utf-8") as f:
    data=json.load(f)
    
# collection.insert_many(data)
result = collection.insert_many(data)
print("Inserted IDs:", result.inserted_ids)
