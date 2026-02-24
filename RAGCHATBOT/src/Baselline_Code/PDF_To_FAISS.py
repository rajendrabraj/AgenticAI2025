from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.storage import LocalFileStore

from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader

import os

# -----------------------
# Step 1: Load PDF
# -----------------------

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the directory name from the script path
script_dir = os.path.dirname(script_path)

# Get the parent directory using os.pardir ('..')
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))

print(f"Script path: {script_path}")
print("=="*20)
print(f"Parent directory: {parent_directory}")
print("=="*20)
data_directory_path = os.path.join(parent_directory, "data")
print(f"Data directory path: {data_directory_path}")
print("=="*20)

pdf_file_name = os.path.join(data_directory_path, "World_Silver_Surveyreport.pdf")
print(pdf_file_name)
loader = PyPDFLoader(pdf_file_name)
documents = loader.load()

# -----------------------
# Step 2: Chunk Text
# -----------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

# -----------------------
# Step 3: Create Embedding Pipeline (with caching)
# -----------------------
store = LocalFileStore("./embedding_cache")

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

embedding_pipeline = CacheBackedEmbeddings.from_bytes_store(
    embedding_model,
    store,
    namespace="pdf_embeddings"
)

# -----------------------
# Step 4: Store in FAISS
# -----------------------
vectorstore = FAISS.from_documents(chunks, embedding_pipeline)

# Save FAISS index locally
vectorstore.save_local("faiss_index")

print("PDF successfully embedded and stored in FAISS!")

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# Example similarity search
query = "What is the document about?"
docs = vectorstore.similarity_search(query, k=3)

for d in docs:
    print("=="*20)        
    print("REading chunk content:")

    print(d.page_content)
    print("=="*20)

