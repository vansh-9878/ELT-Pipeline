from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import psycopg2
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API"))

llm = genai.GenerativeModel('gemini-1.5-pro')
conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
cursor = conn.cursor()
pc = Pinecone(api_key=os.getenv("PINECONE_API"))
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


user_query = "Which drivers failed inspections last week?"
# user_query = "Get the average number of delivery attempts per stop for a company id company_1246"


def is_dynamic_sql(sql_text):
    response = llm.generate_content("""
    Is the following SQL query dynamic? A dynamic SQL contains placeholders like {{var_name}} or variables that need to be filled in.

    Respond with "Yes" or "No" only.

    SQL: """+ sql_text)
    return "yes" in response.text.lower()


def fill_dynamic_sql(sql_template, user_query):
    response = llm.generate_content(f"""
    The user asked: "{user_query}"
    You are given a dynamic SQL query: 
    {sql_template}

    Replace any placeholders (like {{ target_date }}) with appropriate values based on the user's request.
    Return only the final SQL query.
    """)
    return response.text.strip()


query_embedding = model.encode(user_query).tolist()
index = pc.Index("sql-retrieval")
res = index.query(vector=query_embedding, top_k=3, include_metadata=True)
print(res)
try:
    nlp=res['matches'][0]['metadata']['nlp']
    sql=res['matches'][0]['metadata']['sql']

    print(sql)
    if is_dynamic_sql(sql):
        result=fill_dynamic_sql(sql,user_query)
        result=result.replace("```sql","")
        result=result.replace("```","")
    else:
        result=sql
        

    cursor.execute(result)
    rows = cursor.fetchall()
    print("-"*100)
    for row in rows:
        print(row)
except Exception as e:
    print("Could not find query")
    print(e)

