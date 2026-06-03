## Rajendra Bichu : Date : 15.05.2026 , Version 1.0

## Customer Support — AI Support Escalate agent , Escalate to Customer Support/ Humans whenever required
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

file_name = os.path.join(logs_directory_path, "agent_esclation_LOG.log") 

logging.basicConfig(
    filename=file_name,
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True
)

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

##Define Evaluation AGent

## Escalation AGent 
escalation_agent = build_agent(

    role="Enterprise Human Escalation and Customer Support Manager",

    goal="""
    Intelligently evaluate customer interactions and determine whether
    escalation to human customer support, refund operations,
    technical support, fraud team, or compliance team is required.

    Validate if escalation is required for the following: Query: {query}
    Validate the provided JSON data against the user query.
    ONLY use:
    -  actual customer query {query} to esclate further    
    -  JSON response {json_data} to esclate further
    

    Evaluate JSON data for the following conditions.
    
    IF NOT_FOUND is there in the response :
    - Check for Ticket Number or Ticket Status if information is found then mark ticket_or_callback_provided = YES , in structured JSON output
    - Check for User Guidance has some information then  mark customer_guidance_provided = YES,, in structured JSON output
    - Check for Expected SLA has some information then  mark callback_status = YES, in structured JSON output
    - Check for callback status has some information then  mark expected_sla as in the json_data , in structured JSON output


    Provide complete escalation workflows including:
    - support contact details
    - callback handling
    - ticket generation
    - SLA priority
    - escalation reasons
    - customer next steps

    Always return structured JSON output.
    """,

    backstory="""
    
    Enterprise escalation and customer support specialist responsible for handling refund, shipment, login, payment, fraud, and account-related issues.
    Escalate high-risk cases involving failed refunds, delivery failures, fraud, PII exposure, unauthorized access, or security incidents.
    Assign escalation team, severity, SLA priority, ticket number, callback workflow, and customer support channels while ensuring privacy and compliance-safe handling.
    Priority Levels:
    - CRITICAL: Fraud, account takeover, security incidents
    - HIGH: Refund disputes, login failures, delivery failures
    - MEDIUM: Shipment delays, billing clarification
    - LOW: General informational requests

    Always provide escalation status, support contact details, ticket information, expected SLA, and next customer actions.

    
    

    Never expose internal confidential information.
    """,

    llm=llm,
    verbose= False 
)




## Define the Tasks here we can add expected_output for better clarity on what each task should return 

escalation_task = build_task(

    description="""
    Analyze the customer interaction and determine whether escalation
    to human customer support, refund operations, technical support,
    fraud team, or compliance team is required.

    --------------------------------------------------
    ESCALATION CONDITIONS
    --------------------------------------------------

    Automatically escalate if the query involves:

    CUSTOMER SUPPORT:
    - Refund status
    - Refund delays
    - Refund failures    
    - Login problems
    - Account lockout
    - Delivery not received
    - Missing shipment
    - Payment dispute
    - Fraud complaint
    - Identity verification

    COMPLIANCE / SECURITY:
    - Multiple PII detections
    - Financial information exposure
    - Security concerns
    - Unauthorized access attempts
    - Fraud indicators

    --------------------------------------------------
    REQUIRED ACTIONS
    --------------------------------------------------

    Determine:
    - Escalation required or not
    - Escalation team
    - Severity level
    - Priority
    - Recommended action
    - Customer callback eligibility
    - SLA target

    Generate:
    - Ticket ID
    - Support email
    - Toll free number
    - Callback confirmation
    - Tracking reference

    --------------------------------------------------
    RESPONSE REQUIREMENTS
    --------------------------------------------------

    - Always return JSON only
    - Always explain escalation reason
    - Always include customer next steps
    - Never expose sensitive data
    - Ensure compliance-safe outputs
    - Always provide a confidence score

    -----------------------------------------------------------
    PII related issues observed 

	Escalate automatically if:
	    - HIGH risk detected
	    - Multiple PII entities found
	    - Financial data detected
	    - Fraud indicators detected
	    - User requests sensitive account actions
	    - AI confidence is LOW

    """,

    agent=escalation_agent,

    expected_output="""
    {

      "customer_query_type": "ORDER | PRODUCT | REFUND | SHIPMENT | LOGIN | POLICY RELATED| PASSWORD RELATED ",
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
      "customer_support_email": "customer_care@support.com",      
      "Toll Free Number ": "1800-0011-011",
      "escalation_required": "TRUE/FALSE",
      "escalation_category":  " CUSTOMER_SUPPORT | TECH_SUPPORT | REFUND_TEAM | FRAUD_TEAM | COMPLIANCE_TEAM",
      "escalation_team": "",
      "priority": "LOW | MEDIUM | HIGH | CRITICAL",
      "reason": "",
      "detected_issue_type": "REFUND_ISSUE | LOGIN_ISSUE | ORDER_NOT_FOUND | NOT_FOUND | REFUND_ISSUE | DELIVERY_ISSUE | FRAUD | PII_RISK | PAYMENT_DISPUTE",
      "recommended_action": "",
      "ticket_generated": true,
      "ticket_id": "",
      "customer_callback_required": true,
      "callback_status": "REQUESTED | SCHEDULED | NOT_REQUIRED",
      "expected_sla":  "24_HOURS | 48_HOURS | 72_HOURS | IMMEDIATE",
      "customer_support_contact": {
        "support_email": "customer_care@support.com",  "toll_free_number": "1800-000-0001","support_hours": "24x7"
      },
      "next_steps": [],
      "compliance_safe": true
      
      "evaluation_metrics": {

        "accuracy": {
        "score": [1-5] ,
        "reason": ""
        },

        "safety": {
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

        "hallucination": {
        "detected": false,
        "reason": ""
        },

        "groundedness": {
        "score": [1-5] ,
        "reason": ""
        },

        "escalation_correct": {
        "value": "TRUE/FALSE",      "reason": ""
        },

     "confidence_score": [0-9]
     
    }
    """
)






# ============================================================
# Escalation TASK
# ============================================================



def run_escalate_agent(query: str, json_string: str):
    crew_escalate = Crew(
        agents=[escalation_agent],
        tasks=[escalation_task],
        verbose=False,
    )
    
    
    with get_openai_callback() as cb:

            result = crew_escalate.kickoff(
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
            logging.info("Escalation Agent : Total Tokens Used = " + str(cb.total_tokens))
            logging.info("Escalation Agent  : Prompt Tokens = " + str(cb.prompt_tokens))
            logging.info("Escalation Agent  : Completion Tokens = " + str(cb.completion_tokens)) 
            
            token_usage = {
                "prompt_tokens": cb.prompt_tokens,
                "completion_tokens": cb.completion_tokens,
                "total_tokens": cb.total_tokens
            }

            logging.info("Escalation Agent Token Usage : " + str(token_usage))            
            
    return result 
    