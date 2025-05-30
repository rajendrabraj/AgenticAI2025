
from langchain_community.document_loaders import WikipediaLoader

print("-"*100)

print("\n")

print("Start :  Wikipedia Contents Loading  ")
print("\n")
print("-"*100)

docs = WikipediaLoader(query="Virat Kohli", load_max_docs=5).load()
len(docs)
# print(docs)
print("End :  Wikipedia Contents Loading  ")

print("\n")
print("-"*100)


from langchain_text_splitters import RecursiveCharacterTextSplitter
print("-"*100)

print("\n")
print("Start : Printing the Pages")
print("\n")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=125)
text_splitter.split_documents(docs)[:1]
# print(text_splitter)
print("-"*100)
print("\n")
documents=text_splitter.split_documents(docs)
print(documents)

print("END : Printing the Pages")
print("-"*100)
print("\n")


# importing the module
# import wikipedia

# # setting language to hindi
# wikipedia.set_lang("hi")

# print("\n")
# print("-"*100)

# # printing the summary
# print(wikipedia.summary("India"))
# print("\n")
# print("-"*100)
