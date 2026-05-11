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

## Call the different agents and test them out in a chat bot like interface.

#from cust_agent_app import get_support_crew, get_evaluation_crew, execute_deployment_tracking
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


##Use a chat Bot like interface to interact with the agent and test it out   
def main() -> None:    
    print("-" * 90) 
    logging.info("========================")    
    logging.info("Logging is working!")
    logging.info("========================")
    
    print("\n Inside Crew Chat Bot Main Function \n ")
    logging.info("Inside Crew Chat Bot Main Function")
    while True:
        print("-" * 90) 
        print("\n") 
        print("\n") 
        user_input = input("\n User Please Submit your Query \n  : ")   
        print("\n") 
        print("\n") 
        print("-" * 90)
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("CREW CHAT Bot: Goodbye!")
            logging.info("CREW CHATBOT : Goodbye!")
            break
        else:        
            print("-" * 90) 
            print("\n") 
            logging.info("CREW CHATBOT Run #1 (With Evaluation) STARTED........")
            logging.info("========================")   
            result_evaluation= run_evaluation_experiment(user_input)
            logging.info(f"CREW CHATBOT Result Run #1 (With Evaluation): {result_evaluation}")
            logging.info("========================")   
            logging.info("CREW CHATBOT Run #1 (With Evaluation) Completed........")
            print("-" * 90) 
            print("\n") 
    
            query = user_input
            print("Executing chat bot with User Query : ", query )
            logging.info(f"CREW CHATBOT Run #3 Query Given :  {query} ")

            print("\n---CREW CHATBOT Run #2 :  Run Without Retrieval ---\n")
            logging.info("========================")   
            logging.info("CREW CHATBOT Run #2 :  Run Without Retrieval")
            print("-" * 90)
            baseline_output = run_without_retrieval(query)
            logging.info("========================")   
            print("-" * 90)
            logging.info("CREW CHATBOT Run #3 :  Run WITH Retrieval")
            print("\n---CREW CHATBOT Run #3 :  Run WITH Retrieval ---\n")
            retrieval_output = run_with_retrieval(query)
            print("-" * 90)
            print("CREW CHATBOT Run #3 : WITHOUT RETRIEVAL: OUTPUT ", baseline_output)
            logging.info(f"CREW CHATBOT Run #3 : WITHOUT RETRIEVAL OUTPUT: {baseline_output}")
            logging.info("========================")   
            print("-" * 90)
            print("CREW CHATBOT Run #4 : WITH RETRIEVAL: OUTPUT ", retrieval_output)
            logging.info(f"CREW CHATBOT Run #4 : WITH RETRIEVAL OUTPUT: {retrieval_output}")
            logging.info("========================")   
            print("-" * 90)

            ## Test Prompt Testing             
            logging.info("========================")    
            logging.info("CREW CHATBOT Run #4 Prompt Testing") 
            result_prompt_testing = run_prompt_testing(query)
            logging.info(f"CREW CHATBOT Run #4 : {result_prompt_testing}")
            logging.info("========================") 
            
           ## Test Prompt Testing             
            logging.info("========================")    
            logging.info("CREW CHATBOT Run #5 Run Memory with Conversation History") 
            result_memory_conversation = run_memory_conversation(query)
            logging.info(f"CREW CHATBOT Run #5 :  {result_memory_conversation}")
            logging.info("========================") 
    

## The main function

if __name__ == "__main__":
    main()
    
        