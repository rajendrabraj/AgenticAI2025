from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser

## RB :  Date :  25th May'25 , Program : Langchain Parser and querying

# Define the Pydantic class for product info
class ProductInformation(BaseModel):
    name: str = Field(description="Product name")
    details: str = Field(description="Product details")
    price_usd: int = Field(description="Tentative price in USD")


print("\n")
print("\n")
print("Running the Program using LangChain")
print("\n")


## Pass information to Prompt..
print("Passing and Initializing information to Prompt")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant.When asked about any product,provide information in a Header, Rows, tablular format, product name ,details, price in USD"),
    ("user", "{input}")
])

# parser = PydanticOutputParser(pydantic_object=TextPart)

# Initialize the model
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)

# Create the chain
#chain = prompt | model | parser
chain = prompt | model | StrOutputParser()

print("Using String Output Parser")

# Example usage
response = chain.invoke({"input": "Tell me about the iPhone 15"})


print("\n")
print(response)
print("\n")

# Create the chain
#chain = prompt | model | parser
chain = prompt | model | StrOutputParser()

print("Using String Output Parser")

# Example usage

response = chain.invoke({"input": "Compare Iphone 15 and Iphone16 for specifications only"})
print("\n")
print(response)
print("\n")