## Rajendra Bichu : Date : 18.05.2026  , Version 1.0

##This is like a customer support ChatBOT to Test Multiple Agents
## Test and call different agents and test them out in a chat bot like interface.
## This is the main program which calls the other API's 

## Objective

## This is the main and master program which calls the Pinecone KnowledgeBase
## The query wil be first executed against the KnowledgeBASE and output of which will be then routed for Crew AI Agents for Evaluation, Escalation or PII Check
## This will also give a call to Multiple agents as per output of the Query 

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
import json
from datetime import datetime

## This will call all agents as and when recquired


## ============================================================================
## This where all the agents are called and respective API/Functions are called


from search_knowledge_base import search_knowledge_base_records
from agent_escalation import run_escalate_agent
from agent_evaluation import run_evaluation_agent
from agent_PII_check import run_PII_check 
from agent_Cyber_Check import execute_cyber_checks
from search_knowledge_base import search_knowledge_base_records
from agent_execute_tools import run_tools_agent
from agent_multi_agent import execute_multi_agent_check


## ============================================================================


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
file_name = os.path.join(logs_directory_path, "Agent_execution_ChatBOT_LOG.log")

OUTPUT_FILE = os.path.join(logs_directory_path, "AI_CHATBOT_OUTPUT.txt")

logging.basicConfig(
    filename=file_name,
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True,  # Force reconfiguration to ensure the new filename is used
)

print("Logs Directory Path: ", logs_directory_path)
print("Logs File Name: ", file_name)
logging.info("Logging is working!")





    
## This is to create Log file and log critial information as Agents Execute 
## Add Output to a TEXT File 

def append_to_chatbot_file(response_json):

    file = open(OUTPUT_FILE, "a", encoding="utf-8")
    json_output = json.dumps(response_json, indent=4)
    
    file.write(json_output + "\n\n")

    file.close()

    return "SUCCESS"

## This is to create Log file and log critial information as Agents Execute 
## Add Output to a TEXT File 

def append_to_chatbot_file_string(response_string):
    # Handle CrewOutput objects by extracting raw output
    if hasattr(response_string, 'raw'):
        response_text = response_string.raw
    else:
        response_text = str(response_string)

    file = open(OUTPUT_FILE, "a", encoding="utf-8")

    file.write(response_text + "\n\n")

    file.close()

    return "SUCCESS"

## Call the Multi Agents for Cyber Threat and PII Check 

def run_multi_agent() -> str: 
        user_input = input("\n User Please Submit your Query \n  : ")   
        query= user_input     
        
        start_time = str(datetime.now()) 
        lstr_plain_string = start_time + " :  AI CHAT BOT ORDER QUERY : " + query   
        append_to_chatbot_file_string(lstr_plain_string)
        lstr_plain_string = "=========================================================="
        append_to_chatbot_file_string(lstr_plain_string)
    
        print("AI CHATBOT OTHER Queries : Calling the Cyber Threat and PII Agent")
        logging.info(f"AI CHATBOT OTHER Queries  : Calling the Cyber Threat and PII Agent for query  : {query}")
        final_cyber_check_response = execute_multi_agent_check(query)
        print(final_cyber_check_response)
        logging.info(f"AI CHATBOT :  Cyber Threat and PII Agent Result : {final_cyber_check_response}")              
        print("AI CHATBOT OTHER Queries :   Cyber Threat and PII Agent :", final_cyber_check_response)      
        
        ## Log the response
        lstr_plain_string = "========================AI CHATBOT Cyber Check Completed ====================="
        append_to_chatbot_file_string(lstr_plain_string)
        logging.info(f"AI CHATBOTCyber Threat and PII Agent  Result : {final_cyber_check_response}")    
        ## Copy the results to Output File
        append_to_chatbot_file_string(final_cyber_check_response)  
        lstr_plain_string = "============================================"
        append_to_chatbot_file_string(lstr_plain_string)
        
        result = final_cyber_check_response
        



