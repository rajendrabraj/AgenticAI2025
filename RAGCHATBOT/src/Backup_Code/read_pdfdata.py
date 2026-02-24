import os
from pypdf import PdfReader

# Path to your data folder (change if needed)
DATA_FOLDER = "C:\\Rajendra_2015\\AgenticAI_Programs\\Agentic_Batch2\\2-Langchain Basics\\11_IIT_Madras\\Week15_RAG_Assignment\\RAG-Tutorials-main\\RAG-Tutorials-main\\data\\"

# Get absolute path of data folder
data_path = os.path.abspath(DATA_FOLDER)
print("Data folder location:", data_path)


# # Check if folder exists
# if not os.path.exists(data_path):
#     print("❌ Data folder not found.")
#     exit()

# # Loop through all PDF files
# for filename in os.listdir(data_path):
#     if filename.lower().endswith(".pdf"):
#         file_path = os.path.join(data_path, filename)
#         print(f"\n📄 Reading: {file_path}")

#         reader = PdfReader(file_path)
#         text = ""

#         for page in reader.pages:
#             text += page.extract_text() or ""

#         print("----- Extracted Text (first 500 chars) -----")
#         print(text[:500])