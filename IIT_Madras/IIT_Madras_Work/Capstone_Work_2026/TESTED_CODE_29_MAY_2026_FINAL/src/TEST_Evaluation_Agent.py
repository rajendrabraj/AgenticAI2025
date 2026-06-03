## Rajendra Bichu : Date : 29.04.2026 , Version 1.0

## This is to test the evaluation Agent.


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
from agent_evaluation import run_evaluation_agent



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
filename = os.path.join(logs_directory_path, "agent_evaluation_LOG.log") 

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
# EXAMPLE USAGE
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
        print(f"Response String CLEAN  #1  :  {clean_output} " )
        print("\n") 
        
        # Convert to CLEAN single-line JSON string
        #clean_output = json.dumps(response_json, separators=(",", ":"))
        final_clean_output = json.dumps(clean_json)   
        print("\n")         
        print(f"Response String CLEAN  # 2 :  {final_clean_output} " )
        print("\n") 
        
        # Log JSON without \n characters (use safe f-string to avoid percent-formatting issues)
        logging.info(f"Evaluation : Search KnowledgeBase Response : {final_clean_output}")
              
        #logging.info("Evaluation : Search KnowledgeBase Response : %s", json.dumps(clean_output, indent=4))
            
        #Convert JSON object to JSON string
        response_string = json.dumps(response_json, indent=4)            
        print(response_string)              
        ## Execute and run the PII Agent now
        print("Calling the Evaluation Agent")
        logging.info(f"Calling Evaluation Agent Now for query {query}")
        query= user_input    
        final_Evaluation_response = run_evaluation_agent(query,response_string)
        print(final_Evaluation_response)
        logging.info(f"Evaluation Check  Result : {final_Evaluation_response}")
        


if __name__ == "__main__":
    main()
