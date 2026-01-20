## Python Code 
## Name : Rajendra Bichu. 
## Version 1.0. Date : 15th Jan 2026
### CrewAI for creating a Education planner and course recommendation based on User Inputs


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
    role="Education Planner",
    goal="Decompose the education into heirarchical sub-goals and tasks",
    backstory="You break down the learning plan  into clear and order subtasks",
    ll=llm,
    verbose=True
        
)

researcher = Agent(
    role="Education Researcher",
    goal="Find practical all the list of top 10 best courses available for a given topic given constraints.",
    backstory="You are skilled at quickly comparing the options and returning concise recommendations.",
    llm=llm,
    verbose=True
)

budgeter = Agent(
    role="career budget Analyst",
    goal="Estimate costs across various courses and recommend a budget.",
    backstory="You create realistic cost estimates and show price in INR.",
    llm=llm,
    verbose=True
)

itinerary_maker = Agent(
    role="Courses Content Creator",
    goal="Produce a detailed course list along with timelines.",
    backstory="You craft balanced course plan based on experiences.",
    llm=llm,
    verbose=True
)

coordinator = Agent(
    role="Career Coordinator",
    goal="Assemble outputs from other agents into a single cohesive plan and checklist.",
    backstory="You synthesize plans into an actionable final deliverable and list next steps for booking.",
    llm=llm,
    verbose=True
)
# Tasks

decompose_task = Task(
    description=(
        "Decompose the high-level goal:\n"
        "Goal: {education_goal}\n"
        "Dates: {dates}\n"
        "Number of Students: {student_size}\n"
        "Preferences: {preferences}\n\n"
        "Produce a hierarchical plan with levels:\n"
        "Level 1: Major pillars (education pathway, modules, activities, budget)\n"
        "Level 2: For each pillar, list 3-5 concrete sub-tasks\n"
        "Level 3: For the top-priority subtasks, suggest success criteria and timelines.\n\n"
        "Return as a structured list or JSON-like text."
    ),
    expected_output="Heirarchical plan",
    agent=planner
)

research_task = Task(
    description=(
        "Research course list options given:\n"
        "Goal: {education_goal}\n"
        "Dates: {dates}\n"
        "Number of Students: {student_size}\n"
        "Preferences: {preferences}\n\n"
        "Return concise recommendations for:\n"
        "- 5 courses rationale and long with price \n"      
        "- 5 courses from top Indian and foreign universities \n"
        "If course has discount options show with a Checked Box 'DISCOUNT OFFERED'."
    ),
    expected_output="Research summary with 2-3 recommended options per category",
    agent=researcher
)

budget_task = Task(
    description=(
        "Create a budget estimate for the trip described:\n"
        "Goal: {education_goal}\n"
        "Dates: {dates}\n"
        "Number of Students: {student_size}\n"
        "Preferences: {preferences}\n\n"
        "Include estimated costs , discount offeres, payment options and budget friendly options.\n"
        "Give a 'Total estimated budget' and two cost-optimization suggestions."
    ),
    expected_output="Budget table and cost-saving recommendations",
    agent=budgeter
)



coordinate_task = Task(
    description=(
        "Assemble final education pathway plan using previous outputs.\n"
        "Inputs: hierarchical plan, research summary, budget estimate, itinerary.\n\n"
        "Produce a final deliverable containing:\n"
        "- Executive summary (1-2 paragraphs)\n"
        "- List of offline and online courses , universitiy name \n"
        "- Course Duration for each of the courses \n"
        "- Risk notes and contingencies\n"
        "- Final total estimated cost in INR per each course\n\n"
        "Format clearly for sharing with students."
        "Stop execution when you have created final course list."
    ),
    expected_output="Final courses list with all details and the system should stop.",
    agent=coordinator
)

planner = Agent(
    role="High Level list of courses",
    goal="Decompose the goal into courses list, objectives, takeaways, Modules",
    backstory="You break down education pathway plans into clear and order subtasks",
    llm=llm,
    verbose=True
        
)

edu_advisor = Crew(
    agents=[planner, researcher, budgeter, coordinator],
    tasks=[decompose_task, research_task, budget_task,  coordinate_task],
    llm=llm,
    verbose=True,
    max_iterations=1
)


education_goal = "Objective is to learn Agentic AI concepts as per Industry based requirements." 
dates = "2025-01-01 to 2025-12-31"
student_size = "2 students"
preferences = "Moderate budget, Topic contents and course contents , show best rated courses based on univesities, prefer online courses with certification"



inputs={"education_goal":education_goal,
        "dates": dates,
        "student_size": student_size,
        "preferences":preferences
       }

## Kick of the Crew with Inputs 
result = edu_advisor.kickoff(inputs)