## Use the Tools calling Agent to use the tools and get the results for the above query. 
def call_tools(query: str) -> str:
    start_time = str(datetime.now()) 
    lstr_plain_string = start_time + " :  AI CHAT BOT ORDER QUERY : " + query    
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)    
    tools_execution_response = run_tools_agent(query)
    end_time =  str(datetime.now())    
    lstr_plain_string = end_time + " :  AI CHAT BOT QUERY COMPLETED : " + query   
    append_to_chatbot_file_string(tools_execution_response)    
    
    
    return tools_execution_response

def order_status(order_id):
    logging.info("Routing to Order Status")
    #result = f"Checking Order Status for {order_id}"
    query = "give me order status for Order_Id  = " + order_id
    
    
    
    ##give me order status for order id Order_Id= O002
    
    
    start_time = str(datetime.now()) 
    lstr_plain_string = start_time + " :  AI CHAT BOT ORDER QUERY : " + query    
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
       
    append_to_chatbot_file_string(query)
    response_json = search_knowledge_base_records(input_query=query) 
   
    
    print(response_json)
    clean_json = json.loads(response_json)
    final_clean_output = json.dumps(clean_json)        
  
    #clean_output = json.dumps(response_json, separators=(",", ":"))
    final_clean_output = json.dumps(clean_json)   
    print("\n")         
    print(f"Response String CLEAN  # 2 :  {final_clean_output} " )
    print("\n")     
    
    # Log JSON without \n characters (use safe f-string to avoid percent-formatting issues)
    logging.info(f"AI CHATBOT Logging : Search KnowledgeBase Response : {final_clean_output}")    
    logging.info(f"AI CHATBOT Logging :  Response : : {final_clean_output}")    
       
     # Convert JSON object to JSON string
    response_string = json.dumps(response_json, indent=4)            
    print(response_string)   
            
     ## Copy the results to      
    lstr_plain_string = "AI CHATBOT File Logging :  RESULTS of KnowledgeBase   :  " + query
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "AI CHATBOT AI CHATBOT Logging : Knowledge Base Results"
    append_to_chatbot_file_string(final_clean_output)
        
    append_to_chatbot_file(response_string)     
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)        
    
    ## Execute and run the Evaluaton Check 
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Evaluation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    
    print("AI CHATBOT  :  Calling the Evaluation Agent")
    logging.info(f"AI CHATBOT  : Calling Evaluation Agent Now for query {query}")    
    final_Evaluation_response = run_evaluation_agent(query,response_string)
    print(final_Evaluation_response)
    logging.info(f"AI CHATBOT  : Evaluation Check  Result : {final_Evaluation_response}")      
    ## Copy the results to 
    append_to_chatbot_file_string(final_Evaluation_response)
    
    ## Execute the PII Check 
    lstr_plain_string = "AI CHATBOT : Calling PII  Agent Now for  :  "  + query 
    append_to_chatbot_file_string(lstr_plain_string)
    
    print("AI CHATBOT : Calling the PII Agent")
    logging.info(f"AI CHATBOT : Calling PII  Agent Now for query  : {query}")
    final_PII_Check_response = run_PII_check(query,response_string)
    print(final_PII_Check_response)
    logging.info(f"AI CHATBOT : PII Check  Result : {final_PII_Check_response}")
    
    ## Copy the results to 
    append_to_chatbot_file_string(final_PII_Check_response)

    ##Check it there is a need for Escalation for the above query
    print("AI CHATBOT :Calling the Escalation Agent")
    logging.info(f"AI CHATBOT : Calling Escalation Agent Now for query  : {query}")    
    lstr_plain_string = "AI CHATBOT : Calling Escalation Agent Now for query  :  "  + query 
    append_to_chatbot_file_string(lstr_plain_string)   
    
    final_escalation_response = run_escalate_agent(query,response_string)
    print(final_escalation_response)
    logging.info(f"AI CHATBOT : Escalation Agent Results : {final_escalation_response}")   
     
     ## Copy the results to 
    append_to_chatbot_file_string(final_escalation_response)   
    
    end_time =  str(datetime.now())    
    lstr_plain_string = end_time + " :  AI CHAT BOT ORDER QUERY COMPLETED : " + query   
    append_to_chatbot_file_string(lstr_plain_string)    
    
    
    append_to_chatbot_file_string(end_time)    

    return "SUCCESS"


