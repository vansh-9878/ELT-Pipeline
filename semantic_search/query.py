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

conn.autocommit=True


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
    examples : 
        - companyId : company_1246
        - vehicleId : veh_1280
    Return only the final SQL query.
    """)
    return response.text.strip()


def searchDatabase(user_query):
    query_embedding = model.encode(user_query).tolist()
    index = pc.Index("sql-retrieval2")
    res = index.query(vector=query_embedding, top_k=3, include_metadata=True)

    try:
        nlp = None
        sql = None
        print(res['matches'])
        for match in res['matches']:
            metadata = match.get('metadata', {})
            if 'nlp' in metadata and 'sql' in metadata:
                nlp = metadata['nlp']
                sql = metadata['sql']
                break

        if not sql:
            raise ValueError("No valid match with 'nlp' and 'sql' found.")

        if is_dynamic_sql(sql):
            result = fill_dynamic_sql(sql, user_query)
            result = result.replace("```sql", "").replace("```", "")
        else:
            result = sql

        cursor.execute(result)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

# Combine each row with column names
        results_with_headers = [dict(zip(column_names, row)) for row in rows]
        # for row in rows:
        #     print(row)
        return results_with_headers

    except Exception as e:
        print("Could not find query")
        print(e)
        return []


# user_query = "Which drivers failed inspections last week?"
user_query = "get me number of failed deliveries in the past week for company company_1246"
user_query = "Shows the earliest and latest route start dates for each company."

# searchDatabase(user_query)
