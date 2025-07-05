## This program is to implement Multi Agents
## This is to delegate tasks to Team A , Team B and Team C while each team handles different tasks
## Team A - Provides Mobile related report
## Team B - Provides Medicine informattion and Pharma
## Team C - Provides Stocks related information

from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List
from typing import TypedDict, Sequence, Annotated
from langchain_tavily import TavilySearch

import os
import requests

from dotenv import load_dotenv


# # Optional: set your keys securely
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
# os.environ["TAVILI_API_KEY"] = "your_tavili_api_key"

load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Set your OpenAI API key
#os.environ["OPENAI_API_KEY"] = "your-api-key"

#exchange_api_key = os.getenv("EXCHANGE_RATE_API")
tavili_api_key  = os.getenv("TAVILY_API_KEY")
TAVILI_API_URL = "https://api.tavili.ai/search"

config={"configurable":{"thread_id":"1"}}


#tavili = TaviliSearch(api_key=os.getenv("TAVILI_API_KEY"))



# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0.5, model="gpt-4-turbo")


import operator


# Define input and state structure
class TaskState(TypedDict):
    task_input: str
    task_type: str
    history: List[str]


#def invoke(self, state: TaskState) -> TaskState:
#response=app2.invoke({"messages":[HumanMessage("What is the current gdp of the china?")]},config=config)

# def invoke_model(state:AgentState):
#     messages=state["messages"]
#     question=messages[-1]
#     response=llm_with_tools.invoke(question)
#     return {"messages":[response]}
    
#class TeamAAgent(Runnable):    

from langchain_core.messages import BaseMessage

def print_formatted_response(response):
    lines = response.strip().split('\n')
    for i, line in enumerate(lines, start=1):
        print("=======\n")        
        print(f"Line {i:02d}: {line.strip()}")
        print("=======\n")


def invoke_ToolA(state: TaskState) -> TaskState:
    print("\n🔎 Team A is researching via TaviliSearch...")
    print("===\n")
    query = state["task_input"]
    print("===\n")
    print(query)
    print("===\n")
    search_results = search_tavili(query)
    summary= llm.invoke(query)
    print("===\n")
    print(summary)
    print("===\n")
    #summary = llm.invoke([HumanMessage(content=f"Summarize the following research results:\n\n{search_results}")],config=config)
    state["history"].append(f"Team A (Research):\n{summary.content}")   
    formatted_output= str(summary)
    #Show output Line by Line
    #print_formatted_response(formatted_output)

    return state


def invoke_ToolB(state: TaskState) -> TaskState:
    print("\n Team B is analyzing data...")
    print("===\n")
    data_prompt = f"You are a data analyst. Analyze this request:\n\n{state['task_input']}"
    print("===\n")
    print(data_prompt)
    result = llm.invoke([HumanMessage(content=data_prompt)],config=config)
    print("===\n")
    print(result)
    print("===\n")
    print("\n Team B is analyzing Tablets Data...")
    print("===\n")
    medicine_Query = "What is the use of Arvast 5mg tablet and sideeffects,brands"
    medicine_info= get_medicine_details(medicine_Query)
    print(medicine_info)
    #Show output Line by Line
    formatted_output= str(medicine_info)
    #print_formatted_response(formatted_output)
    #Append this to Overall output
    state["history"].append(f"Team B (Analysis):\n{result.content}")
    state["history"].append(f"Team B (Analysis):\n{medicine_info}")
    return state


def invoke_ToolC(state: TaskState) -> TaskState:
    print("\n Team C is summarizing content...")
    print("===\n")
    stock_question = "Yahoo Finance stock information for ADANIPORTS.NS provide all data"
    stock_summary= get_stock_details(stock_question)
    
    summary = llm.invoke([HumanMessage(content=f"Summarize the following:\n\n{state['task_input']}")],config=config)
    state["history"].append(f"Team C (Summary):\n{summary.content}")
    state["history"].append(f"Team B (Analysis):\n{stock_summary}")
    print("===\n")
    print(summary)
      #Show output Line by Line
    formatted_output= str(stock_summary)
    #print_formatted_response(formatted_output)
    print("===\n")
    return state

##Provide Stock specific Information 

