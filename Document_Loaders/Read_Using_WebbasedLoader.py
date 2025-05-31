from langchain_community.document_loaders import WebBaseLoader
import bs4

# Initialize a WebBaseLoader to load and parse the Wikipedia page on Artificial Intelligence.
# The bs_kwargs argument uses BeautifulSoup's SoupStrainer to only parse elements with the specified classes.
loader = WebBaseLoader(
    web_path=("https://en.wikipedia.org/wiki/Artificial_intelligence",),
    bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=("mw-heading mw-heading3", "mw-default-size")))
)

# Load the documents from the web page using the loader
docs = loader.load()


# Print the number of documents loaded from the web page
print(f"Loaded {len(docs)} web-based documents.")
print("Start : Show contents of docs")
print("-"*100)
print("\n")
print(docs)
print("End : Show contents of docs")
print("-"*100)
print("\n")


# Initialize a WebBaseLoader to load and parse the Wikipedia page on Artificial Intelligence.
# The bs_kwargs argument uses BeautifulSoup's SoupStrainer to only parse elements with the specified classes.
loader1 = WebBaseLoader(
    web_path=("https://en.wikipedia.org/wiki/Agentic_AI",),
    bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=("firstHeading mw-first-heading", "mw-default-size")))
)


#firstHeading mw-first-heading


#vector-body-before-content

# Load the documents from the web page using the loader
docs1 = loader1.load()

# Print the number of documents loaded from the web page
# print(f"Loaded {len(docs1)} web-based documents.")
print("Start : Show contents of docs")
print("-"*100)
print("\n")
print(docs1)
print("End : Show contents of docs")
print("-"*100)
print("\n")


