## databricks_client.py

import os
import json
import time
import logging
from databricks import sql
from dotenv import load_dotenv

load_dotenv()


#AppLog File Path

logfile_name= "C:\\Rajendra_2015\\AgenticAI_Programs\\Agentic_Batch2\\2-Langchain Basics\\11_IIT_Madras\\1_0_My_DataBricks_Assignment\\databricks_json_app\\logs\\app.log"


logging.basicConfig(
    filename=logfile_name,
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)


def connect_to_databricks():
    try:
        conn = sql.connect(
            server_hostname=os.getenv("DATABRICKS_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        logging.info("Connected to Databricks successfully")
        return conn
    except Exception as e:
        logging.exception("Databricks connection failed")
        raise e


def execute_query(query: str) -> dict:
    conn = None
    cursor = None

    try:
        conn = connect_to_databricks()
        cursor = conn.cursor()

        start_time = time.time()
        cursor.execute(query)

        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        end_time = time.time()

        execution_time_ms = round((end_time - start_time) * 1000, 2)

        result = {
            "execution_time_ms": execution_time_ms,
            "columns": columns,
            "record_count": len(rows),
            "records": [dict(zip(columns, row)) for row in rows]
        }

        logging.info(f"Query executed in {execution_time_ms} ms")

        return result

    except Exception as e:
        logging.exception("Query execution failed")
        raise e

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
