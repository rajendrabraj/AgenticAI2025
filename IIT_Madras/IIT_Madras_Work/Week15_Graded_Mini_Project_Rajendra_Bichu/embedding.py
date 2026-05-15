## Rajendra B
## This program will only create the embeddings


from typing import List, Any
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
import sys


# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent))

#from data_loader import load_all_documents
#from dataloader_PDF import load_PDF_docs


class EmbeddingPipeline:
    def __init__(self, model_name: str = "groq/compound-mini", chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model = SentenceTransformer(model_name)
        print(f"[INFO] Loaded embedding model: {model_name}")

    def chunk_documents(self, documents: List[Any]) -> List[Any]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_documents(documents)
        print("=="*20)
        print(f"[INFO] Split {len(documents)} documents into {len(chunks)} chunks.")
        print("=="*20)
        
        return chunks

    def embed_chunks(self, chunks: List[Any]) -> np.ndarray:
        texts = [chunk.page_content for chunk in chunks]
        print("=="*20)
        print(f"[INFO] Generating embeddings for {len(texts)} chunks...")
        print("=="*20)
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print("=="*20)
        print(f"[INFO] Embeddings shape: {embeddings.shape}")
        print("=="*20)
        return embeddings

