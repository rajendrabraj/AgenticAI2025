## This Python Program is to read the contents of the PDF File and Query them

## RB  , 31.05.2025 , PDF file Contents reviewer ...

import os

current_directory = os.getcwd()
print(current_directory)

### Read a PDf file

print("-"*100)

print("\n")

print("Start : Reading the PDF Documents")

from langchain_community.document_loaders import PyPDFLoader
loader=PyPDFLoader('syllabus.pdf')
docs=loader.load()
docs
# print(docs)

print("End : Reading the PDF Documents")
print("-"*100)

print("\n")

# from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_text_splitters import RecursiveCharacterTextSplitter
print("-"*100)

print("\n")
print("Start : Printing the Pages")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
text_splitter.split_documents(docs)[:5]
# print(text_splitter)

documents=text_splitter.split_documents(docs)
# print(documents)

print("END : Printing the Pages")
print("-"*100)
print("\n")

# ## Read the pages into the document.

# pages = []
# for doc in loader.lazy_load():
#     pages.append(doc)
#     if len(pages) >= 10:
#         # do some paged operation, e.g.
#         # index.upsert(page)

#         pages = []
# len(pages)

#Read the contents of the PDF PAge

# from langchain_community.document_loaders.parsers import LLMImageBlobParser
# from langchain_openai import ChatOpenAI

# loader = PyPDFLoader(
#     "syllabus.pdf",    
#     mode="page",
#     images_inner_format="markdown-img",
#     images_parser=LLMImageBlobParser(model=ChatOpenAI(model="gpt-4o", max_tokens=1024)),
# )
# docs = loader.load()
# #Read the contents of the Page #5 
# print("Start : Reading the Page #5 - Images ")
# print("-"*100)
# print("\n")
# print(docs[5].page_content)
# print("END : Reading the Page #5 - Images ")


# ## Load the document into FAISS and Query it

from langchain_community.embeddings import OpenAIEmbeddings
# from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
# from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader

print("-"*100)

print("\n")
print("START : Query #1 FAISS ")

#Page #
db=FAISS.from_documents(documents[:34],OpenAIEmbeddings())
query="Introduction to Vector databases "
result=db.similarity_search(query)
page_contents = result[0].page_content
print(page_contents)
print("-"*100)

print("\n")
print("Completed... : Query #1 FAISS ")

print("-"*100)

print("\n")






print("-"*100)

print("\n")
print("START : Query #2 FAISS ")

#Page #
db=FAISS.from_documents(documents[:34],OpenAIEmbeddings())
query="NoSQL databases with MongoDB"
result=db.similarity_search(query)
page_contents = result[0].page_content
print(page_contents)
print("-"*100)

print("\n")
print("End : Query #2 FAISS ")

print("-"*100)

print("\n")

	