def shipment_status(order_id):
    logging.info("Routing to check Shippment Status")
    
    query = "give me shipment status and shipment tracking for Order_Id = " + order_id
    
    # result = f"Checking Shipment Status for {order_id}"
    #give me shipment status and shipment tracking for Order_Id= O015
    start_time = str(datetime.now()) 
    lstr_plain_string = start_time + " :  AI CHAT BOT ORDER QUERY : " + query   
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
    
    
    
    response_json = search_knowledge_base_records(input_query=query)
    print(response_json)
    clean_json = json.loads(response_json)
    clean_output = json.dumps(clean_json)        
    print("\n")         
    print(f"Response String CLEAN  :  {clean_output} " )
    print("\n")   
    logging.info("AI CHATBOT  :  Response : %s", json.dumps(clean_output, indent=4))
     # Convert JSON object to JSON string
    response_string = json.dumps(response_json, indent=4)            
    print(response_string)         
    
    ## Knowledge Base Search to copy the Records are logged to the log file and CHAT BOT File.
    #clean_output = json.dumps(response_json, separators=(",", ":"))
    final_clean_output = json.dumps(clean_json)   
    print("\n")         
    print(f"Response String CLEAN  # 2 :  {final_clean_output} " )
    print("\n")     
    # Log JSON without \n characters (use safe f-string to avoid percent-formatting issues)
    logging.info(f"AI CHATBOT Logging : Search KnowledgeBase Response : {final_clean_output}")    
    logging.info(f"AI CHATBOT Logging :  KnowledgeBase Response : : {final_clean_output}")      
      ## Copy the results to      
    lstr_plain_string = "AI CHATBOT File Logging :  RESULTS of KnowledgeBase   :  " + query
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "AI CHATBOT AI CHATBOT Logging : Knowledge Base Results"
    append_to_chatbot_file_string(final_clean_output)
    

         
    
    ## Execute and run the Evaluaton Check 
    print("AI CHATBOT  :  Calling the Evaluation Agent")
    ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Evaluation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT  : Calling Evaluation Agent Now for query {query}")    
    final_Evaluation_response = run_evaluation_agent(query,response_string)
    print(final_Evaluation_response)
    logging.info(f"AI CHATBOT  : Evaluation Check  Result : {final_Evaluation_response}")  
    
    ## Copy the results to Output File
    append_to_chatbot_file_string(final_Evaluation_response) 


    ## Execute the PII Check 
    print("AI CHATBOT : Calling the PII Agent")
        ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the PII Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT : Calling PII  Agent Now for query {query}")
    final_PII_Check_response = run_PII_check(query,response_string)
    print(final_PII_Check_response)
    logging.info(f"AI CHATBOT : PII Check  Result : {final_PII_Check_response}")
    
    ## Copy the results to Output File
    append_to_chatbot_file_string(final_PII_Check_response) 

    ##Check it there is a need for Escalation for the above query
    print("AI CHATBOT :Calling the Escalation Agent")
        ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Escalation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT : Calling Escalation Agent Now for query {query}")    
    final_escalation_response = run_escalate_agent(query,response_string)
    print(final_escalation_response)
    logging.info(f"AI CHATBOT : Escalation Agent Results : {final_escalation_response}")           

     ## Copy the results to Output File
    append_to_chatbot_file_string(final_escalation_response)   
    
    end_time =  str(datetime.now())    
    lstr_plain_string = end_time + " :  AI CHAT BOT FOR Shippment QUERY COMPLETED : " + query   
    append_to_chatbot_file_string(lstr_plain_string) 
    

    return "SUCCESS"


