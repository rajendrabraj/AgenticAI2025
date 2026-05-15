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
    role="High Level Trip Planner",
    goal="Decompose the vacation into heirarchical sub-goals and tasks",
    backstory="You break down travel plans into clear and order subtasks",
    ll=llm,
    verbose=True
        
)

researcher = Agent(
    role="Travel Researcher",
    goal="Find practical options for flights, accommodations, and local transport given constraints.",
    backstory="You are skilled at quickly comparing travel options and returning concise recommendations.",
    llm=llm,
    verbose=True
)

budgeter = Agent(
    role="Travel Budget Analyst",
    goal="Estimate costs across flights, hotels, transport, food, and activities and recommend a budget.",
    backstory="You create realistic cost estimates and suggest cost-saving tradeoffs for families.",
    llm=llm,
    verbose=True
)

itinerary_maker = Agent(
    role="Itinerary Creator",
    goal="Produce a detailed day-by-day itinerary aligned with family preferences, pace, and child-friendly options.",
    backstory="You craft balanced itineraries with travel time, rest, and high-impact experiences.",
    llm=llm,
    verbose=True
)

coordinator = Agent(
    role="Trip Coordinator",
    goal="Assemble outputs from other agents into a single cohesive travel plan and checklist.",
    backstory="You synthesize plans into an actionable final deliverable and list next steps for booking.",
    llm=llm,
    verbose=True
)
# Tasks

decompose_task = Task(
    description=(
        "Decompose the high-level goal:\n"
        "Goal: {vacation_goal}\n"
        "Dates: {dates}\n"
        "Family size: {family_size}\n"
        "Preferences: {preferences}\n\n"
        "Produce a hierarchical plan with levels:\n"
        "Level 1: Major pillars (travel, lodging, transport, activities, budget)\n"
        "Level 2: For each pillar, list 3-5 concrete sub-tasks\n"
        "Level 3: For the top-priority subtasks, suggest success criteria and timelines.\n\n"
        "Return as a structured list or JSON-like text."
    ),
    expected_output="Heirarchical plan",
    agent=planner
)

research_task = Task(
    description=(
        "Research travel options given:\n"
        "Goal: {vacation_goal}\n"
        "Dates: {dates}\n"
        "Family size: {family_size}\n"
        "Preferences: {preferences}\n\n"
        "Return concise recommendations for:\n"
        "- 2 flight options (price tier and rationale)\n"
        "- 2 accommodation types (hotel vs apartment) and one sample neighborhood each\n"
        "- Local transport options (rail passes, car rental notes)\n\n"
        "If any option requires online bookings or external checks, flag it with 'ACTION REQUIRED'."
    ),
    expected_output="Research summary with 2-3 recommended options per category",
    agent=researcher
)

budget_task = Task(
    description=(
        "Create a budget estimate for the trip described:\n"
        "Goal: {vacation_goal}\n"
        "Dates: {dates}\n"
        "Family size: {family_size}\n"
        "Preferences: {preferences}\n\n"
        "Include estimated costs (per category): Flights, Accommodation (per night), Local transport, Food (per day), Activities, Contingency.\n"
        "Give a 'Total estimated budget' and two cost-optimization suggestions."
    ),
    expected_output="Budget table and cost-saving recommendations",
    agent=budgeter
)

itinerary_task = Task(
    description=(
        "Build a 7-day sample itinerary (adjust to {dates} length if needed) for the family:\n"
        "Goal: {vacation_goal}\n"
        "Family size: {family_size}\n"
        "Preferences: {preferences}\n\n"
        "For each day list:\n"
        "- Morning / Afternoon / Evening items\n"
        "- Estimated travel time between stops\n"
        "- Child-friendly notes and booking needs\n"
        "- Time buffers for rest\n\n"
        "Return a balanced, realistic daily schedule."
    ),
    expected_output="Day-by-day itinerary with notes",
    agent=itinerary_maker
)

coordinate_task = Task(
    description=(
        "Assemble final travel plan using previous outputs.\n"
        "Inputs: hierarchical plan, research summary, budget estimate, itinerary.\n\n"
        "Produce a final deliverable containing:\n"
        "- Executive summary (1-2 paragraphs)\n"
        "- Actionable booking checklist (flights, hotels, passes, reservations)\n"
        "- Timeline for when to book each item\n"
        "- Risk notes and contingencies\n"
        "- Final total estimated cost\n\n"
        "Format clearly for sharing with family."
        "Stop execution when you have created final plan and checklist."
    ),
    expected_output="Final trip plan & checklist The system should stop.",
    agent=coordinator
)

planner = Agent(
    role="High Level Trip Planner",
    goal="Decompose the vacation into heirarchical sub-goals and tasks",
    backstory="You break down travel plans into clear and order subtasks",
    llm=llm,
    verbose=True
        
)

trip_crew = Crew(
    agents=[planner, researcher, budgeter, itinerary_maker, coordinator],
    tasks=[decompose_task, research_task, budget_task, itinerary_task, coordinate_task],
    llm=llm,
    verbose=True,
    max_iterations=1
)


vacation_goal = "Plan a 7-day family vacation to Italy focusing on Varanasi , Ayodhya" 
dates = "2025-12-11 to 2025-12-31"
family_size = "2 adults"
preferences = "Moderate budget, kid-friendly activities, avoid long overnight travel, prefer central accommodations"


inputs={"vacation_goal":vacation_goal,
        "dates": dates,
        "family_size": family_size,
        "preferences":preferences
       }


result = trip_crew.kickoff(inputs)

