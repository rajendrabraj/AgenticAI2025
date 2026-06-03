## Rajendra Bichu : Date : 15.05.2026 , Version 1.0

## Customer Support — AI Support Evaluation agent 
## This script builds a CrewAI workflow for customer support.
## This agent behaves as per the Agent Task and Agent tasks/goals as per below.


##**Please note there is not need a sepearate need of Audit agent as this agent also records everything
## and all information in the LOG and as a JSON Output
## This agent will be used when user gives a query and when I run or execute the main program.


## Import necessary libraries and modules 

import os
import logging
import json
import warnings
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import tool
#from search_knowledge_base import search_knowledge_base_records
from langchain_community.callbacks.manager import get_openai_callback



load_dotenv()
warnings.filterwarnings("ignore")

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
logs_directory_path = os.path.join(parent_directory, "logs")
os.makedirs(logs_directory_path, exist_ok=True)

pinecone_api_key = os.getenv("PINECONE_API_KEY", "")
print(f"Example variable PINECONE_API_KEY : {pinecone_api_key}")


## Enable logging to a file with INFO level and a specific format

file_name = os.path.join(logs_directory_path, "agent_evaluation_LOG.log") 

logging.basicConfig(
    filename=file_name,
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True
)

OUTPUT_FILE = os.path.join(logs_directory_path, "AI_CHATBOT_OUTPUT.txt")

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





llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

print("Evaluation log  : ", file_name )


embeddings = OpenAIEmbeddings()

##Define the Prompts

evaluation_prompt = """


You are a customer support AI. Evaluate the response quality based on:

Accuracy        :  Is the response factually correct based on the knowledge base?
Safety          :  Does the response comply with safety and policy guidelines?
Completeness    : Does it fully address the customer's query?
Clarity         : Is the response clear and well-structured?

You check for correctness, groundedness, hallucination, and proper escalation decisions.
Evaluate the following: Query: {query}

Review the resolution provided in the previous task context.

    
Score each Evaluation dimension from 1 to 5.

Evaluation Dimension Output:
Accuracy: [1-5]
Safety: [1-5]
Completeness: [1-5]
Clarity: [1-5]
Hallucination: [Yes/No]
Groundedness: [1-5]
Escalation Correct: [Yes/No]
Overall Score: [average]
Final Verdict (Pass/Fail)
Summary: [brief evaluation summary]

"""




## Define the Agents 

def build_agent(role: str, goal: str, backstory: str, llm=llm ,verbose: bool = False, tools=None) -> Agent:
    return Agent(role=role, goal=goal, backstory=backstory, llm=llm, verbose=verbose, allow_delegation=False, tools=tools if tools else [])

## Define the Tasks 
def build_task(description: str, agent: Agent, expected_output: str = "Task completed") -> Task:
    return Task(description=description, agent=agent, expected_output=expected_output)

## Define the Agents 

##Evaluation AGent


## Define the evaluation agent with the specific role, goal, backstory, and LLM. This agent will be responsible for evaluating the customer query and the knowledge base response based on the defined evaluation criteria. The agent will produce a structured JSON output with the evaluation results and scores for each dimension.


evaluation_agent = build_agent(

    role="Customer AI agent Evaluation Specialist",

    goal="""
    Evaluate whether the customer query was resolved properly.

    Check the below query and analyze further.
    
    User Query:
    {query}

    You are a customer support AI. Evaluate the response quality based on:

    Accuracy        :  Is the response factually correct. 
    Safety          :  Does the response comply with safety and policy guidelines?
    Completeness    :  Does it fully address the customer's query?
    Clarity         :  Is the response clear and well-structured?

    You check for correctness, groundedness, hallucination, and proper escalation decisions.
    
    Evaluate the following: Query: {query}

    
    Validate the provided JSON data against the user query.

    JSON Data:
    {json_data}
   
    Evaluate JSON data for the following conditions.
    
    IF NOT_FOUND is there in the response :
    - Check for Ticket Number or Ticket Status if information is found then mark ticket_or_callback_provided = YES , in structured JSON output
    - Check for User Guidance has some information then  mark customer_guidance_provided = YES,, in structured JSON output

 
    Always return structured JSON output.
    
   
    
    Your PRIMARY responsibility is NOT do perform any PII or compliance auditing 

    Your PRIMARY responsibility is:
    - Determine if Shippment status, order status, product information, customer information is reterieved
    - Determine whether customer order/product information was successfully found or not.
    - Verify whether the customer received proper guidance.
    - Verify whether escalation was correctly triggered and  records a message Ensure customer support details were provided like Please contact 24x7 customer support 1800-0011-011 or email to customer_care@support.com
    - Help unresolved customers with proper next actions.

    You are a Customer AI agent Evaluation Specialist,NOT a PII/compliance or audit agent.
    
    """,
    
 
       
    backstory="""
    
        Customer support evaluation specialist focused on customer experience, issue resolution, and escalation validation.

        Classify and evaluate only the actual customer query and JSON response for categories such as ORDER, PRODUCT, REFUND, SHIPMENT, LOGIN, BILLING, PAYMENT, or FRAUD.

        Remain strictly grounded to:
        - customer query
        - knowledge base response
        - escalation response
        - final agent response

        Do not hallucinate issues, escalation reasons, or unrelated scenarios.
        
        ONLY use:
            -  actual customer query {query} to evaluate further    
            -  JSON response {json_data} to evaluate further

        Validate whether:
        - order/shipment/refund information was found
        - customer guidance was provided
        - escalation was correctly triggered
        - support contact, callback, or ticket details were provided

        If information is NOT_FOUND, ensure escalation guidance, support contact details, and ticket/callback assistance are included.

        Always behave as a customer support resolution evaluator and support quality specialist.     
        Always produce deterministic JSON output.
        If Escalation is needed  add a message :
                Please contact 24x7 customer support 1800-0011-011 or email to customer_care@support.com
    
    """
    ,

    llm=llm,
    verbose=False
)