def refund_status(order_id):
    logging.info("Routing to check REFUND Status")
    # result = f"Checking Refund Status for {order_id}"
    query = "give me refund status for Order_Id =  " + order_id
    
    start_time = str(datetime.now()) 
    lstr_plain_string = start_time + " :  AI CHAT BOT ORDER QUERY : " + query   
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
    
    
    response_json = search_knowledge_base_records(input_query=query)
    print(response_json)
    clean_json = json.loads(response_json)
    clean_output = json.dumps(clean_json)        
    print("\n")         
    print(f"Response String CLEAN  :  {clean_output} " )
    print("\n")   
    logging.info("AI CHATBOT  :  Response : %s", json.dumps(clean_output, indent=4))
     # Convert JSON object to JSON string
    response_string = json.dumps(response_json, indent=4)            
    print(response_string)              
    
       ## Knowledge Base Search to copy the Records are logged to the log file and CHAT BOT File.
    #clean_output = json.dumps(response_json, separators=(",", ":"))
    final_clean_output = json.dumps(clean_json)   
    print("\n")         
    print(f"Response String CLEAN  # 2 :  {final_clean_output} " )
    print("\n")     
    # Log JSON without \n characters (use safe f-string to avoid percent-formatting issues)
    logging.info(f"AI CHATBOT Logging : Search KnowledgeBase Response : {final_clean_output}")    
    logging.info(f"AI CHATBOT Logging :  KnowledgeBase Response : : {final_clean_output}")      
      ## Copy the results to      
    lstr_plain_string = "AI CHATBOT File Logging :  RESULTS of KnowledgeBase   :  " + query
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "AI CHATBOT AI CHATBOT Logging : Knowledge Base Results"
    append_to_chatbot_file_string(final_clean_output)
    
    
        
    ## Execute and run the Evaluaton Check 
    print("AI CHATBOT  :  Calling the Evaluation Agent")
        ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Evaluation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT  : Calling Evaluation Agent Now for query {query}")    
    final_Evaluation_response = run_evaluation_agent(query,response_string)
    print(final_Evaluation_response)
    logging.info(f"AI CHATBOT  : Evaluation Check  Result : {final_Evaluation_response}")  
    
     ## Copy the results to Output File
    append_to_chatbot_file_string(final_Evaluation_response) 
    
    
    ## Execute the PII Check 
    print("AI CHATBOT : Calling the PII Agent")
        ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the PII Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT : Calling PII  Agent Now for query {query}")
    final_PII_Check_response = run_PII_check(query,response_string)
    print(final_PII_Check_response)
    logging.info(f"AI CHATBOT : PII Check  Result : {final_PII_Check_response}")
    
    ## Copy the results to Output File
    append_to_chatbot_file_string(final_PII_Check_response) 

    ##Check it there is a need for Escalation for the above query
    print("AI CHATBOT :Calling the Escalation Agent")
        ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Escalation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT : Calling Escalation Agent Now for query {query}")    
    final_escalation_response = run_escalate_agent(query,response_string)
    print(final_escalation_response)
    logging.info(f"AI CHATBOT : Escalation Agent Results : {final_escalation_response}")     
    
    ## Copy the results to Output File
    append_to_chatbot_file_string(final_escalation_response)       

    end_time =  str(datetime.now())    
    lstr_plain_string = end_time + " :  AI CHAT BOT Refund QUERY COMPLETED : " + query   
    append_to_chatbot_file_string(lstr_plain_string) 

    return "SUCCESS"


