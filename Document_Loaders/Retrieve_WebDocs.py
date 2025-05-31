
# # ## Web based loader

# # print("Start : Loading documents with WebBased Loader")

print("Start : REad from the WEbbased loader the Pages")
print("-"*100)
print("\n")

from langchain_community.document_loaders import WebBaseLoader
import bs4
#loader=WebBaseLoader(web_paths=("https://python.langchain.com/docs/integrations/document_loaders/",),)

# loader=WebBaseLoader(web_paths=("https://timesofindia.indiatimes.com//",),)
loader=WebBaseLoader(web_paths=("https://inshorts.com/en/read",),)

#https://www.moneycontrol.com/news/tags/bse.html

#https://inshorts.com/en/read



docs=loader.load()
# docs
print("-"*100)
print("\n")

# print(docs)
print("-"*100)
print("\n")

print("End : Loading documents with WebBased Loader")

from langchain_text_splitters import RecursiveCharacterTextSplitter
print("-"*100)

print("\n")
print("Start : Printing the Pages")
print("\n")
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    separators=["\n\n", "\n","/"]
)

#separators=["\n\n", "\n", " ", ""]


text_splitter.split_documents(docs)[:1]
# print(text_splitter)
print("-"*100)
print("\n")
documents=text_splitter.split_documents(docs)
print(documents)

print("END : Printing the Pages")
print("-"*100)
print("\n")


text_splitter.split_documents(docs)[:2]
# print(text_splitter)
print("-"*100)
print("\n")
documents=text_splitter.split_documents(docs)
print(documents)

print("END : Printing the Pages")
print("-"*100)
print("\n")



 ## Web based loader

""" print("START : Loading documents with SoupStrainer Loader")


from langchain_community.document_loaders import WebBaseLoader
import bs4
loader=WebBaseLoader(web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
                     bs_kwargs=dict(parse_only=bs4.SoupStrainer(
                         class_=("post-title","post-content","post-header")
                     ))
                     )

doc=loader.load()
doc

print("-"*100)
print("\n")

print("End : Loading documents with SoupStrainer Loader")
 """

# print("START : Loading documents with Arxiv Loader")




# #Arxiv
# from langchain_community.document_loaders import ArxivLoader
# docs = ArxivLoader(query="1706.03762", load_max_docs=2).load()
# docs
# len(docs)

# print("END : Loading documents with Arxiv Loader")


# ##Wikipedia Information

# print("START : Loading documents with Wikipedia Loader")


# from langchain_community.document_loaders import WikipediaLoader
# docs = WikipediaLoader(query="Generative AI", load_max_docs=4).load()
# len(docs)
# print(docs)

# print("END : Loading documents with Wikipedia Loader")