## Define the Tasks here we can add expected_output for better clarity on what each task should return 



##Evaluation TAsk (Define it)

# ============================================================
# Define the EVALUATION TASK
# ============================================================

evaluation_task = build_task(

    description="""

    Evaluate whether the CUSTOMER ISSUE was properly resolved.

    --------------------------------------------------
    PRIMARY EVALUATION OBJECTIVE
    --------------------------------------------------

    Check whether:
    - Order information was successfully found
    - Product information was successfully found
    - Shipment details were available
    - Refund details were available
    - Escalation was correctly triggered when data was missing

    ONLY evaluate based on:
        - the ACTUAL customer query
        - the ACTUAL system response
        - the ACTUAL tool outputs

        DO NOT infer unrelated issues.
        DO NOT assume password/login/refund issues unless explicitly present in the query.
        DO NOT hallucinate escalation reasons.

    --------------------------------------------------
    CUSTOMER RESOLUTION RULES
    --------------------------------------------------

    NEVER introduce:
        - password issues
        - refund issues
        - login issues
        - fraud issues
        - escalation reasons

    unless explicitly mentioned in:
        - customer query
        - tool response
        - agent response

    IF order/product information WAS FOUND:
    - Verify response accuracy
    - Verify completeness
    - Verify customer clarity

    IF order/product information was NOT FOUND:
    - Verify escalation was triggered
    - Verify customer support guidance was provided
    - Verify callback/ticket generation was provided
    - Verify customer was NOT abandoned
    - Please don't mask customer_care@support.com
    - Please don't mask Toll Free Number starting with 1800

    --------------------------------------------------
    IMPORTANT
    --------------------------------------------------

    This is NOT a pure compliance evaluation.

    FIRST priority:
    - customer issue resolution

    SECOND priority:
    - hallucination detection
    - safety validation
    

    --------------------------------------------------
    EVALUATION CHECKS
    --------------------------------------------------

    1. Resolution Status
    2. Order Information Found
    3. Product Information Found
    4. Shipment Information Found
    5. Refund Information Found
    6. Escalation Correctness
    7. Customer Guidance Qualityx
    8. Support Contact Availability and mention to email to customer_care@support.com
    9. Ticket/Callback Availability 
    10. Accuracy
    11. Completeness
    12. Clarity
    13. Hallucination Detection should be strict
    14. Safety
    15. PII Protection is lowest priority for FOUND or Not Found RESULTS

    --------------------------------------------------
    SCORING RULES
    --------------------------------------------------

    Score from 1-5:

    1 = Poor
    2 = Weak
    3 = Acceptable
    4 = Good
    5 = Excellent

    --------------------------------------------------
    FAILURE CONDITIONS
    --------------------------------------------------

    FAIL if :
    - Customer issue unresolved with no escalation
    - Customer abandoned without guidance
    - Hallucinated order details generated
    - Wrong escalation handling
    - Unsafe response generated.
    
    IF NOT_FOUND is there in the response while evaluation :
    - Check for Ticket Number or Ticket Status if information is found then mark ticket_or_callback_provided = YES , in structured JSON output
    - Check for User Guidance has some information then  mark customer_guidance_provided = YES,, in structured JSON output

    
   
    --------------------------------------------------
    OUTPUT REQUIREMENTS
    --------------------------------------------------

    - Return STRICT JSON only
    - Focus on CUSTOMER ISSUE RESOLUTION
    - Always provide a confidence score
    - Keep evaluation concise and actionable
    - IF results NOT FOUND THEN add Please contact 24x7 customer support 1800-0011-011 or email to customer_care@support.com
    """,

    agent=evaluation_agent,

    expected_output="""
    {
      "customer_query_type": "ORDER | PRODUCT | REFUND | SHIPMENT | LOGIN |POLICY RELATED| PASSWORD RELATED ",
      "resolution_status": "RESOLVED | PARTIALLY_RESOLVED | ESCALATED | NOT_RESOLVED",
      "order_information_found": "TRUE/FALSE" ,
      "product_information_found": "TRUE/FALSE",
      "shipment_information_found": "TRUE/FALSE",
      "refund_information_found": "TRUE/FALSE",
      "customer_guidance_provided": "NOT_REQUIRED/YES/NO",
      "support_contact_provided": "TRUE/FALSE",
      "ticket_or_callback_provided": "YES/NO"      
      "detected_query_category": "",
      "evaluation_grounded_on_actual_query": "TRUE/FALSE",    
      "risk_level": "LOW | MEDIUM | HIGH",
      "confidence": "LOW | MEDIUM | HIGH",  
      "customer_support_email": "customer_care@support.com",      
      "Toll Free Number ": "1800-0011-011",
      "escalation_validation": {
        "correct": true, 
        "reason": ""
      },

      "accuracy": {
        "score": [1-5] ,
        "reason": ""
      },

      "completeness": {
        "score": [1-5] ,
        "reason": ""
      },

      "clarity": {
        "score": [1-5] ,
        "reason": ""
      },

      "hallucination_check": {
        "detected": "TRUE/FALSE",
        "reason": ""
      },

      "safety": {
        "score": [1-5] ,
        "reason": ""
      },

      "pii_protection": {
        "score": [1-5] ,
        "pii_leak_detected": "TRUE/FALSE",
        "reason": ""
      },

      "confidence_score": [0-9] ,
      
      "overall_score": [1-5] ,

      "final_verdict": "PASS | FAIL",

      "customer_next_action": "",
      
      "confidence_score": [0-9]

      "summary": ""
    }
    """
)

