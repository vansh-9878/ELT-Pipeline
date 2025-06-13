import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("HOST"),
    database="postgres",
    user="postgres",
    password=os.getenv("SQL"),
    port=os.getenv("PORT"),
    sslmode="require"  
)

cursor = conn.cursor()

cursor.execute("SELECT version();")
print("Connected to:", cursor.fetchone())

cursor.close()
conn.close()
