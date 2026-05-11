## Rajendra Bichu : Date : 29.04.2026 , Version 1.0
##This is like a customer support ChatBOT to Test Multiple Agents
## Test and call different agents and test them out in a chat bot like interface.


from fastapi import FastAPI
import uvicorn
import os
import sys
import logging
import warnings
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from fastapi import FastAPI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from fastapi import FastAPI, HTTPException
from loguru import logger
import pinecone
import time
import traceback
#from cust_agent_app import get_support_crew, get_evaluation_crew, execute_deployment_tracking

## Call the different agents and test them out in a chat bot like interface.

from Customer_Agent_With_Evaluation import run_evaluation_experiment ,run_without_retrieval , run_with_retrieval
from Customer_Agent_Prompt_Testing import run_prompt_testing
from run_Customer_Agent_With_Memory import run_memory_conversation 

# Ensure the parent src folder is importable when this file is executed from elsewhere.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


## This section is more about calling different agents with different parameters



script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
logs_directory_path = os.path.join(parent_directory, "logs")
os.makedirs(logs_directory_path, exist_ok=True)
file_name = os.path.join(logs_directory_path, "CrewAgentChatBOT_LOG.log")

logging.basicConfig(
    filename=file_name,
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True,  # Force reconfiguration to ensure the new filename is used
)

print("Logs Directory Path: ", logs_directory_path)
print("Logs File Name: ", file_name)
logging.info("Logging is working!")


import streamlit as st

## Streamlit UI
st.title("Customer AI Support Resolution Agent -Crew Chat Bot Interface")


user_input = st.text_input("Enter your Query")

# Non-editable Query Results area
query_results = st.empty()

if st.button("Submit Query"):
    output_text = "CREW CHAT Bot Execution : Calling Multiple Agents!"
    query_results.text_area(
            "Query Results",
            value=output_text,
            height=600,
            disabled=True
        )

    if user_input.lower() in ["exit", "quit", "bye"]:
        output_text = "CREW CHAT Bot: Goodbye!"
        query_results.text_area(
            "Query Results",
            value=output_text,
            height=600,
            disabled=True
        )

        logging.info("Executing Streamlit CREW CHATBOT : Goodbye!")
        output_text = "CREW CHATBOT : Goodbye"
        query_results.text_area(
            "Query Results",
            value=output_text,
            height=600,
            disabled=False )

    else:
        print("-" * 90)

        logging.info("Executing Streamlit CREW CHATBOT Run #1 (With Evaluation) STARTED........")
        logging.info("========================")
        
        output_text = "\n Executing Streamlit CREW CHATBOT with User Query: " + user_input
        query_results.text_area(
            "Query Results",
            value=output_text,
            height=600,
            disabled=False )

        result_evaluation = run_evaluation_experiment(user_input)

        logging.info(f"\n Executing Streamlit CREW CHATBOT Result Run #1 (With Evaluation): {result_evaluation}")
        logging.info("========================")
        logging.info("\n Executing Streamlit CREW CHATBOT Run #1 (With Evaluation) Completed........")

        query = user_input

        logging.info(f"Executing Streamlit CREW CHATBOT Run #3 Query Given :  {query} ")

        logging.info("========================")
        logging.info("Executing Streamlit CREW CHATBOT Run #2 : Run Without Retrieval")

        baseline_output = run_without_retrieval(query)

        logging.info("========================")
        logging.info("Executing Streamlit CREW CHATBOT Run #3 : Run WITH Retrieval")

        retrieval_output = run_with_retrieval(query)

        logging.info(f"Executing Streamlit CREW CHATBOT Run #3 : WITHOUT RETRIEVAL OUTPUT: {baseline_output}")
        logging.info("========================")

        logging.info(f"Executing Streamlit CREW CHATBOT Run #4 : WITH RETRIEVAL OUTPUT: {retrieval_output}")
        logging.info("========================")

        ## Test Prompt Testing
        logging.info("========================")
        logging.info("Executing Streamlit CREW CHATBOT Run #4 Prompt Testing")
        result_prompt_testing = run_prompt_testing(query)
        logging.info("========================")
        
        ## Test Memory Testing             
        logging.info("========================")    
        logging.info("Executing Streamlit CREW CHATBOT Run #5 Run Memory with Conversation History") 
        result_memory_conversation = run_memory_conversation(query)
        logging.info("========================") 

        # Combined output for Query Results area
        output_text = f"""
                Executing Streamlit CREW CHATBOT with User Query:
                {query}

                ------------------------------------------------------------

                WITH EVALUATION OUTPUT:Streamlit CREW CHATBOT Run #1 (With Evaluation) Output:
                {result_evaluation}

                ------------------------------------------------------------

                WITHOUT RETRIEVAL OUTPUT Streamlit CREW CHATBOT Run #2 (Without Retrieval) Output:
                {baseline_output}

                ------------------------------------------------------------

                WITH RETRIEVAL OUTPUT Streamlit CREW CHATBOT Run #3 (With Retrieval) Output:
                {retrieval_output}
                ------------------------------------------------------------
                Customer CHAT BOT Query Fetched and execution is completed.
                ------------------------------------------------------------
                
                Streamlit CREW CHATBOT Run #4 (With Prompt Testing) Output:
                {result_prompt_testing}
                ------------------------------------------------------------
                
                Streamlit CREW CHATBOT Run #5 (With Memory Testing) Output:
                {result_memory_conversation}
                ------------------------------------------------------------
                
                Customer CHAT BOT Query Fetched and execution is completed.
                ------------------------------------------------------------
                
                
                
                """

        # Non-editable output area
        query_results.text_area(
            "Query Results",
            value=output_text,
            height=600,
            disabled=False
        )
                
        
