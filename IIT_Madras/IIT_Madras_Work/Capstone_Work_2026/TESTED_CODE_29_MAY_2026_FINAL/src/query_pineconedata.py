import pandas as pd
import uuid
from pinecone import Pinecone
from openai import OpenAI
from tqdm import tqdm

import os
import logging
import warnings
from dotenv import load_dotenv, find_dotenv

# Find the .env file, searching upwards in the directory tree
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Now you can access environment variables
print(f"Path to .env file: {dotenv_path}")


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

input_query = """
    give me order status for order id 'Order_Id= O002' 

"""
input_query = input_query + " ,  provide data as product_id, Order_Status, Shippment_Status ,user_name as details"

# =====================================================
# STEP 1 → EXTRACT ORDER ID
# =====================================================

order_match = re.search(r"O\d+", input_query)

order_id = order_match.group(0) if order_match else None

print(f"Extracted Order ID: {order_id}")

# =====================================================
# STEP 2 → CREATE EMBEDDING
# =====================================================

query_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=input_query
).data[0].embedding

# =====================================================
# STEP 3 → QUERY PINECONE WITH FILTER
# =====================================================

results = index.query(
    vector=query_embedding,

    top_k=5,

    include_metadata=True,

    # IMPORTANT:
    # Exact metadata filtering
    filter={
        "Order_Id": {
            "$eq": order_id
        }
    }
)

# =====================================================
# STEP 4 → FORMAT CLEAN RESPONSE
# =====================================================

if results.matches:

    for match in results.matches:

        metadata = match.metadata

        response = {
            "Order_Id": metadata.get("Order_Id"),
            "User_Name": metadata.get("user_name"),
            "Product_ID": metadata.get("product_id"),
            "Order_Status": metadata.get("Order_Status"),
            "Shipment_Status": metadata.get("Shippment_Status"),
            "Shippment Tracking #": metadata.get("Shippment_track_number"),
            "Refund Status": metadata.get("Refund_Status"),
            
        }

        print(json.dumps(response, indent=4))

else:
    print("No matching order found.")
    
    
print("\n")
#print(results)
print(json.dumps(response, indent=4))
print("\n")