def get_stock_details(query: str) -> str:
    
    tavili = TavilySearch(api_key=tavili_api_key)

    print("=========\n")
    print(query)
    print("=========\n")
    print("Showing detailed output...\n")
    results = tavili.run(query)
    print("=========\n")
    print(results)
    print("=========\n")
    response = results
    output = "🔍 Stock Information:\n"

    print("Showing detailed output...\n")
    print(output)


    # for result1 in response["results"]:
    #     print("=========\n")
    #     print("Showing detailed output...\n")        
    #     print("=========\n")
    #     print(f"TITLE : {result1['title']} \n ")
    #     print(f"URL : {result1['url']} \n ")
    #     print(f"CONTENTS : {result1['content']} \n ")
    #     print("=========\n")


    response = results 
    


# Function to get medicine details
##Provide Stock medicine Information 

def get_medicine_details(query: str) -> str:
    tavili = TavilySearch(api_key=tavili_api_key)
    print("=========\n")
    print(query)
    print("=========\n")
    results = tavili.run(query)
    print("=========\n")
    print(results)
    print("=========\n")

    if not results:
        return "No medicine details found."

    output = "🔍 Medicine Information:\n"
    response = results
    
    print("Showing detailed output...\n")
    print(output)
    

    for result1 in response["results"]:
        print("=========\n")
        print("Showing detailed output...\n")
        print(f"URL: {result1['url']} \n ")
        print("=========\n")
    
    response = results 
    


# -------------------------------
# Tavili Search Function
# -------------------------------
def search_tavili(query: str) -> str:
    headers = {"Authorization": f"Bearer {tavili_api_key}"}
    params = {"query": query, "num_results": 3}
    try:
        response = requests.get(TAVILI_API_URL, headers=headers, params=params)
        results = response.json()
        snippets = [item.get("snippet", "") for item in results.get("results", [])]
        return "\n".join(snippets) or "No relevant TaviliSearch results found."
    except Exception as e:
        return f"Error fetching from TaviliSearch: {str(e)}"


# ---- Controller Agent ---- #
def controller(state: TaskState) -> str:
    print("Inside Controller")
    task_type = state["task_type"].lower()
    print(f"\n🧭 Controller routing task: {task_type}")
    print(task_type)

    if task_type == "research":
        print("Team A : Researrch")
        return "team_a"
    elif task_type == "analysis":
        print("Team B : analysis") 
        return "team_b"
        
    elif task_type == "summary":
        print("Team C : summary") 
        return "team_c"
    else:
        state["history"].append("Controller: Unknown task type. Ending.")
    return END


# ---- LangGraph State Graph Setup ---- #
graph_builder = StateGraph(TaskState)

# Add team nodes
graph_builder.add_node("team_a", invoke_ToolA)
graph_builder.add_node("team_b", invoke_ToolB)
graph_builder.add_node("team_c", invoke_ToolC)


# Add controller logic
graph_builder.add_conditional_edges("controller", controller)

# Add controller node and connect flow
graph_builder.add_node("controller", lambda x: x)
graph_builder.set_entry_point("controller")

# Define transitions from teams back to controller or end
graph_builder.add_edge("team_a", END)
graph_builder.add_edge("team_b", END)
graph_builder.add_edge("team_c", END)

# Finalize the graph
graph = graph_builder.compile()

from IPython.display import Image, display
display(Image(graph.get_graph().draw_mermaid_png()))
config={"configurable":{"thread_id":"1"}}


# -------------------------------
# Example Execution
# -------------------------------

# -------------------------------
# Sample Tasks
# -------------------------------
if __name__ == "__main__":
    tasks = [
    {"task_input": "Summarize the Apple List of latest mobiles in 2 pages as report", "task_type": "research"},
    {"task_input": "Provide detailed information about Medicine progress in Cholestrol management as One Page Report", "task_type": "analysis"},
    {"task_input": "reliance.NS from show data using screener summary", "task_type": "summary"},
    ]


##Finally Print the data.. Of The History added

for idx, task in enumerate(tasks, start=1):
    print(f"\n\n🔄 Running Task {idx}: {task['task_type']}")
    initial_state: TaskState = {**task, "history": []}
    final_state = graph.invoke(initial_state,config=config)

    
print("\n✅ Final Output:")
for item in final_state["history"]:
    print("=========\n")
    print("Showing Final Output...\n")
    print(item)
    print("=========\n")
    




