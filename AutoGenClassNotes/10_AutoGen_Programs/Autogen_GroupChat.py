# ##  July 2025 
# SelectorGroupChat implements a team where participants take turns broadcasting 
# messages to all other members.
# A generative model (e.g., an LLM) selects the next speaker based on the shared context,
#  enabling dynamic, context-aware collaboration.

# ##
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination

from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Model client
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

## Define the planning agent

planning_agent = AssistantAgent(
    name="PlanningAgent",
    description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
    model_client=model_client,
    system_message="""
    You are a planning agent.
    Your job is to break down complex tasks into smaller, manageable subtasks.
    Your team members are:
        WebSearchAgent: Searches for information
        DataAnalystAgent: Performs calculations

    You only plan and delegate tasks - you do not execute them yourself.

    When assigning tasks, use this format:
    1. <agent> : <task>

    After all tasks are complete, summarize the findings and end with "TERMINATE".
    """,
)

from dotenv import load_dotenv

from langchain_community.utilities import GoogleSerperAPIWrapper
from autogen_ext.tools.http import HttpTool

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
#exchange_api_key = os.getenv("EXCHANGE_RATE_API")
SERPER_API_KEY  = os.getenv("SERPER_API_KEY")

#os.environ['SERPER_API_KEY']='bead05022450578faa7498f4c90d85e534c372e0'

## Search Tool Wrapper using Google Serper API and execute a Web query

search_tool_wrapper = GoogleSerperAPIWrapper(type='search')

def search_web(query:str) ->str:
    """Search the web for the given query and return the results."""
    print("INSIDE SEARCH_WEB\n")
    try:
        results = search_tool_wrapper.run(query)
        return results
    except Exception as e:
        print(f"Error occurred while searching the web: {e}")
        return "No results found."
    

## Simulate a Web Search 
def search_web_tool(query:str)-> str:
    # Simulate a web search
    print("INSIDE SEARCH_WEB_TOOL\n")
    if "2006-2007" in query:
        return """Here are the total points scored by Miami Heat players in the 2006-2007 season:
        Udonis Haslem: 844 points
        Dwayne Wade: 1397 points
        James Posey: 550 points
        ...
        """
    elif "2007-2008" in query:
        return "The number of total rebounds for Dwayne Wade in the Miami Heat season 2007-2008 is 214."
    elif "2008-2009" in query:
        return "The number of total rebounds for Dwayne Wade in the Miami Heat season 2008-2009 is 398."
    return "No data found."

model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)


## Web Search Agent 

web_search_agent = AssistantAgent(
    name = 'WebSearchAgent',
    description= 'An agent for searching the web for information.',
    model_client=model_client,
    tools = [search_web_tool],
    reflect_on_tool_use=False,
    system_message='''
        You are a web search agent.
        Your only tool is search_web - use it to find the information you need.

        You make only one search call at a time.
        
        Once you have the results, you never do calculations or data analysis on them.
    ''',
)

def percentage_change_tool(start:float, end:float) -> float:
    # Calculate percentage change
    print("% INSIDE Change Tool\n")
    if start == 0:
        return 0
    return ((end - start) / start) * 100

## Data Analyst Agent


data_analyst_agent = AssistantAgent(
    name = 'DataAnalystAgent',
    description= 'An agent for performing calculations and data analysis.',
    model_client=model_client,
    tools= [percentage_change_tool],
    system_message='''
        You are a data analyst agent.
        Given the tasks you have been assigned, you should analyze the data and provide results using the tools provided (percentage_change_tool).

        If you have not seen the data, ask for it.

    ''',
)

## Termination Conditions

from autogen_agentchat.conditions import TextMentionTermination,MaxMessageTermination
text_mention_termination = TextMentionTermination('TERMINATE')
max_message_termination = MaxMessageTermination(max_messages=20)
combined_termination = text_mention_termination | max_message_termination

## Prompt Selector 

selector_prompt = '''
Select an agent to perform the task.

{roles}

current conversation history :
{history}

Read the above conversation, then select an agent from {participants} to perform the next task.
Make sure that the planning agent has assigned task before other agents start working.
Only select one agent.
'''

print("============\n")
print(planning_agent.description)
print("============\n")

print("============\n")

#define the team with multiple agents


selector_team = SelectorGroupChat(
    participants=[planning_agent, web_search_agent, data_analyst_agent],
    model_client=model_client,
    termination_condition=combined_termination,
    selector_prompt=selector_prompt,
    allow_repeated_speaker=True)

#define the task

task = "Who was the Miami Heat player with the highest point in the 2006-2007 season, and what was the percentage change in his total rebounds between the 2007-2008 and 2008-2009 seasons?"




from autogen_agentchat.ui import Console
async def team_run_operation():
    print("RUNNING TEAM RUN FIRST OPERATIONS\n")
    await Console(selector_team.run_stream(task=task))   
    state = await selector_team.save_state()

from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage
from typing import Sequence

def my_selector_fun(messages: Sequence[BaseAgentEvent | BaseChatMessage]):
    if messages[-1].source == web_search_agent.name:
        return data_analyst_agent.name
    return None

