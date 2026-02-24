import os
import sys
from pathlib import Path
from dotenv import load_dotenv


# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent))


from vectorstore import FaissVectorStore
from langchain_groq import ChatGroq


load_dotenv()

#Load Env Variables
import os
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

#New  model : nomic-embed-text-v1.5
# old embedding model : all-MiniLM-L6-v2


## Deprecated :  llama-3.1-70b-versatile



class RAGSearchPDF:

    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "llama-3.3-70b-versatile"):
        print("[INFO] Initailazing  RAGSearch PDF  Search... ")
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from dataloader_PDF import load_PDF_docs
            #docs = load_PDF_docs("data")
            docs = load_PDF_docs(data_path)
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        groq_api_key = GROQ_API_KEY
        self.llm = ChatGroq(api_key=groq_api_key, model=llm_model, temperature=0)
        print(f"[INFO] Groq LLM initialized: {llm_model}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = f"""Summarize the following context for the query: '{query}'\n\nContext:\n{context}\n\nSummary:"""
        response = self.llm.invoke([prompt])
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
    query= input("Enter your query to search: ")
    summary = rag_search_pdf.search_and_summarize(query, top_k=10)
    print("Summary:", summary)
