## Rajendra Bichu : Date : 15.05.2026 , Version 1.0

## Customer Support — AI Support Resolution Agent

## This program is to test using the FAST_API and execution calls.


import os
import sys
import logging
import warnings
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import uvicorn


# Ensure the parent src folder is importable when this file is executed from elsewhere.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


from search_knowledge_base import search_knowledge_base_records
from agent_escalation import run_escalate_agent

from loguru import logger
import pinecone
import time
import traceback

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
logs_directory_path = os.path.join(parent_directory, "logs")
os.makedirs(logs_directory_path, exist_ok=True)

file_name = os.path.join(logs_directory_path, "FAST_API_Execution.log") 

logging.basicConfig(
    filename=file_name,
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True
)



app = FastAPI()


@app.post("/support")
def support_endpoint(request: dict):

    query = request.get("query")

    logging.info(
        f"START - FAST API /support called with query: {query}"
    )

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query missing"
        )

    result = search_knowledge_base_records(query)

    return {
        "status": "SUCCESS",
        "response": result
    }
    


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8002)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8002,
        reload=True
    )
    