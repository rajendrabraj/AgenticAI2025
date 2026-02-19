from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()

conn = sql.connect(
    server_hostname=os.getenv("DATABRICKS_HOSTNAME"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    access_token=os.getenv("DATABRICKS_TOKEN")
)

cursor = conn.cursor()
cursor.execute("SELECT 1")
print(cursor.fetchall())

cursor.close()
conn.close()

print("✅ Databricks connection successful!")
