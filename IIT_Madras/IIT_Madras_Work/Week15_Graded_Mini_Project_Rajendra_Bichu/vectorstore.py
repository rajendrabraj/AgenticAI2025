## Rajendra B
## This program will load the documents and create a Vector Store.
## This program will injest the contents of the document
## This program will also create Embeddings by calling the Embedding Pipeline and will create the FAISS Vector Store and will save the Vector Store in the local directory.
## It will also log all the activities in the VectorStore.log file in the data folder.


import os
from pathlib import Path
import faiss
import numpy as np
import pickle
import sys
import logging
import os

from dotenv import load_dotenv

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent))

from typing import List, Any
from sentence_transformers import SentenceTransformer
from embedding import EmbeddingPipeline

from dotenv import load_dotenv

load_dotenv()

#Load Env Variables
import os
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

script_path = os.path.abspath(__file__)
# Get the directory name from the script path
script_dir = os.path.dirname(script_path)
# Get the parent directory using os.pardir ('..')
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
data_directory_path = os.path.join(parent_directory, "data")
print(f"Data directory path: {data_directory_path}")

## Basic logging configuration


logging.basicConfig(
    filename=os.path.join(data_directory_path, "/VectorStore.log"),
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)


## Create a FAISS Vector store

class FaissVectorStore:
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", chunk_size: int = 1000, chunk_overlap: int = 200):
        print("[VectorStore INFO] Initializing FaissVectorStore... ")
        
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        self.index = None
        self.metadata = []
        self.embedding_model = embedding_model
        self.model = SentenceTransformer(embedding_model)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        print(f"[VectorStoreINFO] Loaded embedding model: {embedding_model}")
        logging.info(f"[ VectorStore INFO] Loaded embedding model: {embedding_model}")

    ## Build from the documents and create the vector store


    def build_from_documents(self, documents: List[Any]):
        print(f"[ VectorStore INFO] Building vector store from {len(documents)} raw documents...")
        emb_pipe = EmbeddingPipeline(model_name=self.embedding_model, chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = emb_pipe.chunk_documents(documents)
        embeddings = emb_pipe.embed_chunks(chunks)
        metadatas = [{"text": chunk.page_content} for chunk in chunks]
        self.add_embeddings(np.array(embeddings).astype('float32'), metadatas)
        # print(chunks[0].page_content if len(chunks) > 0 else "No chunks created.")
        # print("====" * 30)

        # print(chunks[55].page_content if len(chunks) > 0 else "No chunks created.")
        # print("====" * 30)
        
        self.save()
        print(f" [ VectorStore INFO] Vector store built Completed and saved to {self.persist_dir}")
        logging.info(f"[ VectorStore INFO] Vector store built Completed and saved to {self.persist_dir}")

    ## Create embeddings and add to the vector store


    def add_embeddings(self, embeddings: np.ndarray, metadatas: List[Any] = None):
        print("[VectorStore INFO] Initializing add_embeddings... ")
        print("=="*20)
        dim = embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        if metadatas:
            self.metadata.extend(metadatas)
        print(f"[VectorStore INFO] Added {embeddings.shape[0]} vectors to Faiss index.")
        logging.info(f"[ VectorStore INFO] Added {embeddings.shape[0]} vectors to Faiss index.")

    ## Save the embeddings
    
    def save(self):
        print("[INFO] calling save embeddings... ")
        faiss_path = os.path.join(self.persist_dir, "faiss.index")
        meta_path = os.path.join(self.persist_dir, "metadata.pkl")
        faiss.write_index(self.index, faiss_path)
        with open(meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
        print(f"[VectorStore INFO] Saved Faiss index and metadata to {self.persist_dir}")
        logging.info(f"[ VectorStore INFO] Saved FAISS index and metadata to {self.persist_dir}")

    def load(self):
        print("[VectorStore INFO] Initializing load faiss index... ")
        faiss_path = os.path.join(self.persist_dir, "faiss.index")
        meta_path = os.path.join(self.persist_dir, "metadata.pkl")
        self.index = faiss.read_index(faiss_path)
        with open(meta_path, "rb") as f:
            self.metadata = pickle.load(f)
        print(f"[VectorStore INFO] Loaded Faiss index and metadata from {self.persist_dir}")
        logging.info(f"[ VectorStore INFO] Faiss index and metadata loaded from {self.persist_dir}")

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        print("[VectorStore INFO] Invoking Vectore Search... ")
        D, I = self.index.search(query_embedding, top_k)
        results = []
        for idx, dist in zip(I[0], D[0]):
            meta = self.metadata[idx] if idx < len(self.metadata) else None
            results.append({"index": idx, "distance": dist, "metadata": meta})
        return results

    def query(self, query_text: str, top_k: int = 5):
        print(f"[VectorStore INFO] Querying vector store for: '{query_text}'")
        logging.info(f"[ VectorStore INFO] Querying vector store for: '{query_text}'")
        query_emb = self.model.encode([query_text]).astype('float32')
        return self.search(query_emb, top_k=top_k)

# # Example usage
# if __name__ == "__main__":
#     from data_loader import load_all_documents
#     docs = load_all_documents("data")
#     store = FaissVectorStore("faiss_store")
#     store.build_from_documents(docs)
#     store.load()
#     print(store.query("What is attention mechanism?", top_k=3))