def products_by_user(user_name):
    logging.info("Routing to check Product by User")
    # result = f"Fetching Products purchased by {user_name}"
    query = "give me products purchased by user_name =  " + user_name
    
    start_time = str(datetime.now()) 
    lstr_plain_string = start_time + " :  AI CHAT BOT ORDER QUERY : " + query    
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)

    response_json = search_knowledge_base_records(input_query=query)
    print(response_json)
    clean_json = json.loads(response_json)
    clean_output = json.dumps(clean_json)        
    print("\n")         
    print(f"Response String CLEAN  :  {clean_output} " )
    print("\n")   
    logging.info("AI CHATBOT  :  Response : %s", json.dumps(clean_output, indent=4))
     # Convert JSON object to JSON string
    response_string = json.dumps(response_json, indent=4)            
    print(response_string)              
    
       ## Knowledge Base Search to copy the Records are logged to the log file and CHAT BOT File.
    #clean_output = json.dumps(response_json, separators=(",", ":"))
    final_clean_output = json.dumps(clean_json)   
    print("\n")         
    print(f"Response String CLEAN  # 2 :  {final_clean_output} " )
    print("\n")     
    # Log JSON without \n characters (use safe f-string to avoid percent-formatting issues)
    logging.info(f"AI CHATBOT Logging : Search KnowledgeBase Response : {final_clean_output}")    
    logging.info(f"AI CHATBOT Logging :  KnowledgeBase Response : : {final_clean_output}")      
      ## Copy the results to      
    lstr_plain_string = "AI CHATBOT File Logging :  RESULTS of KnowledgeBase   :  " + query
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "AI CHATBOT AI CHATBOT Logging : Knowledge Base Results"
    append_to_chatbot_file_string(final_clean_output)
    
    
  
    
    
    ## Execute and run the Evaluaton Check 
    print("AI CHATBOT  :  Calling the Evaluation Agent")
    ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Evaluation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT  : Calling Evaluation Agent Now for query {query}")    
    final_Evaluation_response = run_evaluation_agent(query,response_string)
    print(final_Evaluation_response)
    logging.info(f"AI CHATBOT  : Evaluation Check  Result : {final_Evaluation_response}")  
    
      ## Copy the results to Output File
    append_to_chatbot_file_string(final_Evaluation_response) 
    
    ## Execute the PII Check 
    print("AI CHATBOT : Calling the PII Agent")
    ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the PII Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT : Calling PII  Agent Now for query {query}")
    final_PII_Check_response = run_PII_check(query,response_string)
    print(final_PII_Check_response)
    logging.info(f"AI CHATBOT : PII Check  Result : {final_PII_Check_response}")
    
      ## Copy the results to Output File
    append_to_chatbot_file_string(final_PII_Check_response) 

    ##Check it there is a need for Escalation for the above query
    print("AI CHATBOT :Calling the Escalation Agent")
    ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Escalation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT : Calling Escalation Agent Now for query {query}")    
    final_escalation_response = run_escalate_agent(query,response_string)
    print(final_escalation_response)
    logging.info(f"AI CHATBOT : Escalation Agent Results : {final_escalation_response}")           

       ## Copy the results to Output File
    append_to_chatbot_file_string(final_escalation_response) 
    
    end_time =  str(datetime.now())    
    lstr_plain_string = end_time + " :  AI CHAT BOT Product QUERY COMPLETED : " + query   
    append_to_chatbot_file_string(lstr_plain_string) 

    return "SUCCESS"