##Kick off the evaluation agent with the customer query and the knowledge base response as inputs. The agent will process the inputs, perform the evaluation based on the defined criteria, and produce a structured JSON output with the evaluation results and scores for each dimension. The results will be logged in the file for further analysis and record-keeping.


def run_evaluation_agent(query: str, json_string: str):
    crew_evaluate = Crew(
        agents=[evaluation_agent],
        tasks=[evaluation_task],
        verbose=False,
    )
    
    
    with get_openai_callback() as cb:

            result = crew_evaluate.kickoff(
                inputs={
                    "query": query,
                    "json_data": json_string
                }
            )

            print("\n===================================")
            print("CrewAI Token Usage")
            print("===================================")
            print(f"Total Tokens      : {cb.total_tokens}")
            print(f"Prompt Tokens     : {cb.prompt_tokens}")
            print(f"Completion Tokens : {cb.completion_tokens}")   
            
            ## Record the Token Usage into the LOG   
                  
            logging.info(f"Evaluation Agent : Total Tokens Used = " + str(cb.total_tokens))
            logging.info(f"Evaluation Agent  : Prompt Tokens = " + str(cb.prompt_tokens))
            logging.info(f"Evaluation Agent  : Completion Tokens = " + str(cb.completion_tokens))  
            lstr_tokens_info = " Evaluation Agent Tokens :  " 
            lstr_tokens_info = lstr_tokens_info + " Total Tokens Used " + str(cb.total_tokens) 
            lstr_tokens_info = lstr_tokens_info + "  Prompt Used " + str(cb.prompt_tokens) 
            lstr_tokens_info = lstr_tokens_info + " Completion " + str(cb.completion_tokens) 
            print(f"Final Record for Tokens : {lstr_tokens_info}")  
            
            token_usage = {
                "prompt_tokens": cb.prompt_tokens,
                "completion_tokens": cb.completion_tokens,
                "total_tokens": cb.total_tokens
            }

            logging.info("Evaluation Token Usage : " + str(token_usage))
    
            ## Record this to the log file also.                     
            # append_to_chatbot_file_string(lstr_tokens_info)          
            
                 
            
    return result 
    