from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

import streamlit as st
st.title(" AI Product Agent Assistant ")
user_input = st.text_input("Please Enter the City...")
city_name = user_input

# 1. Define the desired JSON structure using a Pydantic model or a dictionary
# For simplicity, we'll use a dictionary here.
json_output_schema = {
    "hotel_name": "string",
    "hotel_address": "string",
    "hotel_rating": "string"
    "rate_per_night": "string"
}


class MyHotelAssistant (BaseModel):
    hotel_name : str = Field(description="Name of the Hotel.")
    hotel_address: str = Field(description="Address of the Hotel.",max_length=500)
    hotel_rating : str = Field(description="Ratings of the Hotel.")
    rate_per_night : float = Field(description="Rate per night.")



#parser = JsonOutputParser(pydantic_object=MyHotelAssistant )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "ou are a helpful assistant designed to output JSON. Your output must conform to the following JSON schema: {json_schema}\n"),
         #('user','{product_query} \n {format_instructions}')
         ("human", "Tell me top 10 best Hotels in the city {city_name}")
    ]
)

# 3. Instantiate the JSONOutputParser
parser = JsonOutputParser()

# 4. Bind the schema to the prompt and format for the LLM
# The .partial method allows injecting variables into the prompt before invocation.
prompt_with_schema = ChatPromptTemplate.partial(json_schema=str(json_output_schema))

model_list = ["gemma2-9b-it", "llama-3.1-8b-instant" ,"llama-3.3-70b-versatile","whisper-large-v3"]

# Step 1: Select Model
selected_model = st.selectbox("Select Type of OpenAI Model", model_list)
model_selected = selected_model

button=st.button(" Get Hotel Details",type="primary",icon="🔍",use_container_width=True)



if selected_model:
    model = ChatGroq(model=selected_model, temperature=0.7, max_tokens=500)

chain = prompt | model | parser

if user_input:
    if user_input.isnumeric():
        st.error("Please enter a valid product query.Numeric input is not allowed.")
    else:
        # Invoke the chain with the user input
        response = chain.invoke({"product_query": user_input, "format_instructions": parser.get_format_instructions()})
        #response["product_price"] = f"${response['product_price']:.2f}"  # Format price to two decimal places
        #response["product_price"] = float(response["product_price"])
        price= response["product_price"]
        converted_product_price = float(price)

        


        st.write("### Product Details")
        st.write(f"**Name:** {response['product_name']}")
        st.write(f"**Details:** {response['product_description']}")
        #st.write(f"**Product Price:** {response['product_price']}")
        st.write(f"**Product Price:** {converted_product_price}")
        
        st.write(f"**Product Category:** {response['product_category']}")
        st.success("Product details fetched successfully!")
else:
    st.write("Please enter a product query to get started.")