## Rajendra Bichu : Date : 15.05.2026 , Version 1.0

## Customer Support — AI Support Evaluation agent 
## This script builds a CrewAI workflow for customer support.
## This code defines to 2 functions as Tools and tries to call them and usage of TOOLS
## This agent will be used when user gives a query and when I run or execute the main program.


##Tools Defined 

# @tool("show_refund_policy")
# @tool("show_cancellation_policy")


##**Please note there is not need a sepearate need of Audit agent as this agent also records everything
## and all information in the LOG and as a JSON Output


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

from crewai.tools import tool

load_dotenv()
warnings.filterwarnings("ignore")

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
logs_directory_path = os.path.join(parent_directory, "logs")
os.makedirs(logs_directory_path, exist_ok=True)



## Enable logging to a file with INFO level and a specific format

file_name = os.path.join(logs_directory_path, "agent_TOOLS_Execution.log") 

logging.basicConfig(
    filename=file_name,
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

print("Agent TOOLS log  : ", file_name )


embeddings = OpenAIEmbeddings()

def show_refund_policy():

    refund_policy = """
    REFUND POLICY

    1. Customers can request a refund within 7 days of product delivery.
    2. Refunds are applicable only for damaged, defective, or incorrect products.
    3. Products must be returned in original condition with packaging intact.
    4. Refund requests are reviewed within 2 business days.
    5. Approved refunds are processed within 5-7 business days.
    6. Shipping charges are non-refundable unless the issue was caused by the seller.
    7. Refunds will be credited to the original payment method.
    8. Digital products and gift cards are non-refundable.
    9. Cancellation refunds may take additional processing time depending on the bank.
    10. For refund disputes, customers may contact customer support for escalation.
    """

    return refund_policy


def show_cancellation_policy():

    cancellation_policy = """
    CANCELLATION POLICY

    1. Customers can cancel orders before the product is shipped.
    2. Orders already shipped cannot be cancelled directly.
    3. Cancellation requests can be submitted through the customer portal.
    4. Refunds for cancelled orders are processed after cancellation approval.
    5. Some products may not be eligible for cancellation due to seller restrictions.
    6. Bulk or customized orders may incur cancellation charges.
    7. Cancellation confirmation will be sent via email or SMS.
    8. Payment gateway charges may not be refundable in certain cases.
    9. Failed or duplicate orders are automatically cancelled and refunded.
    10. Customers can contact support for urgent cancellation assistance.
    """

    return cancellation_policy


##Define the Toools

@tool("show_refund_policy")
def show_refund_policy_tool() -> str:
    """
    Returns Ecommerce Refund Policy
    """
    return show_refund_policy()


@tool("show_cancellation_policy")
def show_cancellation_policy_tool() -> str:
    """
    Returns Ecommerce Cancellation Policy
    """
    return show_cancellation_policy()


##Define the Prompts

###=======================================================================================================
# ============================================================
# INTENT PROMPT
# ============================================================

intent_prompt = """

You are an Ecommerce Customer Support AI Agent.

Your PRIMARY responsibility is to provide correct POLICY information
using ONLY the available tools.

--------------------------------------------------
AVAILABLE TOOLS and Executed 
--------------------------------------------------

1. show_refund_policy
   - Use ONLY when customer asks about:
        - REFUND POLICY
        - refund rules
        - refund terms
        - refund process

2. show_cancellation_policy
   - Use ONLY when customer asks about:
        - CANCELLATION POLICY
        - cancellation rules
        - cancel order policy
        - order cancellation process

--------------------------------------------------
TOOL EXECUTION RULES
--------------------------------------------------

IF query contains:
- "REFUND POLICY"
- "refund policy"
- "refund rules"


THEN:
    - MUST call tool: show_refund_policy

--------------------------------------------------

IF query contains:
- "CANCELLATION POLICY"
- "cancellation policy"
- "CANCELLATION POLICY"
- "cancellation policy"
- "cancellation rules"


THEN:
    - MUST call tool: show_cancellation_policy

--------------------------------------------------

STRICT RULES
--------------------------------------------------

- NEVER hallucinate policy information
- NEVER invent policy terms
- ONLY use tool outputs
- NEVER answer without tool execution
- NEVER generate unrelated escalation reasons
- NEVER assume refund/login/password issues
- ONLY answer using actual tool output
- ALWAYS stay grounded to customer query

--------------------------------------------------
CUSTOMER QUERY
--------------------------------------------------

Query:
{query}

--------------------------------------------------
OUTPUT FORMAT
--------------------------------------------------

Return STRICT JSON only.

{
  "query_type": "",
  "tool_called": "",
  "policy_information_provided": true,
  "response": "",
  "support_contact":
  {
      "email": "customer_care@support.com",
      "phone": "1800-0011-011"
  },
  "confidence": "HIGH|MEDIUM|LOW",
  "final_status": "SUCCESS|FAILED"
}

"""



###=======================================================================================================


## Define the Agents 

def build_agent(role: str, goal: str, backstory: str, llm=llm ,verbose: bool = True, tools=None) -> Agent:
    return Agent(role=role, goal=goal, backstory=backstory, llm=llm, verbose=verbose, allow_delegation=False, tools=tools if tools else [])

## Define the Tasks 
def build_task(description: str, agent: Agent, expected_output: str = "Task completed") -> Task:
    return Task(description=description, agent=agent, expected_output=expected_output)

## Define the Agents 


# ============================================================
# INTENT AGENT
# ============================================================

intent_agent = build_agent(

    role="Ecommerce Customer Support Policy AI Agent",

    goal="""

    Provide accurate Ecommerce policy information
    using ONLY approved policy tools.

    Your responsibilities:

    - Detect customer intent
    - Identify whether query is:
        - REFUND POLICY
        - CANCELLATION POLICY

    - Execute the correct tool
    - Return grounded policy information
    - Never hallucinate policy content
    - Never invent escalation reasons
    - Never answer outside tool responses

    IMPORTANT:

    Check if {query} as KEYWORDS "refund POLICY" or "cancellation POLICY"
    
    IF query asks about REFUND POLICY:
        MUST call show_refund_policy tool

    IF query asks about CANCELLATION POLICY:
        MUST call show_cancellation_policy tool

    Always provide deterministic JSON output.

    """,

    backstory="""

    You are a specialized Ecommerce Customer Support AI Agent.

    Your ONLY responsibility is to provide policy information
    for Ecommerce customers.

    You are strictly tool-grounded.

    You NEVER:
    - hallucinate policies
    - create fake rules
    - infer unrelated support issues
    - invent refund/login/password issues
    - behave like audit/compliance/security agent

    You ALWAYS:
    - execute correct policy tool
    - provide grounded responses
    - provide support contact information
    - provide concise customer guidance

    If customer needs more help:

    Please contact:
    - 24x7 Customer Support: 1800-0011-011
    - customer_care@support.com

    """,

    tools=[
        show_refund_policy_tool,
        show_cancellation_policy_tool
    ],

    llm=llm,
    verbose=True
)


# ============================================================


# INTENT TASK
# ============================================================

intent_task = build_task(

    description="""

    Determine the customer policy query type.

    --------------------------------------------------
    POLICY QUERY TYPES
    --------------------------------------------------

    1. REFUND POLICY
    2. CANCELLATION POLICY

    --------------------------------------------------
    TOOL EXECUTION REQUIREMENTS
    --------------------------------------------------

    IF customer asks about REFUND POLICY:
        - MUST execute show_refund_policy tool

    IF customer asks about CANCELLATION POLICY:
        - MUST execute show_cancellation_policy tool

    --------------------------------------------------
    VALIDATION RULES
    --------------------------------------------------

    - ONLY use tool output
    - NEVER hallucinate policies
    - NEVER invent policy details
    - NEVER answer without tool execution
    - ALWAYS remain grounded to query

    --------------------------------------------------
    CUSTOMER QUERY
    --------------------------------------------------

    Query:
    {query}

    Check if {query} as KEYWORDS "refund POLICY" or "cancellation POLICY"
    --------------------------------------------------
    OUTPUT REQUIREMENTS
    --------------------------------------------------

    Return STRICT JSON only.

    """,

    agent=intent_agent,

    expected_output="""
    {
      "customer_query_type": "CANCELLATION POLICY |REFUND POLICY|CANCELLATION RULES |REFUND RULES",
      "tool_called": "",
      "policy_information_provided": "TRUE/FALSE" ,
      "response": "",
      "support_contact_provided": "TRUE/FALSE" ,

      "support_contact": {
          "email": "customer_care@support.com",
          "phone": "1800-0011-011"
      },

      "accuracy": {
          "score": 5,
          "reason": ""
      },

      "completeness": {
          "score": 5,
          "reason": ""
      },

      "clarity": {
          "score": 5,
          "reason": ""
      },

      "hallucination_check": {
          "detected": false,
          "reason": ""
      },

      "overall_score": [1-5] ,
      "confidence": "HIGH|MEDIUM|LOW",
      "final_verdict": "PASS/FAIL",
      "final_status": "SUCCESS"
    }
    """
)




##=======================================================================================
### Run the Agents 

def run_tools_agent(query: str):
    crew_call_tools = Crew(
        agents=[intent_agent],
        tasks=[intent_task],
        verbose=True,
    )
    
    
    with get_openai_callback() as cb:

            result = crew_call_tools.kickoff(
                inputs={
                    "query": query                  
                }
            )

            print("\n===================================")
            print("CrewAI Token Usage")
            print("===================================")
            print(f"Total Tokens      : {cb.total_tokens}")
            print(f"Prompt Tokens     : {cb.prompt_tokens}")
            print(f"Completion Tokens : {cb.completion_tokens}")   
            
            ## Record the Token Usage into the LOG   
            logging.info("Tools Agent : Total Tokens Used = " + str(cb.total_tokens))
            logging.info("Tools Agent  : Prompt Tokens = " + str(cb.prompt_tokens))
            logging.info("Tools Agent  : Completion Tokens = " + str(cb.completion_tokens))   
            
            token_usage = {
                "prompt_tokens": cb.prompt_tokens,
                "completion_tokens": cb.completion_tokens,
                "total_tokens": cb.total_tokens
            }

            logging.info("Tools Agent  Token Usage : " + str(token_usage))          
            
    return result 

