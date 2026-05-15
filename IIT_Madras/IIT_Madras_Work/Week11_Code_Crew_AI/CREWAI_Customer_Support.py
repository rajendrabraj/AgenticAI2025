##Python Code
## Customer support teams often receive diverse queries—from login issues and billing errors to technical problems. Manually analyzing each message, searching a knowledge base, generating a helpful response, and deciding whether to escalate takes time and is inconsistent across agents.

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



issue_classifier = Agent(
    role="Issue Identification Specialist",
    goal="Correctly interpret and classify customer issues.",
    backstory="You are trained in identifying user intent and support category.",
    llm = llm,
    verbose=True
)

knowledge_agent = Agent(
    role="Knowledge Base Specialist",
    goal="Search the internal documentation to find matching solutions.",
    backstory="You are a search system that returns the best match from the support knowledge base.",
    llm=llm,
    verbose=True
)

solution_agent = Agent(
    role="Solution Generator",
    goal="Craft a final, user-friendly response using available info.",
    backstory="You write empathetic support replies with clarity and helpful tone.",
    llm=llm,
    verbose=True
)

escalation_agent = Agent(
    role="Escalation Coordinator",
    goal="Determine whether escalation to a human agent is required.",
    backstory="You evaluate uncertainty, urgency, or missing details to decide escalation.",
    llm=llm,
    verbose=True
)


# ---------------- Tasks ----------------
identify_issue = Task(
    description="""Analyze the customer message: "{customer_query}".
Identify:
- Issue type (billing, technical, login, refund, general inquiry)
- Sentiment (angry, neutral, confused, urgent)
- Priority level (low, normal, high)
Output as JSON with keys: type, urgency, sentiment, summary.""",
    agent=issue_classifier,
    expected_output="A JSON object describing classified issue details."
)

fetch_knowledge = Task(
    description="""Based on the classification above and the message "{customer_query}",
search the knowledge base and retrieve the closest matching solution.
If no solution exists, respond with: 'NO MATCH FOUND'.""",
    agent=knowledge_agent,
    expected_output="Best possible KB solution or 'NO MATCH FOUND'."
)

generate_solution_response = Task(
    description="""Using the classification and retrieved KB content for: "{customer_query}",
create a friendly step-by-step customer support response that:
- Uses plain language
- Offers clear next steps
- Includes apology if needed""",
    agent=solution_agent,
    expected_output="A polished support response formatted for users."
)

apply_escalation_logic = Task(
    description="""Evaluate whether the AI response is sufficient.
Consider:
- Confidence level
- Urgency from issue classification
- Whether solution was 'NO MATCH FOUND'

Output either:
- `resolved` if handled successfully
- `requires_escalation` with explanation and escalation notes""",
    agent=escalation_agent,
    expected_output="Resolution status + justification."
)


# ---------------- Crew Setup ----------------
cs_crew = Crew(
    agents=[issue_classifier, knowledge_agent, solution_agent, escalation_agent],
    tasks=[identify_issue, fetch_knowledge, generate_solution_response, apply_escalation_logic],
    verbose=True
)


# ---------------- Run ----------------
# customer_query = input("\nEnter customer message: ")
customer_query= """I’m unable to log into my account even though I’m sure the password is correct. Can someone help?"""

result = cs_crew.kickoff(inputs={"customer_query": customer_query})
print("-" * 90)
print("\n--- FINAL SYSTEM RESPONSE ---\n")
print(result)
print("-" * 90)