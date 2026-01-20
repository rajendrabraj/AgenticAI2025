##Health Care Crew AI Implemenation...

# Warning control
import warnings

from sympy import true
warnings.filterwarnings('ignore')
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import warnings
warnings.filterwarnings('ignore')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

from crewai import Agent, Task, Crew

# ---------------- AGENTS ----------------

triage_agent = Agent(
    role="Triage Specialist",
    goal="Classify patient urgency based on symptoms and reported condition.",
    backstory="You are trained in medical emergency response and follow triage protocols like ESI and CTAS.",
    llm=llm,
    verbose=True
)

planning_agent = Agent(
    role="Care Planning Strategist",
    goal="Generate a structured plan for treatment priorities.",
    backstory="You create evidence-based plans and ensure medical decisions follow best practice frameworks.",
    llm=llm,
    verbose=True
)

decision_agent = Agent(
    role="Hybrid Decision Intelligence Unit",
    goal="Select between reactive emergency response or deliberate planned care.",
    backstory="When a case is critical, you respond rapidly. For stable cases, you perform deeper reasoning.",
    llm=llm,
    verbose=True
)

monitoring_agent = Agent(
    role="Patient Monitoring and Escalation Agent",
    goal="Continuously evaluate patient vitals and symptoms to adjust urgency dynamically.",
    backstory="You track patient condition in real-time and trigger escalation if health indicators deteriorate.",
    llm=llm,
    verbose=True
)



# ---------------- TASKS and DEFINE the Tasks ----------------



triage_task = Task(
    description=(
        "You will evaluate the provided patient details.\n"
        "Patient Symptoms:\n\n"
        "{patient_details}\n\n"
        "Steps:\n"
        "1. Identify key symptoms.\n"
        "2. Classify severity (Mild / Moderate / Severe / Emergency).\n"
        "3. Recommend next steps along with list of top 5 medicines.\n\n"
        "Return the result in a clear structured response."
    ),
    expected_output="A structured medical triage report including severity and guidance.",
    agent=triage_agent
)

care_plan_task = Task(
    description="""Using the triage results and patient details "{patient_details}",
generate a treatment prioritization plan with 3–5 actionable steps and recommend the medicines for the symptoms .
Ensure actions align with evidence-based emergency response standards.""",
    agent=planning_agent,
    expected_output="A structured care plan."
)

decision_task = Task(
    description="""Using the triage results and care plan for "{patient_details}":
Decide the treatment mode:
- 'Reactive Emergency Response' for high or critical cases
- 'Deliberative Planned Care' for stable cases

Provide justification in 2–3 sentences.""",
    agent=decision_agent,
    expected_output="Decision + reasoning."
)

monitoring_task = Task(
    description="""Simulate ongoing condition monitoring for "{patient_details}".
If signs of deterioration appear (e.g., 'breathing difficulty', 'loss of consciousness', 'chest pain worsening'):
Return: "ESCALATE IMMEDIATELY".

Otherwise return: "Patient stable. Continue existing care plan." """,
    agent=monitoring_agent,
    expected_output="Monitoring result and escalation status."
)

# ---------------- CREW PIPELINE ----------------

triage_pipeline = Crew(
    agents=[triage_agent, planning_agent, decision_agent, monitoring_agent],
    tasks=[triage_task, care_plan_task, decision_task, monitoring_task],
    verbose= True
)

# ---------------- EXECUTE THE CREW WITH CUSTOMER QUERY ----------------

# patient_details = """Patient has mild fever, sore throat, and fatigue for two days. No trouble breathing, no chest pain."""

# result = triage_pipeline.kickoff(inputs={"patient_details": patient_details})
# print("-" * 90)
# print("\n--- FINAL OUTPUT ---\n")
# print(result)
# print("-" * 90)


patient_details = """Patient chest pain."""

result = triage_pipeline.kickoff(inputs={"patient_details": patient_details})
print("-" * 90)
print("\n--- FINAL OUTPUT ---\n")
print(result)
print("-" * 90)