def orders_by_user(user_name):
    logging.info("Routing to check ORDERS placed by User")
    # result = f"Fetching Orders placed by {user_name}"
    query = "give me order details for user_name =  " + user_name
    
    start_time = str(datetime.now()) 
    lstr_plain_string = start_time + " :  AI CHAT BOT ORDER QUERY : " + query   
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
    
    response_json = search_knowledge_base_records(input_query=query)
    print(response_json)
    clean_json = json.loads(response_json)
    clean_output = json.dumps(clean_json)        
    print("\n")         
    print(f"Response String CLEAN  :  {clean_output} " )
    print("\n")   
    logging.info("AI CHATBOT  :  Response : %s", json.dumps(clean_output, indent=4))
     # Convert JSON object to JSON string
    response_string = json.dumps(response_json, indent=4)            
    print(response_string)    
    
     ## Knowledge Base Search to copy the Records are logged to the log file and CHAT BOT File.
    #clean_output = json.dumps(response_json, separators=(",", ":"))
    final_clean_output = json.dumps(clean_json)   
    print("\n")         
    print(f"Response String CLEAN  # 2 :  {final_clean_output} " )
    print("\n")     
    # Log JSON without \n characters (use safe f-string to avoid percent-formatting issues)
    logging.info(f"AI CHATBOT Logging : Search KnowledgeBase Response : {final_clean_output}")    
    logging.info(f"AI CHATBOT Logging :  KnowledgeBase Response : : {final_clean_output}")      
      ## Copy the results to      
    lstr_plain_string = "AI CHATBOT File Logging :  RESULTS of KnowledgeBase   :  " + query
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "AI CHATBOT AI CHATBOT Logging : Knowledge Base Results"
    append_to_chatbot_file_string(final_clean_output)
    
    ## Execute and run the Evaluaton Check 
    print("AI CHATBOT  :  Calling the Evaluation Agent")
    ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Evaluation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT  : Calling Evaluation Agent Now for query {query}")    
    final_Evaluation_response = run_evaluation_agent(query,response_string)
    print(final_Evaluation_response)
    logging.info(f"AI CHATBOT  : Evaluation Check  Result : {final_Evaluation_response}")  
    
       ## Copy the results to Output File
    append_to_chatbot_file_string(final_Evaluation_response) 
    
    ## Execute the PII Check 
    print("AI CHATBOT : Calling the PII Agent")
    ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the PII Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT : Calling PII  Agent Now for query {query}")
    final_PII_Check_response = run_PII_check(query,response_string)
    print(final_PII_Check_response)
    logging.info(f"AI CHATBOT : PII Check  Result : {final_PII_Check_response}")
    
         ## Copy the results to Output File
    append_to_chatbot_file_string(final_PII_Check_response) 

    ##Check it there is a need for Escalation for the above query
    print("AI CHATBOT :Calling the Escalation Agent")
    ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Escalation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT : Calling Escalation Agent Now for query {query}")    
    final_escalation_response = run_escalate_agent(query,response_string)
    print(final_escalation_response)
    logging.info(f"AI CHATBOT : Escalation Agent Results : {final_escalation_response}")    
    
          ## Copy the results to Output File
    append_to_chatbot_file_string(final_escalation_response)        
    
    end_time =  str(datetime.now())    
    lstr_plain_string = end_time + " :  AI CHAT BOT ORDER QUERY COMPLETED : " + query   
    append_to_chatbot_file_string(lstr_plain_string) 


    return "SUCCESS"


def billing_details(order_id):
    logging.info("Routing to check Billing Details")   

    query = "I have billing related issues please help escalate further for Order_Id  = " + order_id
    

    ## Directly escalate further for Billing Issues as this is a critical issue which needs to be resolved on priority.
    ## Searching Pinecone data will not help it will be Human Agent Intervention which can resolve the issue and provide better customer experience.
    
    start_time = str(datetime.now()) 
    lstr_plain_string = start_time + " :  AI ChatBOT for Billing related Issues  : " + query   
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
                  
    query = "I have billing related issues please help escalate further for Order_Id  = " + order_id
    response_string = {"status": "NOT_FOUND", "message": "Billing Related Issue needs to be escalated to Human Agent"}
    
    ##Check it there is a need for Escalation for the above query
    print("AI CHATBOT :Calling the Escalation Agent For Billing Issues")
       ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Esalation Agent (Billing Issues)  :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    logging.info(f"AI CHATBOT : Calling Escalation Agent Now for query {query}")    
    final_escalation_response = run_escalate_agent(query,response_string)
    print(final_escalation_response)
    logging.info(f"AI CHATBOT : Escalation Agent Results : {final_escalation_response}")           

    ## Copy the results to Output File
    append_to_chatbot_file_string(final_escalation_response) 
    
    
    end_time =  str(datetime.now())    
    lstr_plain_string = end_time + " :  AI CHAT BOT (Billing Issues) COMPLETED : " + query   
    append_to_chatbot_file_string(lstr_plain_string) 
    
    

    return "SUCCESS"


