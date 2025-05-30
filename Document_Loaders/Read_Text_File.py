# file_name = "C:\Rajendra_2015\AgenticAI_Programs\Agentic_Batch2\2-Langchain Basics\2.1-DataIngestion\speech.txt" 
# print(file_name) 


# print("Start : Loading documents with Text Loaders")


from langchain_community.document_loaders.text import TextLoader
loader=TextLoader('speech.txt')
loader
text_documents=loader.load()
text_documents
print(text_documents)
print("End : Loading documents with Text Loaders")

from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)

print("\n")

print("-"*100)


print("START : Splitting the documents using : RecursiveCharacterTextSplitter ")

speech=""
with open("speech.txt") as f:
    speech=f.read()


text_splitter=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20)
text=text_splitter.create_documents([speech])
print(text[0])
print(text[1])
print(text[2])
print(text[3])


print("-"*100)

print("\n")

print("END : Splitting the documents : using RecursiveCharacterTextSplitter")