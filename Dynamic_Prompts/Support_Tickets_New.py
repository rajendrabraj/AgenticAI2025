# Initialize client
import os
import json
from langchain_openai import ChatOpenAI

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, SystemMessage

from textwrap import indent
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import warnings
warnings.filterwarnings('ignore')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

######-==========




# Example input values — you can replace these dynamically
ticket_input = {
    "CUSTOMER_TIER": "Enterprise",
    "PRODUCT_AREA": "Billing",
    "SENTIMENT_SCORE": 0.25,
    "EXTRACTED_KEYWORDS": ["refund", "delay"]
}



# basic_prompt = f"Write email to {ticket_user['name']}: loan rejected due to {ticket_user['reason']}"

## Define Routing Rules in natural language for LLM to parse and apply


ROUTING_RULES = """
1️⃣ If CUSTOMER_TIER = "Enterprise" AND SENTIMENT_SCORE < 0.3:
    Priority = "URGENT"
    Route to = "Senior Support"
    SLA_TARGET = "1 hour"
    ESCALATION_CRITERIA = "If not acknowledged in 30 minutes"

2️⃣ If PRODUCT_AREA = "Billing" AND EXTRACTED_KEYWORDS contain any of ["refund", "charge", "payment"]:
    Route to = "Billing Team"
    SLA_TARGET = "4 hours"
    TEMPLATE_ID = "Billing_Issue_Response"

3️⃣ If EXTRACTED_KEYWORDS contain any of ["bug", "error", "broken"] AND CUSTOMER_TIER = "Premium":
    Priority = "HIGH"
    Route to = "Technical Team"
    SLA_TARGET = "2 hours"
    TEMPLATE_ID = "Tech_Error_Response"

4️⃣ Default rule:
    Priority = "MEDIUM"
    Route to = "General Support"
    SLA_TARGET = "6 hours"
    TEMPLATE_ID = "Generic_Response"
    
    """


# Example input values — you can replace these dynamically
ticket_input = {
    "CUSTOMER_TIER": "Enterprise",
    "PRODUCT_AREA": "Billing",
    "SENTIMENT_SCORE": 0.25,
    "EXTRACTED_KEYWORDS": ["refund", "delay"]
}

#Test Case 1 — Enterprise + Low Sentiment (Rule 1)
ticket_input = {
    "CUSTOMER_TIER": "Enterprise",
    "PRODUCT_AREA": "App",
    "SENTIMENT_SCORE": 0.20,
    "EXTRACTED_KEYWORDS": ["slow", "crash"]
}


# {ticket_input['CUSTOMER_TIER']} 

# {ticket_input['PRODUCT_AREA']} 

# {ticket_input['SENTIMENT_SCORE']} 

# {ticket_input['EXTRACTED_KEYWORDS']} 

# Inputs:
# - CUSTOMER_TIER = {{customer_tier}}
# - SENTIMENT_SCORE = {{sentiment_score}}
# - PRODUCT_AREA = {{product_area}}
# - EXTRACTED_KEYWORDS = {{extracted_keywords}}


# new_prompt = f"""
# Role:
# You are an AI-powered customer support routing engine responsible for intelligently classifying and routing customer support tickets based on predefined business rules.


# Inputs:
# - CUSTOMER_TIER = {ticket_input['CUSTOMER_TIER']} 
# - SENTIMENT_SCORE = {ticket_input['PRODUCT_AREA']} 
# - PRODUCT_AREA =  {ticket_input['SENTIMENT_SCORE']} 
# - EXTRACTED_KEYWORDS = {ticket_input['EXTRACTED_KEYWORDS']} 


# Task:
# Analyze the inputs and apply the routing rules to determine:
# - Priority
# - Assigned Team (Route to)
# - SLA Target
# - Escalation Criteria (if applicable)
# - Response Template ID (if applicable)

# Routing Rules:
# 1️⃣ If CUSTOMER_TIER == "Enterprise" AND SENTIMENT_SCORE < 0.3:
#     - Priority = "URGENT"
#     - Route to = "Senior Support"
#     - SLA_TARGET = "1 hour"
#     - ESCALATION_CRITERIA = "If not acknowledged in 30 minutes"

# 2️⃣ If PRODUCT_AREA == "Billing" AND EXTRACTED_KEYWORDS contain any of ["refund", "charge", "payment"]:
#     - Route to = "Billing Team"
#     - SLA_TARGET = "4 hours"
#     - TEMPLATE_ID = "Billing_Issue_Response"

# 3️⃣ If EXTRACTED_KEYWORDS contain any of ["bug", "error", "broken"] AND CUSTOMER_TIER == "Premium":
#     - Priority = "HIGH"
#     - Route to = "Technical Team"
#     - SLA_TARGET = "2 hours"
#     - TEMPLATE_ID = "Tech_Error_Response"

# 4️⃣ Default Rule:
#     - Priority = "MEDIUM"
#     - Route to = "General Support"
#     - SLA_TARGET = "6 hours"
#     - TEMPLATE_ID = "Generic_Response"

# Constraints:
# - Apply only one rule per ticket based on priority order.
# - Follow the rules in the exact sequence listed above.
# - If multiple rules match, apply the first matching rule.
# - If no rule matches, apply the default rule.

# Output Format:
# Return the final routing decision strictly in JSON format as:

# {{
#   "priority": "",
#   "route_to": "",
#   "sla_target": "",
#   "template_id": "",
#   "escalation_criteria": ""
# }}

# Now evaluate the inputs and generate the routing decision.
# """

# Build the dynamic prompt
new_prompt = f"""
You are an AI assistant for a Customer Support Ticket Analysis System.
Your task is to analyze the ticket details and determine routing priority,
SLA, escalation, and response template based on the rules.

[INPUTS]
Customer Tier: {ticket_input['CUSTOMER_TIER']}
Product Area: {ticket_input['PRODUCT_AREA']}
Sentiment Score: {ticket_input['SENTIMENT_SCORE']}
Extracted Keywords: {ticket_input['EXTRACTED_KEYWORDS']}

[ROUTING RULES]
{ROUTING_RULES}

[OUTPUT FORMAT]
Priority: <CALCULATED_PRIORITY>
Route to: <ASSIGNED_TEAM>
Suggested response time: <SLA_TARGET>
Initial response template: <TEMPLATE_ID based on the rule followed>
Escalation trigger: <ESCALATION_CRITERIA>

Now output only the structured result, no explanation.
"""





print("-----"*50)
response_to_new_prompt = llm.invoke(new_prompt)
print(response_to_new_prompt.content)

print("-----"*50)
