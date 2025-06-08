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

# Set up the output parser
parser = JsonOutputParser(pydantic_object=ProductInformation)

# Create the chat prompt template

#You are a helpful assistant. When asked about any product, respond in JSON with product name, details, and a tentative price in USD (integer).

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant.When asked about any product, respond in JSON with product name, details, and a tentative price in USD (integer)"),
    ("user", "{input}")
])

# Initialize the model
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# Create the chain
chain = prompt | model | parser

print("\n")


print("JSON output parser")

# Example usage
response = chain.invoke({"input": "Tell me about the iPhone 15"})
print(response)


# chain = prompt | model | StrOutputParser()

# response = chain.invoke({"input": "what you suggest for mild fever."})

# print(response)

print("\n")
print("\n")

# ##Show output in a Table Format


# # parser = PydanticOutputParser(pydantic_object=TextPart)
    
# #     prompt = ChatPromptTemplate.from_messages(
# #         [
# #             ("system", systemprompt),
# #             ('human', "{section}"),
# #             ('human', f"{transcript.page_content}"),
# #         ]
# #     ).partial(format_instructions=parser.get_format_instructions(),
# #       pattern=re.compile(r"\`\`\`\n\`\`\`"))
    
# #     chain = prompt | llm | parser





# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful assistant.When asked about any product,provide information in a Header, Rows, tablular format, product name ,details, price in USD"),
#     ("user", "{input}")
# ])

# # parser = PydanticOutputParser(pydantic_object=TextPart)

# # Initialize the model
# model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

# # Create the chain
# #chain = prompt | model | parser
# chain = prompt | model | StrOutputParser()

# print("Using String Output Parser")

# # Example usage
# response = chain.invoke({"input": "Tell me about the iPhone 15"})
# print("\n")
# print(response)
# print("\n")