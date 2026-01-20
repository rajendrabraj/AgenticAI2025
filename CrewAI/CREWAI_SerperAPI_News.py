## Python Code 
## Name : Rajendra Bichu. 
## Version 1.0. Date : 20th Jan2025
## Crew AI and Serper API Integration to get Latest News using Google Search


import os
#os.environ["OPENAI_API_KEY"] = "Your Key"
#os.environ["SERPER_API_KEY"] = "Your Key" # serper.dev API key

from dotenv import load_dotenv

load_dotenv()

## Call Serper_API_Search using Google Search

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

#exchange_api_key = os.getenv("EXCHANGE_RATE_API")
serper_api_key = os.getenv("SERPER_API_KEY")



from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

research_agent = Agent(
  role='Researcher',
  # goal='Find and summarize the latest AI news',
  goal= 'Find and summarize the output based no the query : {customer_query}',
  backstory="""You're a researcher at a large company.
  You're responsible for analyzing data and providing insights
  to the business.""",
  verbose=True
)

# to perform a semantic search for a specified query from a text's content across the internet
search_tool = SerperDevTool()

task = Task(
  # description='Find and summarize the latest AI news',
  description= 'Analyze the customer message: {customer_query}',
  expected_output='A bullet list summary of the top 10 as ouput',
  agent=research_agent,
  tools=[search_tool]
)

crew = Crew(
    agents=[research_agent],
    tasks=[task],
    verbose=True
)


customer_query= """TOP 10 Agentic AI news of 2026?"""
print("-" * 90)
print("\n--- FINAL CREW AI SYSTEM RESPONSE ---\n")
result = crew.kickoff(inputs={"customer_query": customer_query})
print("-" * 90)
print(result)
print("-" * 90)