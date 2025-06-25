import os
import glob
import json
import uuid
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API"))

model = genai.GenerativeModel('gemini-1.5-pro')

embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

pc = Pinecone(api_key=os.getenv("PINECONE_API"))
index = pc.Index("sql-retrieval2")

# sql_files = glob.glob("./DataBuildTool/project/models/**/*.sql", recursive=True) 
files=glob.glob("./DataBuildTool/project/models/metric/*.sql", recursive=True) 
count=0
for path in files:
    print(path)
    # if "fct_route_performance" not in path:
    #     continue
    with open(path, "r", encoding="utf-8") as f:
        raw_sql = f.read().strip()
        # print(raw_sql)
        # print("-"*100)

    count+=1
    try:
        print("hi")
        # result = model.generate_content("""
        # You are an AI Assistant that generates sql queries and its corresponding nlp descriptions
        # You have been given a dbt model, you have you create different sql queries and their nlp descriptions using that model
        # - use different aggregates
        # - you are given file name and the query in it, file name is the table name to be called
        # - return only a list of objects with the following structure :
        #         list=[
        #             {
        #                 "nlp" : description what the sql fetches
        #                 "sql" : actual sql query
        #             }
        #         ]
        # - dont return anything else other than the list
        # - dont create a python function
        #                                 """+path.split("metric")[1]+raw_sql)
        result = model.generate_content("""
        You are an AI Assistant tasked with generating only **dynamic SQL queries** and their corresponding **natural language (NLP) descriptions** based on a provided dbt model.

            You will receive:
            - The **file name**, which represents the name of the dbt model/table.
            - The **SQL code** defined in that model file.

            Your objective:
            - Create a variety of **dynamic SQL queries** using the structure and fields of the model.
            - Use **different SQL aggregations**, filters, groupings, and conditions.
            - Ensure queries include **placeholders** (e.g., `{{ target_date }}`, `{{ vehicle_id }}`) to make them dynamic and adaptable.
            - All queries should assume that the table name equals the **file name** (without extension).

            Output format:
            - Return ONLY a list of JSON objects in the following exact structure (do not include Python code or any extra explanation):

            ```json
            list = [
                {
                    "nlp": "Brief description of what the SQL query fetches using simple natural language.",
                    "sql": "The dynamic SQL query using the dbt model table."
                },
                ...
            ]"""+path.split("metric")[1]+raw_sql)
        
        print("wow")
        json_str=result.text.split("```")[1].split("json")[1].strip()
        query_list = json.loads(json_str)
        # print(query_list)
        
        for query in query_list:
            try:
                embedding = embedder.encode(query['nlp']).tolist()  
                index.upsert([
                    (
                        str(uuid.uuid4()),         
                        embedding,                 
                        {                          
                            "nlp": query['nlp'],
                            "sql": query['sql']
                        }
                    )
                ])
            except Exception as e:
                print("Embedding/Upsert error:", e)

        print("donee")
        # print(f"✅ Enriched & inserted: {path}")
    except Exception as e:
        print(f"❌ Error with {path}:", e)
