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

# Accept explicit override from env, and try both expected filenames.
CSV_FILE = os.getenv("CSV_FILE_PATH")
if not CSV_FILE:
    expected_file = os.path.join(data_directory_path, "Product_Order_Customer_Data.csv")
    duplicate_file = os.path.join(data_directory_path, "Product_Order_Customer_Data.csv.csv")
    if os.path.exists(expected_file):
        CSV_FILE = expected_file
    elif os.path.exists(duplicate_file):
        CSV_FILE = duplicate_file
    else:
        raise FileNotFoundError(
            f"CSV file not found. Checked:\n"
            f"  {expected_file}\n"
            f"  {duplicate_file}\n"
            "Set CSV_FILE_PATH env var to the correct path if needed."
        )

print(f"Using CSV file: {CSV_FILE}")








# =====================================================
# INITIALIZE CLIENTS
# =====================================================

pc = Pinecone(api_key=pinecone_api_key)
#index = pc.Index(PINECONE_INDEX_NAME)
index = pc.Index(index_name)

openai_api_key = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=openai_api_key)

# # =====================================================
# STEP 1: Delete old data


# index.delete(delete_all=True)
# print("\nExisting records deleted\n")
# stats = index.describe_index_stats()
# print(" After Deleting Records :", stats["total_vector_count"])

# # =====================================================
# # LOAD CSV
# # =====================================================

print("Loading CSV file...")
df = pd.read_csv(CSV_FILE)
print(f"Total rows found: {len(df)}")

# # =====================================================
# # CREATE TEXT FOR EMBEDDING
# # =====================================================

# # Combine all columns into one searchable text
# # You can customize this section

def row_to_text(row):
    return " | ".join([
        f"{col}: {row[col]}"
        for col in df.columns
    ])

# # =====================================================
# # GENERATE EMBEDDINGS
# # =====================================================

def get_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding

# # =====================================================
# # UPSERT DATA TO PINECONE
# # =====================================================

batch_size = 100
vectors = []


print("Generating embeddings and uploading to Pinecone...")

for i, row in tqdm(df.iterrows(), total=len(df)):

    text = row_to_text(row)

    embedding = get_embedding(text)

    vector = {
        "id": str(uuid.uuid4()),
        "values": embedding,
        "metadata": {
            "text": text,
            **{col: str(row[col]) for col in df.columns}
        }
    }

    vectors.append(vector)

    # Batch upload
    if len(vectors) >= batch_size:
        index.upsert(vectors=vectors)
        vectors = []

# # Upload remaining vectors
# if vectors:
#     index.upsert(vectors=vectors)

print("Data upload completed successfully!")
stats = index.describe_index_stats()
print("Final Records Inserted/updated  Records:", stats["total_vector_count"])


## Query the data to check again


# query_embedding = client.embeddings.create(
#     model="text-embedding-3-small",
#     input="Customer refund issue for delayed order"
# ).data[0].embedding

# results = index.query(
#     vector=query_embedding,
#     top_k=5,
#     include_metadata=True
# )

# print(results)

