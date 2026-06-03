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
from agent_PII_check import run_PII_check 
from agent_Cyber_Check import execute_cyber_checks
from search_knowledge_base import search_knowledge_base_records


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
filename = os.path.join(logs_directory_path, "agent_PII_check.log")
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


# def search_knowledge_base_records(input_query) -> str:
#     """
#     Fetch order details from Pinecone using Order ID.

#     Args:
#         input_query (str): User query containing Order ID
#         client: OpenAI client instance
#         index: Pinecone index instance

#     Returns:
#         str: JSON string response
#     """

#     try:

#         # =====================================================
#         # STEP 1 → APPEND REQUIRED DETAILS
#         # =====================================================

#         # input_query = (
#         #     input_query
#         #     + " provide data as product_id, "
#         #       "Order_Status, Shippment_Status, user_name as details"
#         # )
#         input_query = input_query
        
      
        
#         # =====================================================
#         # STEP 2 → DETECT SEARCH FIELD
#         # =====================================================

#         field_patterns = [
#             (r"(?:Order[_\s]?Id|order[_\s]?id)\s*[:=]\s*([A-Za-z0-9]+)", "Order_Id"),
#             (r"(?:Product[_\s]?Id|product[_\s]?id)\s*[:=]\s*([A-Za-z0-9]+)", "product_id"),
#             (r"(?:User[_\s]?Name|user[_\s]?name|Customer[_\s]?Name|customer[_\s]?name)\s*[:=]\s*([A-Za-z0-9\s]+)", "user_name"),
#         ]

#         filter_field = None
#         filter_value = None
#         print("Query ")
#         print(input_query)
        
#         for pattern, field_name in field_patterns:
#             match = re.search(pattern, input_query, re.IGNORECASE)
#             print (field_name)
#             print(match)
#             if match:
#                 filter_field = field_name
#                 filter_value = match.group(1).strip()
#                 break

#         if not filter_field:
#             print (order_match)            
#             order_match = re.search(r"\bO\d+\b", input_query)
#             if order_match:
#                 print(filter_field)
#                 filter_field = "Order_Id"
#                 filter_value = order_match.group(0)

#         if not filter_field:
#             return json.dumps({
#                 "status": "NOT_FOUND",
#                 "message": "No searchable field found. Use Order_Id, product_id, or user_name in the query.",
#             }, indent=4)

#         # =====================================================
#         # STEP 3 → CREATE EMBEDDING
#         # =====================================================

#         query_embedding = client.embeddings.create(
#             model="text-embedding-3-small",
#             input=input_query
#         ).data[0].embedding

#         # =====================================================
#         # STEP 4 → QUERY PINECONE
#         # =====================================================

#         results = index.query(
#             vector=query_embedding,
#             top_k=5,
#             include_metadata=True,
#             filter={
#                 filter_field: {
#                     "$eq": filter_value
#                 }
#             }
#         )

#         # =====================================================
#         # STEP 5 → FORMAT RESPONSE
#         # =====================================================

#         if results.matches:

#             response_list = []

#             for match in results.matches:

#                 metadata = match.metadata

#                 response = {
#                     "Order_Id": metadata.get("Order_Id"),
#                     "Customer_Name": metadata.get("user_name"),
#                     "Product_ID": metadata.get("product_id"),
#                     "Order_Status": metadata.get("Order_Status"),
#                     "Shipment_Status": metadata.get("Shippment_Status"),
                    
#                 }

#                 response_list.append(response)                
#             return json.dumps({
#                 "status": "SUCCESS",
#                 "total_records": len(response_list),
#                 "data": response_list
#             }, indent=4)
            
#         else:
         
#             return json.dumps({
#                 "status": "NOT_FOUND",
#                 "message": f"ORDER Information Not Found or Query is not order related. "
#             }, indent=4)

#     except Exception as e:

#         return json.dumps({
#             "status": "NOT_FOUND",
#             "message": str(e)
#         }, indent=4)


# =====================================================
# EXAMPLE USAGE
# =====================================================
def main() -> None:
    while True :
        user_input = input("\n User Please Submit your Query \n  : ")   
        query= user_input    
        
        ## Execute Cyber Attack Check 
        print("Calling Cyber ATTACK Check Agent")
        logging.info(f"Calling Cyber ATTACK Check for query {query}")
        query= user_input    
        final_cyber_check = execute_cyber_checks(query)
        print(final_cyber_check)
        logging.info(f"Cyber ATTACK  Result : {final_cyber_check}")
        
        
        
        


if __name__ == "__main__":
    main()
