from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Define the Pydantic class for product info
class ProductInformation(BaseModel):
    name: str = Field(description="Product name")
    details: str = Field(description="Product details")
    price_usd: int = Field(description="Tentative price in USD")

# Set up the output parser
parser = JsonOutputParser(pydantic_object=ProductInformation)

# Create the chat prompt template

#You are a helpful assistant. When asked about any product, respond in JSON with product name, details, and a tentative price in USD (integer).

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant.When asked about any product, respond in JSON with product name, details, and a tentative price in USD (integer)"),
    ("user", "{input}")
])

# Initialize the model
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

# Create the chain
chain = prompt | model | parser

print("\n")

# Example usage
response = chain.invoke({"input": "Tell me about the iPhone 15"})
print(response)

print("\n")
print("\n")

##Show output in a Table Format

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant.When asked about any product,provide information in a tablular format, product name ,details, price in USD"),
    ("user", "{input}")
])

# Initialize the model
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

# Create the chain
chain = prompt | model | parser

# Example usage
response = chain.invoke({"input": "Tell me about the iPhone 15"})
print("\n")
print(response)
print("\n")