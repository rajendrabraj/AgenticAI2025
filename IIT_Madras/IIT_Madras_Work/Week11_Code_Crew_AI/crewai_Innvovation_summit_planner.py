## Python Code 
## Name : Rajendra Bichu. 
## Version 1.0. Date : 15th Jan 2026
### CrewAI for creating a Innovation summit planner based on User Inputs


from crewai import Crew, Agent, Task

# Warning control
import warnings
warnings.filterwarnings('ignore')
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import warnings
warnings.filterwarnings('ignore')
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

planner = Agent(
    role="Event Planner Agent (Hierarchical Planner)",
    goal="Breaks the big goal into pillars: venue, logistics, speakers, vendors, schedule, budget.",
    backstory="Generates sub-tasks and success metrics for each pillar",
    llm=llm,  # FIXED: was ll=llm
    verbose=True
)

researcher = Agent(
    role="Vendor Research Agent",
    goal="Catering vendors (2–3 options) with Audio/visual vendors with provide and Seating & event décor providers. Optional: Stage setup companies.",
    backstory="You are skilled at quickly comparing the options and returning concise recommendations.",
    llm=llm,
    verbose=True
)

budgeter = Agent(
    role="Builds detailed cost estimates.",
    goal="Breaks down by category (venue, F&B, décor, A/V, labour, marketing). Outputs total budget estimate & “must-book-first” items.",
    backstory="Suggests cost-saving strategies. You create realistic cost estimates and show price in INR.",
    llm=llm,
    verbose=True
)

itinerary_maker = Agent(
    role="Schedule Designer Agent",
    goal="Creates a full-day event schedule. Includes keynote sessions, buffer times, breaks, workshops, and networking blocks.",
    backstory="Includes speaker preparation windows.Should be realistic and time-bound..",
    llm=llm,
    verbose=True
)

coordinator = Agent(
    role="Final Event Coordinator Agent",
    goal="Consolidates all outputs into one structured event plan. Includes booking checklist, timeline, risks, and contingencies.",
    backstory="Produces a final formatted deliverable. Required Dynamic Inputs and concise recommendation.",
    llm=llm,
    verbose=True
)
# Tasks

decompose_task = Task(
    description=(
        "Breaks down the high-level event goal into a structured multi-level plan.:\n"
        "Goal: {event_goal}\n"
        "Dates: {dates}\n"
        "Number of attendees : {attendees_count}\n"
        "Preferences: {preferences}\n\n"
        "Produce a hierarchical plan with levels:\n"
        "Level 1:  Researches vendors, venues, and scheduling options. \n"
        "Level 2:Researches vendors, venues, and scheduling options. \n"
        "Level 3: Builds a complete event budget. Creates a full event-day schedule.\n\n"
        "Produces a final consolidated event plan. Return as a structured list or JSON-like text."
    ),
    expected_output="Heirarchical plan",
    agent=planner
)

research_task = Task(
    description=(
        "Research for the list options given:\n"
        "Goal: {event_goal}\n"
        "Dates: {dates}\n"
        "Number of attendees : {attendees_count}\n"
        "Preferences: {preferences}\n\n"
        "Return concise recommendations for:\n"
        "- 5- Catering vendors (2–3 options). Audio/visual vendors. \n"      
        "- 5- Seating & event décor providers. Optional: Stage setup companies. \n"
        "If Vendor has discount pricing show with a Checked Box 'DISCOUNT PRICING(YES)'."
    ),
    expected_output="Research summary with 2-3 recommended options per category",
    agent=researcher
)

budget_task = Task(
    description=(
        "Create a budget estimate for the options described:\n"
        "Goal: {event_goal}\n"
        "Dates: {dates}\n"
        "Number of attendees : {attendees_count}\n"
        "Preferences: {preferences}\n\n"
        "Builds detailed cost estimates. Breaks down by category (venue, F and B, décor, A/V, labour, marketing).\n"
        "Suggests cost-saving strategies. Outputs total budget estimate & “must-book-first” items."
    ),
    expected_output="Budget table and cost-saving recommendations",
    agent=budgeter
)

itinerary_task = Task(
    description=(
        "Create a full-day event schedule:\n"
        "Goal: {event_goal}\n"
        "Dates: {dates}\n"
        "Number of attendees : {attendees_count}\n"
        "Preferences: {preferences}\n\n"
        "Creates a full-day event schedule. Includes keynote sessions, buffer times, breaks, workshops, and networking blocks.\n"
        "Includes speaker preparation windows. Should be realistic and time-bound."
    ),
    expected_output="Full-day event schedule with timings",
    agent=itinerary_maker
)

coordinate_task = Task(
    description=(
        "Assemble Researches vendors, venues, and scheduling options using previous outputs.\n"
        "Inputs: hierarchical plan, research summary, budget estimate, itinerary.\n\n"
        "Produce a final deliverable containing:\n"
        "- Executive summary (1-2 paragraphs)\n"
        "- Consolidates all outputs into one structured event plan. Includes booking checklist, timeline, risks, and contingencies. \n"
        "- Produces a final formatted deliverable. Required Dynamic Inputs and concise recommendation. \n"
        "- Final total estimated cost in INR per each course\n\n"
        "Format clearly for sharing with higher management ."
        "Stop execution when you have created final Vendor list."
    ),
    expected_output="Produces a final formatted deliverable. Required Dynamic Inputs and concise recommendation all details and the system should stop.",
    agent=coordinator
)

innvoation_manager = Crew(
    agents=[planner, researcher, budgeter, itinerary_maker, coordinator],  # ADDED: itinerary_maker
    tasks=[decompose_task, research_task, budget_task, itinerary_task, coordinate_task],  # ADDED: itinerary_task
    llm=llm,
    verbose=True,
    max_iterations=1
)

# FIXED: Removed trailing commas that created tuples
event_goal = "Organize a 1 day corporate innovation summit focusing on AI and automation"
dates = "2025-01-15 to 2025-01-31"
attendees_count = "100 attendees"
preferences = "Premium decor, vegetarian vegan meal options, mid-range budget, interactive sessions."



inputs={"event_goal":event_goal,
        "dates": dates,
        "attendees_count": attendees_count,
        "preferences":preferences
       }

print("=== Innovation Summit Planner ===")
print("-" * 90)
## Kick of the Crew with Inputs 
result = innvoation_manager.kickoff(inputs)
print("-" * 90)
print("=== Innovation Summit Planner ===")


