
## Rajendra Bichu : Date : 15.05.2026 , Version 1.0

## Customer Support — AI Support Resolution Agent

## This program is to test using the FAST_API and execution calls.
## This program will ensure that the FAST API is working and we can call the API from the ChatBOT and respective results are logged in the file.
## This program uses the search_knowledge_base_records function to get the results from the knowledge base and logs the results in the file.

## Launch it using : uvicorn src.app:app --reload --host 127.0.0.1 --port 8002
## Executed and TESTED using the CURL commands in a batch file. 


import os
import sys
import logging
import warnings
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import uvicorn
import json
from datetime import datetime

## Call the knowledge base function to get the results and log the results in the file.

from .search_knowledge_base import search_knowledge_base_records


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

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
logs_directory_path = os.path.join(parent_directory, "logs")
os.makedirs(logs_directory_path, exist_ok=True)
file_name = os.path.join(logs_directory_path, "Agent_execution_ChatBOT_LOG.log")

#OUTPUT_FILE = os.path.join(logs_directory_path, "FAST_API_OUTPUT.txt")

OUTPUT_FILE = os.path.join(logs_directory_path, "AI_CHATBOT_OUTPUT.txt")


def append_to_chatbot_file_string(response_string):
    # Handle CrewOutput objects by extracting raw output
    if hasattr(response_string, 'raw'):
        response_text = response_string.raw
    else:
        response_text = str(response_string)

    file = open(OUTPUT_FILE, "a", encoding="utf-8")

    file.write(response_text + "\n\n")

    file.close()

    return "SUCCESS"


## FAST API app object

app = FastAPI()

## FAST API endpoint to handle support queries

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
    
    response_json = search_knowledge_base_records(query)       
    print(response_json)
    
    response_string = json.dumps(result, indent=4)            
    print(response_string)   
    print(response_json)
    clean_json = json.loads(response_json)
    final_clean_output = json.dumps(clean_json)        
  
    #clean_output = json.dumps(response_json, separators=(",", ":"))
    final_clean_output = json.dumps(clean_json)   
    # print("\n")         
    # print(f"Response String CLEAN  # 2 :  {final_clean_output} " )
    # print("\n")     
            
     ## Copy the results to  
    start_time = str(datetime.now())        
    lstr_plain_string = start_time +  " FAST API CHATBOT File Logging :  QUERY Executed (using FAST API)   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "FAST API CHATBOT Logging : RESULTS OF Knowledge Base Results(using FAST API)"
    append_to_chatbot_file_string(lstr_plain_string)    
    append_to_chatbot_file_string(final_clean_output)      
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)        
    result= final_clean_output

    return {
        "status": "SUCCESS",
        "response": result
    }
    




if __name__ == "__main__":
    # Prefer to run uvicorn with an import string so reload/workers work.
    candidates = ["src.app", "app"]
    selected_module = None
    import importlib
    for name in candidates:
        try:
            importlib.import_module(name)
            selected_module = name
            break
        except Exception:
            continue

    if selected_module:
        uvicorn.run(
            f"{selected_module}:app",
            host="127.0.0.1",
            port=8002,
            reload=True,
        )
    else:
        logging.warning(
            "FAST API: No importable module name found for reload; running app object without reload."
        )
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8002,
            reload=False,
        )
    