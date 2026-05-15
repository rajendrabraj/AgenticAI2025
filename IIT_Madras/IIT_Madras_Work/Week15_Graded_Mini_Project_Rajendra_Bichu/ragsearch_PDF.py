## Rajendra B. This program will search all the PDF documents in the folder and as per the query will build the FAISS VEctor Store
## It will also log all the activities in the RagSearchLog.log file in the data folder.
## It will also query the Search based on the query given into FAISS Vector Store and will summarize the results using Groq LLM and log the results in the same log file.

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

from unstructured import logger

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent))


from vectorstore import FaissVectorStore
from langchain_groq import ChatGroq


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



logging.basicConfig(
    filename=os.path.join(data_directory_path, "/RagSearchLog.log"),
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)

logging.info("RAG Search PDF module initialized.")

logging.info(f"Data directory path: {data_directory_path}")


#New  model : nomic-embed-text-v1.5
# old embedding model : all-MiniLM-L6-v2


## Deprecated :  llama-3.1-70b-versatile



class RAGSearchPDF:

    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "llama-3.3-70b-versatile"):
        print("[RAGPDF] Initailazing  RAGSearch PDF  Search... ")
        logging.info(f"[RAGPDF] initailazing  RAGSearch PDF  Search")
  


        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")        
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        print("Faiss path:", faiss_path)
        print("META path:", meta_path)
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            print("[Debug]-INSIDE IF function...")    
            logging.info(f"[ VRAGPDF] Inside IF Function...")
            from dataloader_PDF import load_PDF_docs
            #docs = load_PDF_docs("data")
            docs = load_PDF_docs(data_path)
            print(docs[0] if docs else "No documents loaded.")
            print("=="*20)
            print(docs[-1] if docs else "No documents loaded.")
            print("=="*20)
            print(docs[0] if docs else "No documents loaded.")
            print("=="*20)
            print("total documents loaded:", len(docs) if docs else 0)
            print("=="*20)
            print("First Document:", docs[-1] if docs else "No documents loaded.")
            print("Second Document:", docs[0] if docs else "No documents loaded.")
            print("Third Document:", docs[1] if docs else "No documents loaded.")

            print("=="*20)
            print("total documents loaded:", len(docs) if docs else 0)

        
            print("[RAGSERACH BOT : ] START building vector store from documents...")          
            logging.info(f"[RAGSERACH BOT : ] START building vector store from documents...")
            self.vectorstore.build_from_documents(docs)
            print("[RAGSERACH BOT : ] END  building vector store from documents...")          
            logging.info(f"[RAGSERACH BOT : ] END  building vector store from documents...")
        else:
            print("[Debug]-START Loading Vector Stores...") 
            logging.info(f"[RAGSERACH BOT : ] START Loading Vector Stores...")  
            self.vectorstore.load()
            print("[Debug]-END Loading Vector Completed...")   
            logging.info(f"[RAGSERACH : ] END Loading Vector Completed...")   
        groq_api_key = GROQ_API_KEY
        self.llm = ChatGroq(api_key=groq_api_key, model=llm_model, temperature=0)
        print(f"[INFO] Groq LLM initialized: {llm_model}")
        logging.info(f"[RAGSERACH BOT : ] Groq LLM initialized: {llm_model}")   

    ## Search the vector store and summarize based on the contents laoded for the query given.
    
    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        logging.info(f"[RAGSERACH BOT : ] Searching and Summarizing for query: {query}")   
        if not context:
            return "No relevant documents found."
        prompt = f"""Summarize the following context for the query: '{query}'\n\n Context:\n{context}\n\nSummary:"""
        print("=="*60)
        logging.info(f"================================")

        logging.info(f"[RAGSERACH BOT : ] Summarize the following context for the query: : {query} '\n\n ")
        print("=="*60)
        logging.info(f"================================")
        logging.info(f"[RAGSERACH BOT: ] Searching and Summarizing this Context : {context}")   
        print("=="*60)    
        logging.info(f"================================")
        response = self.llm.invoke([prompt])
        logging.info(f"================================")
        logging.info(f"[RAGSERACH BOT : ] Logging the RE: {response.content}")   
        logging.info(f"================================")
        return response.content





# Example usage
if __name__ == "__main__":
    # Path to your data folder (change if needed)
    #DATA_FOLDER = "C:\\Rajendra_2015\\AgenticAI_Programs\\Agentic_Batch2\\2-Langchain Basics\\11_IIT_Madras\\Week15_RAG_Assignment\\RAG-Tutorials-main\\RAG-Tutorials-main\\data\\"
    # Get absolute path of data folder
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
    ##Give the DATA_FOLDER path to the data_path variable

    data_path = data_directory_path
    print("Data folder location:", data_path)
    rag_search_pdf = RAGSearchPDF(data_path)
    logging.info(f"[RAGSERACH : ] Querying the Final Vector Store....")   

    query= input("Enter your query to search: ")
    summary = rag_search_pdf.search_and_summarize(query, top_k=10)
    print("Summary:", summary)

    query= input("Next query to search: ")
    summary = rag_search_pdf.search_and_summarize(query, top_k=10)
    print("Summary:", summary)

    query= input("Enter Last Query to Search ")
    summary = rag_search_pdf.search_and_summarize(query, top_k=10)
    print("Summary:", summary)