def login_issue(user_name):
    logging.info("Routing to check Login Issues Status Query")
    result = f"Handling Login Issue for {user_name}"
    query = "I have login related issues please help  for  User  " + user_name
           
    ## Directly Escalate furtther for Login Issues as this is a critical issue which needs to be resolved on priority.
    
    start_time = str(datetime.now()) 
    query = "I have login related issues please help  for  User  " + user_name
    response_string = {"status": "NOT_FOUND", "message": "Login Related Issue needs to be escalated to Human Agent"}
    
    lstr_plain_string = start_time + " :  Escalating for Login Issues : " + query   
    append_to_chatbot_file_string(lstr_plain_string)
    lstr_plain_string = "=========================================================="
    append_to_chatbot_file_string(lstr_plain_string)
    
    ## Directly escalate further 
    print("AI ChatBOT : Calling the Escalation Agent")
       ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Escalation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    lstr_plain_string = "AI CHATBOT  :  Calling the Escalation Agent   :  " + query
    append_to_chatbot_file_string(lstr_plain_string)    
    logging.info(f"Calling Escalation Agent Now for query {query}")    
    final_escalation_response = run_escalate_agent(query,response_string)
      
    
      ## Copy the results to 
    append_to_chatbot_file_string(final_escalation_response)
    
    print(final_escalation_response)
    logging.info(f"Escalation Agent :  Check  Result : {final_escalation_response}")
    
    end_time =  str(datetime.now())    
    lstr_plain_string = end_time + " : Escalating for Login Issues(COMPLETED) : " + query   
    append_to_chatbot_file_string(lstr_plain_string) 
    
    
    return "SUCCESS"


def password_issue(user_name):
    logging.info("Routing to check Login Issues to check Password details")
    result = f"Handling Password Issue for {user_name}"
    query = "I have password related issues user is " + user_name
    start_time = str(datetime.now()) 
    query = "I have password related issues user is " + user_name
    response_string = {"status": "NOT_FOUND", "message": "Password Related Issue needs to be escalated to Human Agent"}
    lstr_plain_string = start_time + " :  Escalating for Password Issues : " + query  
    append_to_chatbot_file_string(lstr_plain_string)
    
    
    ## Directly escalate further 
    print("AI ChatBOT : Calling the Escalation Agent")    
    lstr_plain_string = "AI CHATBOT  :  Calling the Escalation Agent For Password Related Issues  :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    
     ##=======================================
    ##Log this to file which agent is called.
    lstr_plain_string = "AI CHATBOT File Logging  :  Calling the Escalation Agent For Password Related Issues  :  " + query
    append_to_chatbot_file_string(lstr_plain_string)
    ##=======================================
    
    logging.info(f"Calling Escalation Agent Now for  For Password Related Issues  : query {query}")    
    final_escalation_response = run_escalate_agent(query,response_string)
    print(final_escalation_response)
    logging.info(f"Escalation Agent :  For Password Related Issues (COMPLETED) : {final_escalation_response}")    
     ## Copy the results to Output File
    append_to_chatbot_file_string(final_escalation_response)   
 
    
    end_time =  str(datetime.now())    
    lstr_plain_string = end_time + " :   For Password Related Issues(COMPLETED) : " + query   
    append_to_chatbot_file_string(lstr_plain_string) 
    
    

    return "SUCCESS"


# =====================================================
# MAIN ROUTER FUNCTION

## This is the CHATBOT routing logic
# =====================================================

