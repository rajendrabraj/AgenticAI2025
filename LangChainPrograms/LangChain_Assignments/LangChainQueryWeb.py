from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.tools import DuckDuckGoSearchRun


## RB :  Date :  25th May'25 , Program : Query the Web and Internet for specific answers
## RB :  Date :  25th May'25 , Program : Query the web using DuckduckGoSearch


##Try asking question using the OpenAPI queries.

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions."),
#     ("human", "{question}")
# ])

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a very knowledgeable who provides accurate answers to questions."),
    ("human", "{question}")
])


# runnable = prompt | model | StrOutputParser()
# print("\n")   
# for chunk in runnable.stream({"question": "Display records about Sachin Tendulkar"}):     
#     print(chunk, end="", flush=True)
    

print("\n")
print("\n")

print("Executing DuckduckGo...")

# search = DuckDuckGoSearchRun()
# search.run("manchester united vs luton town match summary")

tool = DuckDuckGoSearchRun(
    description="A custom DuckDuckGo search tool for finding programming resources.",
    verbose=True
)

print("\n")

# Example usage
result = tool.invoke("List of available GenAi Tools")

# word_count = len(result.split())
# print("\nNumber of words:", word_count)
print("\n")
print("\n")
# print(result)
print("\n")


# List of queries to process in a Array one by one 
queries = ["machine learning", "data science"]

# Perform batch processing
results = tool.batch(queries)
for result in results:
    print(result)
    print("-"*100)


print("\n")
print("-"*100)

##Initialize the variable

tool = None

# Initialize the tool
tool = DuckDuckGoSearchRun(
    description="Latest News.",
    verbose=True
)



print("-"*100)
print("Showing the Latest News Feeds...")
print("\n")
print("\n")


# Stream search results
query = "Latest on India Mumbai Rains."
for result in tool.stream(query):
    print(result)
    

print("\n")
print("\n")

print("Completed DuckduckGo...")