selector_team2 = SelectorGroupChat(
    participants=[planning_agent, web_search_agent, data_analyst_agent],
    model_client=model_client,
    termination_condition=combined_termination,
    selector_prompt=selector_prompt,
    allow_repeated_speaker=True,
    selector_func=my_selector_fun)


async def team_2_ops():
    task = "Who was the Miami Heat player with the highest point in the 2007-2008 season, and what was the percentage change in his total rebounds between the 2007-2008 and 2008-2009 seasons?"
    from autogen_agentchat.ui import Console
    print("RUNNING TEAM RUN SECOND OPERATIONS\n")
    await Console(selector_team2.run_stream(task=task))  



from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage
from typing import Sequence

def my_selector_fun2(messages: Sequence[BaseAgentEvent | BaseChatMessage]):
    print("RUNNING my_selector_fun2: \n")
    if messages[-1].source != web_search_agent.name:
        return data_analyst_agent.name
    return None


selector_team3 = SelectorGroupChat(
    participants=[planning_agent, web_search_agent, data_analyst_agent],
    model_client=model_client,
    termination_condition=combined_termination,
    selector_prompt=selector_prompt,
    allow_repeated_speaker=False,
    selector_func=my_selector_fun2)


async def team_3_ops():
    from autogen_agentchat.ui import Console
    # If Data analyst agent is not selected after web search agent
    task = "Who was the Miami Heat player with the highest point in the 2006-2007 season, and what was the percentage change in his total rebounds between the 2007-2008 and 2008-2009 seasons?"
    await selector_team.reset()     
    from autogen_agentchat.ui import Console
    print("RUNNING TEAM RUN THIRD OPERATIONS\n")
    await Console(selector_team3.run_stream(task=task))  

from typing import List, Sequence
    
def candidate_func(messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> List[str]:
    # keep planning_agent first one to plan out the tasks
    if messages[-1].source == "user":
        return [planning_agent.name]

    # if previous agent is planning_agent and if it explicitely asks for web_search_agent
    # or data_analyst_agent or both (in-case of re-planning or re-assignment of tasks)
    # then return those specific agents
    last_message = messages[-1]
    if last_message.source == planning_agent.name:
        participants = []
        if web_search_agent.name in last_message.to_text():
            participants.append(web_search_agent.name)
        if data_analyst_agent.name in last_message.to_text():
            participants.append(data_analyst_agent.name)
        if participants:
            return participants  # SelectorGroupChat will select from the remaining two agents.

    # we can assume that the task is finished once the web_search_agent
    # and data_analyst_agent have took their turns, thus we send
    # in planning_agent to terminate the chat
    previous_set_of_agents = set(message.source for message in messages)
    if web_search_agent.name in previous_set_of_agents and data_analyst_agent.name in previous_set_of_agents:
        return [planning_agent.name]

    # if no-conditions are met then return all the agents
    return [planning_agent.name, web_search_agent.name, data_analyst_agent.name]



from autogen_agentchat.agents import UserProxyAgent

user_proxy_agent = UserProxyAgent("UserProxyAgent", description="A proxy for the user to approve or disapprove tasks.")
text_mention_termination = TextMentionTermination("TERMINATE")
max_messages_termination = MaxMessageTermination(max_messages=10)
termination = text_mention_termination | max_messages_termination

def selector_func_with_user_proxy(messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> str | None:
    if messages[-1].source != planning_agent.name and messages[-1].source != user_proxy_agent.name:
        # Planning agent should be the first to engage when given a new task, or check progress.
        return planning_agent.name
    

    if messages[-1].source == planning_agent.name:
        if messages[-2].source == user_proxy_agent.name and "APPROVE" in messages[-1].content.upper():  # type: ignore
            # User has approved the plan, proceed to the next agent.
            return None
        # Use the user proxy agent to get the user's approval to proceed.
        return user_proxy_agent.name
    

    if messages[-1].source == user_proxy_agent.name:
        # If the user does not approve, return to the planning agent.
        if "APPROVE" not in messages[-1].content.upper():  # type: ignore
            return planning_agent.name
        

    return None

# Reset the previous agents and run the chat again with the user proxy agent and selector function.
# await sele.reset()

async def team_ops_with_proxy():
    team = SelectorGroupChat(
        [planning_agent, web_search_agent, data_analyst_agent, user_proxy_agent],
        model_client=model_client,
        termination_condition=termination,
        selector_prompt=selector_prompt,
        selector_func=selector_func_with_user_proxy,
        allow_repeated_speaker=True,
    )
    print("RUNNING TEAM#4 OPERATIONS\n")
    await Console(team.run_stream(task=task))


##Call from the Main Function.
async def main():
    print("RUNNING OPERATIONS FROM MAIN\n")
    await team_run_operation()
    await team_2_ops()
    await team_3_ops()
    await team_ops_with_proxy()
    print("COMPLETED OPERATIONS FROM MAIN\n")

#Execute the request using the model
asyncio.run(main())
