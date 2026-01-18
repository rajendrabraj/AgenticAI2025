from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import json
import pandas as pd
from typing import TypedDict, List


load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

import streamlit as st

st.title(" 🏨 AI Toursit Attractions.. ")

user_input = st.text_input("Please Enter the City...")
city_name = user_input





#parser = JsonOutputParser(pydantic_object=MyHotelAssistant )

#("human", "Top 10 best Hotels with location and price per night and output must conform in JSON Format according to this schema: {json_schema} ")


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful Travel assistant and provide Top 10 Touist Attractions in the city given as input designed to output in strict JSON format.. "),         

        ( "human", 
          
          "Please provide Top 10 Touist Attractions {user_input} "
          "Provide Data as : 'Name', 'Location', 'Open Time' "
          
          ),
         
    ]
)

 


# 3. Instantiate the JSONOutputParser
#parser = JsonOutputParser()
output_parser = JsonOutputParser()

# 4. Bind the schema to the prompt and format for the LLM
# The .partial method allows injecting variables into the prompt before invocation.
#prompt_with_schema = chat_template.partial(json_schema=str(json_output_schema))

#prompt_with_schema = ChatPromptTemplate.partial(str(json_output_schema))    
#model_list = ["gemma2-9b-it", "llama-3.1-8b-instant" ,"llama-3.3-70b-versatile","whisper-large-v3"]

# Step 1: Select Model
# selected_model = st.selectbox("Select Type of OpenAI Model", model_list)
selected_model = "gemma2-9b-it"
model_selected = "gemma2-9b-it"

button=st.button("Search Toursit Attractions",type="primary",icon="🔍",use_container_width=True)

##Select the ChatGroq Model
#model = ChatGroq(model=selected_model, temperature=0.7, max_tokens=500)

#Invoke the LLM Model and bind the Json object 

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.5,max_tokens=1000).bind(response_format={"type": "json_object"})
#chain = prompt | model | parser
chain = prompt | llm | output_parser



if user_input:
    if user_input.isnumeric():
        st.error("Please Enter a proper City.")
    else:
        # Invoke the chain with the user input
        #response = chain.invoke({"Query": user_input, "format_instructions": output_parser.get_format_instructions()})
        response = chain.invoke(user_input)
        final_response = response
        st.write("Showing response\n")        
        st.write(final_response)
        st.write("--")
        # print(response)
      

        # 8. Convert the output to a JSON string for display
        json_output = json.dumps(response, indent=2)
        # 3. Use json.dumps() to serialize the list of dictionaries to a JSON string
        json_string_records = json_output # indent for pretty printing
        #df= json_output

        # df = pd.json_normalize(
        #     json_string_records,
        #     record_path='Hotels',  # Path to the list of records
        #     meta=['name', 'location', 'price_per_night' ], # Metadata to include from parent
        #     sep=':' # Separator for flattened column names
        # )
        
        response_df = pd.DataFrame(response)
        st.write("--")
               
        # st.write("🏨 Showing Toursit Attractions...")
        # print("\nJSON Formatted Output:")
        # print(json_output)
        # st.write(json_output) 
        #st.set_page_config(layout="wide")
      

        # # st.dataframe(response_df, use_container_width=True)
        # st.dataframe(response_df)
        # st.write("--")
        # st.table(response_df)
        # st.write("--")
        
       




        #Show the JSON Response
        
        st.write("\n")               
        #st.write("🏨Showing Toursit Attractions \n...")
        ## Convert to Dictionary object

        #Convert to List of Dictionaries
        list_of_dicts = response_df.to_dict(orient="records")
        # st.write("--")
        # st.write("🏨 Showing Toursit Attractions \n.....")
        # st.table(list_of_dicts)
        # st.write("--")

      

        ##Convert data to HTML
        html_table = response_df.to_html(index=False, border=1)
        # Show raw HTML (optional)
        # with st.expander("See raw HTML code"):
        # st.code(html_table, language='html')
        st.write("--")
        #st.write("🏨Showing Hotel Details\n...")
        st.subheader("🏨Showing Toursit Attractions\n")
        st.markdown(html_table, unsafe_allow_html=True)
        st.write("--")



          #Process the Dictionary

        # Convert list of dicts to DataFrame
        #df3 = pd.DataFrame(list_of_dicts)

        # Optional: Sort by price
        #df_sorted = df3.sort_values(by="price_per_night")

        # Display in Streamlit using table format
        # st.write("--")
        # st.subheader("Hotel Data Final\n.")
        # st.dataframe(df3, use_container_width=True)
        # st.write("--")
        st.write("Showing Markdown Response")
        st.write("--")
        st.markdown(final_response, unsafe_allow_html=False)
        st.write("--")

        st.write("Showing Data Frame...")
        st.write("--\n")
        st.dataframe(
            response_df,
            column_config=
                {
                "Name": "Hotel_Name","Location": "Hotel Address","Open Time": "Open Time",       
                } , hide_index=True)   
        st.write("--\n")
        st.success("Showing Toursit Attractions- Fetched Successful!")
else:
    st.write("--")