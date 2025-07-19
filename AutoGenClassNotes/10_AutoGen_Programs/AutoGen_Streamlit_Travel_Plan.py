from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
#from autogen_agentchat.teams import TaskResult
from autogen_agentchat.base import TaskResult

import os
import asyncio

import streamlit as st
import asyncio
import time
import sys
from contextlib import redirect_stdout
from io import StringIO


from dotenv import load_dotenv
load_dotenv()


## This program is not running as of now as Streamlit output is giving few errors.

model_client = OpenAIChatCompletionClient(model="gpt-4o")

planner_agent = AssistantAgent(
    "planner_agent",
    model_client=model_client,
    description="A helpful assistant that can plan trips.",
    system_message="You are a helpful assistant that can suggest a travel plan for a user based on their request.",
)

food_agent = AssistantAgent(
    "food_agent",
    model_client=model_client,
    description="A local assistant that can suggest the TOP 10 Food restaurants in the places given.",
    system_message="You are a helpful assistant that can suggest authentic TOP 10 Food restaurants for a user and can utilize any context information provided.",
)

local_agent = AssistantAgent(
    "local_agent",
    model_client=model_client,
    description="A local assistant that can suggest local activities or places to visit.",
    system_message="You are a helpful assistant that can suggest authentic and interesting local activities or places to visit for a user and can utilize any context information provided.",
)

language_agent = AssistantAgent(
    "language_agent",
    model_client=model_client,
    description="A helpful assistant that can provide language tips for a given destination.",
    system_message="You are a helpful assistant that can review travel plans, providing feedback on important/critical tips about how best to address language or communication challenges for the given destination. If the plan already includes language tips, you can mention that the plan is satisfactory, with rationale.",
)

travel_summary_agent = AssistantAgent(
    "travel_summary_agent",
    model_client=model_client,
    description="A helpful assistant that can summarize the travel plan.",
    system_message="You are a helpful assistant that can take in all of the suggestions and advice from the other agents and provide a detailed final travel plan. You must ensure that the final plan is integrated and complete. YOUR FINAL RESPONSE MUST BE THE COMPLETE PLAN. When the plan is complete and all perspectives are integrated, you can respond with TERMINATE.",
)

termination = TextMentionTermination("TERMINATE")
#Round Robin agent and calls different agents.
group_chat = RoundRobinGroupChat(
    [planner_agent, local_agent, language_agent,food_agent, travel_summary_agent], termination_condition=termination
)


async def Travel_Operation(city):
    print("============\n")
    city_variable = city
    await Console(group_chat.run_stream(task="Plan a 5 day trip to {city_variable}."))
    await model_client.close()
    #travel_plan = group_chat.run_stream(task="Plan a 5 day trip to {city_variable}.")
    
    print("============\n")
    print(travel_plan)    
    print("============\n")
    
    

##Call from the Main Function.
# async def main():
#     await Travel_Operation(city)

 

##Streamlit code


# Streamlit UI
st.title("Async Travel Planner..")


  # Input
city = st.text_input("Enter City Name", "Mumbai")
city_variable = city
# Button
if st.button("Get me City Plan"):
    #Execute the request using the model
  
    #await Console(group_chat.run_stream(task="Plan a 5 day trip to {city_variable}."))
    #await model_client.close()
    print("============\n")
    
    #st.text_area("Console Output", final_iternary, height=800)
    st.subheader("Iternary Output:")
    chat_container = st.empty() # Placeholder for streaming output

    async def run_chat_stream():
        print(city_variable)
        full_output = ""
        user_query= "Plan a 5 day trip to " + city_variable
        print(user_query)
        ## Process the output..

        await Console(group_chat.run_stream(task="Plan a 5 day trip to {city_variable}."))
        await model_client.close()


 # Run the asynchronous function
    asyncio.run(run_chat_stream())            