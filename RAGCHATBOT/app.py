# from src.data_loader import load_all_documents
# from src.vectorstore import FaissVectorStore
# from src.search import RAGSearch
# from src.ragsearch_PDF import RAGSearchPDF
# import os
# from pathlib import Path
# from dotenv import load_dotenv

# import sys
# # Add parent directory to path to enable imports
# sys.path.insert(0, str(Path(__file__).parent))


# from src.vectorstore import FaissVectorStore
# from langchain_groq import ChatGroq


# # # Example usage
# # if __name__ == "__main__":
    
# #     docs = load_all_documents("data")
# #     store = FaissVectorStore("faiss_store")
# #     #store.build_from_documents(docs)
# #     store.load()
# #     #print(store.query("What is attention mechanism?", top_k=3))
# #     ##Cal the RAG search on the PDF files
    
# #     rag_search = rag_search_pdf()
# #     query = "What is attention mechanism?"
# #     summary = rag_search.search_and_summarize(query, top_k=3)
# #     print("Summary:", summary)



# # Example usage
# if __name__ == "__main__":
#     # Path to your data folder (change if needed)
#     DATA_FOLDER = "C:\\Rajendra_2015\\AgenticAI_Programs\\Agentic_Batch2\\2-Langchain Basics\\11_IIT_Madras\\Week15_RAG_Assignment\\RAG-Tutorials-main\\RAG-Tutorials-main\\data\\"
#     # Get absolute path of data folder
#     data_path = os.path.abspath(DATA_FOLDER)
#     print("Data folder location:", data_path)
#     rag_search_pdf = RAGSearchPDF()
#     query= input("Enter your query to search: ")
#     summary = rag_search_pdf.search_and_summarize(query, top_k=10)
#     print("Summary:", summary)
