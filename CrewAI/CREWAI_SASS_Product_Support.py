## Python Code 
## Name : Rajendra Bichu. 
## Version 1.0. Date : 20th Jan2025
### Use Case 4: SaaS Product Support – Technical Issue Diagnosis. Problem Statement: SaaS companies receive technical queries related to login failures, feature usage, API errors, and integration issues.

## of Agents planned
## Technical Issue Diagnosis Agent
## Product Knowledge Reasoning Agent (non-RAG)
## Troubleshooting Response Agent
## Engineering Escalation Agent
## Goal: Reduce support workload while ensuring unresolved issues reach engineering teams.



# Warning control
import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew

import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

import warnings
warnings.filterwarnings('ignore')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)



issue_diagnosis_agent = Agent(
    role="Technical Issue Diagnosis Agent",
    goal="Correctly interpret and classify customer issues.",
    backstory="You are trained in identifying user intent and support category.",
    llm = llm,
    verbose=True
)

## This agent is Non(RAG) agent 

product_knowledge_agent = Agent(
    role="Product Knowledge Reasoning Agent",
    goal="Search the internal documentation to find matching solutions.",
    backstory="You are a search system that returns the best match from the support knowledge base available for the product.",
    # llm=llm,
    verbose=True
)

troubleshooting_agent = Agent(
    role="Troubleshooting Response Agent",
    goal="Craft a final, user-friendly response using available information.",
    backstory="You write empathetic support replies with clarity and helpful tone.",
    llm=llm,
    verbose=True
)

enginnering_escalation_agent = Agent(
    role="Engineering Escalation Agent",
    goal="Determine whether escalation to a human agent is required.",
    backstory="You evaluate uncertainty, urgency, or missing details to decide escalation.",
    llm=llm,
    verbose=True
)





# ---------------- Tasks ----------------
## This is the most important critical Tasks: #login failures, feature usage, API errors, and integration issues.

identify_tech_issue = Task(
    description="""Analyze the customer message: "{customer_query}".
Identify:
- Issue type (login failures, API errors, technical, login, feature usage, general inquiry, integration issue)
- Sentiment (angry, neutral, confused, urgent)
- Priority level (low, normal, high)
Output as JSON with keys: type, urgency, sentiment, summary.""",
    agent=issue_diagnosis_agent,
    expected_output="A JSON object describing classified issue details."
)

fetch_product_knowledge = Task(
    description="""Based on the classification above and the message "{customer_query}",
search the knowledge base and retrieve the closest matching solution.
If no solution exists, respond with: 'NO MATCH FOUND'.""",
    agent=product_knowledge_agent,
    expected_output="Best possible KB solution or 'NO MATCH FOUND'."
)

generate_troubleshooting_outcome = Task(
    description="""Using the classification and retrieved KB content for: "{customer_query}",
create a friendly step-by-step customer support response that:
- Uses plain language
- Offers clear next steps
- Includes apology if needed""",
    agent=troubleshooting_agent,
    expected_output="A polished support response formatted for users."
)

apply_engineering_escalate_logic = Task(
    description="""Evaluate whether the AI response is sufficient.
Consider:
- Confidence level
- Urgency from issue classification
- Whether solution was 'NO MATCH FOUND'

Output either:
- `resolved` if handled successfully
- `requires_escalation` with explanation and escalation notes""",
    agent=enginnering_escalation_agent,
    expected_output="Resolution status + justification."
)


# ---------------- Crew Setup ----------------
cs_crew = Crew(
    agents=[issue_diagnosis_agent, product_knowledge_agent, troubleshooting_agent, enginnering_escalation_agent],
    tasks=[identify_tech_issue, fetch_product_knowledge, generate_troubleshooting_outcome, apply_engineering_escalate_logic],
    verbose=True
)


# ---------------- Run and CREW KickOFF  ----------------
# customer_query = input("\nEnter customer message: ")
customer_query= """I am unable to login to salesforce and I have login issues. Can someone help?"""

result = cs_crew.kickoff(inputs={"customer_query": customer_query})
print("-" * 90)
print("\n--- FINAL SYSTEM RESPONSE ---\n")
print(result)
print("-" * 90)