def route_customer_support():

    print("\n========== CUSTOMER SUPPORT AI CHATBOT MENU ==========\n")
    print("Option #1 : Order Status Enquiry")
    print("Option #2 : Order Shipping Status Enquiry")
    print("Option #3 : Order Refund Status Enquiry")
    print("Option #4 : Products purchased by User")
    print("Option #5 : Orders placed by User")
    print("Option #6 : Billing Details Query")
    print("Option #7 : Login Related Issues")
    print("Option #8 : Password Related Issues")
    print("Option #9  : REFUND POLICY ")
    print("Option #10 : CANCELLATION POLICY")
    print("Option #11 : Please ask any other question ")
    print("Option #12 : Exit or Quit")

    option = input("\nPlease Select Option (1-11): ").strip()

    # =================================================
    # OPTION 1
    # =================================================

    if option == "1":

        order_id = input("Enter Order_ID (OXXX): ")

        result = order_status(order_id)

        print("AI CHATBOT :  Function Result :", result)

        return result

    # =================================================
    # OPTION 2
    # =================================================

    elif option == "2":

        order_id = input("Enter Order_ID (OXXX): ")

        result = shipment_status(order_id)

        print("AI CHATBOT :  Function Result :", result)

        return result

    # =================================================
    # OPTION 3
    # =================================================

    elif option == "3":

        order_id = input("Enter Order_ID (OXXX): ")

        result = refund_status(order_id)

        print("AI CHATBOT :  Function Result :", result)

        return result

    # =================================================
    # OPTION 4
    # =================================================

    elif option == "4":

        user_name = input("Enter User_Name: ")

        result = products_by_user(user_name)

        print("AI CHATBOT :  Function Result :", result)

        return result

    # =================================================
    # OPTION 5
    # =================================================

    elif option == "5":

        user_name = input("Enter User_Name: ")

        result = orders_by_user(user_name)

        print("AI CHATBOT :  Function Result :", result)

        return result

    # =================================================
    # OPTION 6
    # =================================================

    elif option == "6":

        order_id = input("Enter Order_ID (OXXX): ")

        result = billing_details(order_id)

        print("AI CHATBOT :  Function Result :", result)

        return result

    # =================================================
    # OPTION 7 - Login Related Issues
    # =================================================

    elif option == "7":

        user_name = input("Enter User_Name: ")

        result = login_issue(user_name)

        print("AI CHATBOT :  Function Result :", result)

        return result

    # =================================================
    # OPTION 8  (Password Related Issues)
    # =================================================

    elif option == "8":

        user_name = input("Enter User_Name: ")

        result = password_issue(user_name)

        print("AI CHATBOT :   Function Result :", result)

        return result
    # =================================================
    # OPTION 9
    # =================================================
    elif option == "9":
        ## Use the Tools calling Agent to use the tools and get the results for the above query. 
        query = "Show me Refund Policy"
        tools_execution_response = call_tools(query)        
        print("AI CHATBOT :   Result :", tools_execution_response)
        result = tools_execution_response

        return result
    
    # =================================================
    # OPTION 10
    # =================================================
    elif option == "10":

        query = "Show me Cancellation Policy"
        ## Use the Tools calling Agent to use the tools and get the results for the above query. 
                
        tools_execution_response = call_tools(query)        
        print("AI CHATBOT :   Result :", tools_execution_response)
        result = tools_execution_response
        return result
        
                
    # =================================================
    # OPTION 11
    # =================================================

      # =================================================
    # OPTION 11
    # =================================================
    elif option == "11":
        ## This will call and TEST multi Agents using CrewAI
        ## If any other question is asked
        print("AI CHATBOT :   OTHER QUERIES Executed :")
        result_cyber_threat_PII_response = run_multi_agent()         
        
        return result_cyber_threat_PII_response
    
    elif option == "12":

        exit_option = input("Type exit/quit: ").lower()

        if exit_option in ["exit", "quit"]:

            print("AI CHATBOT :  Exiting CHATBOT Application...")               
            lstr_plain_string = "=========================================================="
            append_to_chatbot_file_string(lstr_plain_string)   
            lstr_plain_string = "AI CHATBOT :  Exiting CHATBOT Application..." 
            append_to_chatbot_file_string(lstr_plain_string)   
            lstr_plain_string = "=========================================================="
            append_to_chatbot_file_string(lstr_plain_string)   
            lstr_plain_string = "=========================================================="
            

            return "EXIT"

    else:

        print("AI CHATBOT :  Invalid Option Selected")

        return "EXIT"


# =====================================================
# CALL FUNCTION
# =====================================================

##Use a chat Bot like interface to interact with the agent and test it out   
def main() -> None:    
    while True:
        result = route_customer_support()
        if result == "EXIT":
            break    
    return 

## The main function

if __name__ == "__main__":
    main()
    
        