import psycopg2
import json
import os
from psycopg2.extras import execute_batch
from dotenv import load_dotenv
load_dotenv()


conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
cursor = conn.cursor()

# cursor.execute("SELECT * FROM delivery_attempts")
# records = cursor.fetchall()
# print(records)

cursor.execute("DROP TABLE synthetic_data_airbyte_tmp CASCADE")

conn.commit()
print("✅ All data successfully migrated to PostgreSQL!")

cursor.close()
conn.close()