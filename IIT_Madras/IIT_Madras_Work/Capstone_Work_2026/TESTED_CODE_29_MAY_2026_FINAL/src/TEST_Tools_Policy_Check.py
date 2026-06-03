## Rajendra Bichu : Date : 29.04.2026 , Version 1.0

## This is to test the Tool Execution  Agent.


import pandas as pd
import uuid
from pinecone import Pinecone
from openai import OpenAI
from tqdm import tqdm
import re
import json
import os
import logging
import warnings
import json
from dotenv import load_dotenv, find_dotenv
from agent_execute_tools import run_tools_agent



# Find the .env file, searching upwards in the directory tree
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Now you can access environment variables
print(f"Path to .env file: {dotenv_path}")

# =====================================================

##Logging

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
logs_directory_path = os.path.join(parent_directory, "logs")
os.makedirs(logs_directory_path, exist_ok=True)

## Enable logging to a file with INFO level and a specific format
filename = os.path.join(logs_directory_path, "agent_Policy_Execution_LOG.log") 

print("Logs File Name Path: ", filename)

logging.basicConfig(
    filename=filename,
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True,  # Force reconfiguration to ensure the new filename is used
    
)


# =====================================================
# CONFIGURATION
# =====================================================

# PINECONE_API_KEY = "YOUR_PINECONE_API_KEY"
# OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"



# =====================================================
# INITIALIZE CLIENTS
# =====================================================
openai_api_key = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=openai_api_key)




# =====================================================
# EXAMPLE USAGE
# =====================================================
def main() -> None:
    while True :
        user_input = input("\n User Please Submit your Query \n  : ")   
        query= user_input             
  
        print("Calling the Tool Execution  Agent")
        logging.info(f"Calling Tool Execution  Agent Now for query {query}")
        query= user_input    
        tools_execution_response = run_tools_agent(query)
        print(tools_execution_response)
        logging.info(f"Tool Execution  Check  Result : {tools_execution_response}")
        


if __name__ == "__main__":
    main()
