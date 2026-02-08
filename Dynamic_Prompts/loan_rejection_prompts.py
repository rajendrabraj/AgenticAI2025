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


# Customer case
customer = {
    "name": "Sarah Johnson",
    "reason": "credit_score is low i.e. 550", 
    "product": "Personal Loan"
}
basic_prompt = f"Write email to {customer['name']}: loan rejected due to {customer['reason']}"



response_to_basic_prompt = llm.invoke(basic_prompt)
print(response_to_basic_prompt.content)


instruction_prompt = f"""
You are a FinTech customer officer. Write professional email to {customer['name']} about {customer['product']} rejection. The reason for rejection is {customer['reason']}.

Guidelines:
- Start with appreciation
- State decision clearly but gently  
- Give general reason (no specific numbers)
- Offer next steps
- Use empathetic, compliant tone
- Professional closing
- Keep it limited to 50 words
"""

print("-----"*50)
response_to_instruction_prompt = llm.invoke(instruction_prompt)
print(response_to_instruction_prompt.content)

print("-----"*50)


## Mock Customers

mock_customers = [
    {
        "name": "Priya Shah",
        "product_type": "Credit Card",
        "rejection_reason": "high existing credit utilization",
        "email": "priya.shah@example.com",
        "customer_since": "2019",
        "tier": "Standard",
        "location": "Pune, India"
    },
    {
        "name": "Rohit Khanna",
        "product_type": "Business Loan",
        "rejection_reason": "incomplete business documentation",
        "email": "rohit.khanna@example.com",
        "customer_since": "2020",
        "tier": "Enterprise",
        "location": "Bangalore, India"
    },
    {
        "name": "Neha Iyer",
        "product_type": "Home Loan",
        "rejection_reason": "unstable recent income pattern",
        "email": "neha.iyer@example.com",
        "customer_since": "2018",
        "tier": "Premium",
        "location": "Chennai, India"
    },
    {
        "name": "Sandeep Kulkarni",
        "product_type": "Auto Loan",
        "rejection_reason": "policy criteria not met",
        "email": "sandeep.k@example.com",
        "customer_since": "2022",
        "tier": "Standard",
        "location": "Hyderabad, India"
    }
]


default_prompt = f"Write an email to {mock_customers[0]['name']} explaining their {mock_customers[0]['product_type']} was rejected due to {mock_customers[0]['rejection_reason']}."

print("-----"*50)

response_to_default_prompt = llm.invoke(default_prompt)
print(response_to_default_prompt.content)

print("-----"*50)

##New Imoproved Prompt
# improved_prompt = f"Write an email to {mock_customers[1]['name']} explaining their {mock_customers[1]['product_type']} was rejected due to {mock_customers[1]['rejection_reason']}."




improved_prompt = f"""

Write an email to {mock_customers[1]['name']}  explaining their {mock_customers[1]['product_type']} 
was rejected due to {mock_customers[1]['rejection_reason']}. 
Role : I am a customer relationship manager from the bank. 

Task:  Write a clear, polite, and professional email to {mock_customers[1]['name']} explaining that their {mock_customers[1]['product_type']} application has been rejected.


Constraints under which the loan was rejected like credit score, defaulter history.
Outcome : Help the customer how he can seek a better loan application next time.
Details : Provide brief guidance on what steps the customer can take to improve their eligibility in the future.
Constraints : - Do not disclose confidential internal scoring models.
Tone :  A very professional and polite tone. 
"""


print("-----"*50)
print("========= Improved Prompt =========")

response_to_improved_prompt = llm.invoke(improved_prompt)
print(response_to_improved_prompt.content)

print("-----"*50)

