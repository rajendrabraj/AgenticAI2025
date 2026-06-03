import pandas as pd
import uuid
from pinecone import Pinecone
from openai import OpenAI
from tqdm import tqdm

import os
import logging
import warnings
import json
from dotenv import load_dotenv, find_dotenv
from search_knowledge_base import search_knowledge_base_records
from agent_multi_agent import execute_multi_agent_check

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
filename = os.path.join(logs_directory_path, "agent_multi_agent.log")
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


EMBEDDING_MODEL = "text-embedding-3-small"
PINECONE_INDEX_NAME = "orderproductdata"

pinecone_api_key = os.getenv("PINECONE_API_KEY", "") or os.getenv("PINE_CONE_API_KEY", "")
openai_api_key = os.getenv("OPENAI_API_KEY", "")
index_name = os.getenv("PINECONE_INDEX_NAME", "orderproductdata")
#index_host = os.getenv("PINECONE_INDEX_HOST", "")

pinecone_environment = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
#vector_dimension = int(os.getenv("PINECONE_VECTOR_DIMENSION", "1536"))
vector_dimension= int("1536")  # For OpenAI's text-embedding-3-small model

print(f"PINECONE_API_KEY: {'SET' if pinecone_api_key else 'MISSING'}")
print(f"OPENAI_API_KEY: {'SET' if openai_api_key else 'MISSING'}")
print(f"PINECONE_INDEX_NAME: {index_name}")
#print(f"PINECONE_INDEX_HOST: {'SET' if index_host else 'MISSING'}")
print(f"PINECONE_ENVIRONMENT: {pinecone_environment}")


script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
data_directory_path = os.path.join(parent_directory, "data")
print(f"Data directory path: {data_directory_path}")


# =====================================================
# INITIALIZE CLIENTS
# =====================================================

pc = Pinecone(api_key=pinecone_api_key)
#index = pc.Index(PINECONE_INDEX_NAME)
index = pc.Index(index_name)




openai_api_key = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=openai_api_key)


# # =====================================================
# # CREATE TEXT FOR EMBEDDING
# # =====================================================

batch_size = 100
vectors = []


print("Querying  embeddings and data from Pinecone...")

print("\n")

# =====================================================
# EXACT ORDER LOOKUP + SEMANTIC SEARCH
# =====================================================

import re
import json


# =====================================================
# Test of the Agent 
# =====================================================
def main() -> None:
    while True :
        user_input = input("\n User Please Submit your Query \n  : ")   
        query= user_input    
        response_json = search_knowledge_base_records(input_query=query)
        print("JSON Search Output")         
        # print("\n")        
        print(response_json)
        # print("\n")   
        clean_json = json.loads(response_json)
        clean_output = json.dumps(clean_json)        
        print("\n")         
        print(f"Response String CLEAN  :  {clean_output} " )
        print("\n") 
       
       
        logging.info("Multi Agent Check Search KnowledgeBase Response : %s", json.dumps(clean_output, indent=4))
      
            
        ## Execute and run the Multi Agent Check now
        print("Calling the Multi Agent Check for Cyber Threat or PII check")
        logging.info(f"Multi Agent Check  Now for Cyber Threat or PII check for query {query}")
        query= user_input    
        final_multi_agent_response = execute_multi_agent_check(query)
        print(final_multi_agent_response)
        logging.info(f"Multi Agent  Result : {final_multi_agent_response}")        
        

if __name__ == "__main__":
    main()
