##Rajendra B
## This program will load the documents and scan from the folder location 
## This program will be used to Injest data into the vector Store and create embeddings


from pathlib import Path
from typing import List, Any
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders import JSONLoader
from unstructured import documents

from collections import defaultdict
from langchain_community.document_loaders import PyPDFLoader

import logging
import os

script_path = os.path.abspath(__file__)
# Get the directory name from the script path
script_dir = os.path.dirname(script_path)
# Get the parent directory using os.pardir ('..')
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
data_directory_path = os.path.join(parent_directory, "data")
print(f"Data directory path: {data_directory_path}")



logging.basicConfig(
    filename=os.path.join(data_directory_path, "dataload.log"),
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)




def load_PDF_docs(data_dir: str) -> List[Any]:
  
    print("[INFO] Initailazing  load_PDF_docs to load the files.. ")

    logging.info("Initailazing  load_PDF_docs to load the files")

    # Use project root data folder
    data_path = Path(data_dir).resolve()
    print("=="*20)
    print(f"[DataLoader DEBUG] Data path: {data_path}")
    print("=="*20)
    print(f"[DataLoader DEBUG] Initializing array for documents : {data_path}")
    print("=="*20)

    documents = []
    
    # PDF files
    pdf_files = list(data_path.glob('**/*.pdf'))
    print("=="*20)
    print(f"[DataLoader DEBUG] Found {len(pdf_files)} PDF files: {[str(f) for f in pdf_files]}")
    print("=="*20)

    for pdf_file in pdf_files:
        print("=="*20)
        print(f"[DataLoaderDEBUG] Loading PDF: {pdf_file}")
        print("=="*20)
        try:
            loader = PyPDFLoader(str(pdf_file))
            loaded = loader.load()
            print(f"[DataLoaderDEBUG] Loaded {len(loaded)} PDF docs from {pdf_file}")
            documents.extend(loaded)
            # Store documents grouped by file
            # pdf_data[str(pdf_file)] = docs
            for i, doc in enumerate(documents):
                print(f"DataLoader :  Showing the Doc Contents {i}: {doc}")
                logging.info(f"DataLoader :  Showing the Doc Contents {i}: {doc}")

        except Exception as e:
            print(f"[ERROR] Failed to load PDF {pdf_file}: {e}")

#     # TXT files
  
    return documents





# # Example usage
# if __name__ == "__main__":
#     docs = load_PDF_docs("data")
#     print(f"Loaded {len(docs)} documents.")
#     print("Example document:", docs[0] if docs else None)