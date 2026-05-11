## Rajendra Bichu : Date : 29.04.2026 , Version 1.0

## Customer Support — AI Support Resolution Agent
## This script builds a CrewAI workflow for customer support.
## It classifies intent, checks safety, retrieves knowledge, generates a response,
## escalates unresolved or sensitive cases, and logs decisions safely.


## Import necessary libraries and modules 


import os
import logging
import warnings
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.tools import Tool
import pinecone


load_dotenv()
warnings.filterwarnings("ignore")

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
logs_directory_path = os.path.join(parent_directory, "logs")
os.makedirs(logs_directory_path, exist_ok=True)

pinecone_api_key = os.getenv("PINECONE_API_KEY", "")
print(f"Example variable PINECONE_API_KEY : {pinecone_api_key}")


## Enable logging to a file with INFO level and a specific format


logging.basicConfig(
    filename=os.path.join(logs_directory_path, "Customer_Support_LOG.log"),
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

##Pincone setup

## PINECONE INITIALIZATION

pinecone.init(
    api_key=pinecone_api_key,
    environment='us-east-1'
)

index_name = 'support-kb'

if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536)

## EMBEDDINGS SETUP

embeddings = OpenAIEmbeddings()

vector_store = Pinecone.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

## SAMPLE DOCUMENT INGESTION

documents = [
    "Refund policy: Users can request refund within 7 days of duplicate charge.",
    "Subscription billing issues can be resolved by verifying transaction ID.",
    "Technical issues should be escalated if unresolved within 24 hours.",
    "Personal data must never be shared with unauthorized users."
]

vector_store.add_texts(documents)

## RETRIEVAL FUNCTION

def retrieve_docs(query):
    docs = vector_store.similarity_search(query, k=3)
    return [doc.page_content for doc in docs]

## TOOLS DEFINITION

##  Define the Knowledge Base Tool 

def knowledge_base_tool(query):
    results = retrieve_docs(query)
    return "\n".join(results)

##  Define the Escalation Base Tool 

def escalation_tool(query):
    return "Escalation triggered for query: " + query

knowledge_tool = Tool(
    name="KnowledgeBaseSearch",
    func=knowledge_base_tool,
    description="Search internal knowledge base for accurate answers"
)

escalation_tool_def = Tool(
    name="EscalationTool",
    func=escalation_tool,
    description="Escalate query to human agent when needed"
)

##  Define the right Tools here 

tools = [knowledge_tool, escalation_tool_def]

## Prompt with the Tools usage 

safe_prompt_with_tools = """
You are a production-grade customer support AI.
Rules:

Always try KnowledgeBaseSearch first for factual queries
Use EscalationTool if:
- confidence is low
- query is sensitive
- no relevant data found
Do not hallucinate
If no data found, say "No relevant information found"
Query: {query}

Available Tools:
{tools}

Output format:
Answer:
Reasoning:
Tool Used:
Confidence:
Escalation Required:
"""


## Define the Agents 

def build_agent(role: str, goal: str, backstory: str, verbose: bool = True, tools=None) -> Agent:
    return Agent(role=role, goal=goal, backstory=backstory, llm=llm, verbose=verbose, tools=tools)

## Define the Tasks 
def build_task(description: str, agent: Agent, expected_output: str = "Task completed") -> Task:
    return Task(description=description, agent=agent, expected_output=expected_output)

## Define the Agents 

intent_agent = build_agent(
    role="Intent Classifier",
    goal="Identify customer intent and assign confidence score",
    backstory="Expert in NLP classification for customer support",
)

safety_agent = build_agent(
    role="Safety Guard",
    goal="Ensure compliance and block unsafe or policy-violating queries",
    backstory="Compliance expert ensuring safe AI behavior",
)

retrieval_agent = build_agent(
    role="Knowledge Retriever",
    goal="Fetch accurate answers from the internal knowledge base",
    backstory="Expert in semantic search and vector databases",
    tools=[knowledge_tool]
)

resolution_agent = build_agent(
    role="Resolution Generator",
    goal="Generate final response with explanation and confidence",
    backstory="Customer support specialist trained on SOPs",
)

escalation_agent = build_agent(
    role="Escalation Manager",
    goal="Escalate unresolved or sensitive queries to human agents",
    backstory="Customer experience manager",
)

audit_agent = build_agent(
    role="Audit Logger",
    goal="Log decisions without storing personal data",
    backstory="Compliance logging specialist",
)

## Agents with Tools defined. 

retrieval_agent_with_tool = build_agent(
    role="Knowledge Retriever",
    goal="Fetch accurate answers from the internal knowledge base",
    backstory="Expert in semantic search and vector databases",
    tools=[knowledge_tool]
)

escalation_agent_with_tool = Agent(
    role= "Escalation Manager",
    goal= "Escalate unresolved or risky queries",
    tools=[escalation_tool_def]
   
)


## Define the Tasks here we can add expected_output for better clarity on what each task should return 

intent_task = build_task(
    description="Classify user intent and assign confidence score",
    agent=intent_agent,
    expected_output="Intent classification with confidence score"
)

safety_task = build_task(
    description="Check for unsafe content and redact personal data",
    agent=safety_agent,
    expected_output="Safety check result with data redaction"
)

retrieval_task = build_task(
    description="Retrieve relevant documents from the knowledge base",
    agent=retrieval_agent,
    expected_output="Relevant documents retrieved from knowledge base"
)

resolution_task_with_tools  = build_task(
    description=safe_prompt_with_tools,
    agent=resolution_agent,
    expected_output="Relevant documents retrieved from knowledge base"
)



resolution_task = build_task(
    description="Generate final response using retrieved knowledge",
    agent=resolution_agent,
    expected_output="Final resolution response with explanation"
)

escalation_task = build_task(
    description="Determine if escalation to human is required",
    agent=escalation_agent,
    expected_output="Escalation decision with reasoning"
)

audit_task = build_task(
    description="Log decision path safely without storing PII",
    agent=audit_agent,
    expected_output="Audit log entry without personal data"
)


## Define the actual crew to launch later with all the agents and tasks 

support_crew = Crew(
    agents=[
        intent_agent,
        safety_agent,
        retrieval_agent,
        resolution_agent,
        escalation_agent,
        audit_agent,
    ],
    tasks=[
        intent_task,
        safety_task,
        retrieval_task,
        resolution_task,
        escalation_task,
        audit_task,
    ],
    verbose=True,
)

## Run Experiments with different prompts for the resolution task to see how it affects the output and escalation decisions 


def run_experiment(prompt_task: Task, query: str):
    crew = Crew(
        agents=[
            intent_agent,
            safety_agent,
            retrieval_agent,
            resolution_agent,
            escalation_agent,
            audit_agent,
        ],
        tasks=[
            intent_task,
            safety_task,
            retrieval_task,
            prompt_task,
            escalation_task,
            audit_task,
        ],
        verbose=False,
    )
    return crew.kickoff(inputs={"query": query})


## Define the various kinds of prompts for experimetation


basic_prompt = """
Answer the customer query clearly.

Query: {query}
"""

structured_prompt = """
You are a customer support assistant.

Steps:
- Understand the issue
- Use only provided knowledge
- Give clear resolution

Query: {query}

Provide:
- Answer
- Reason
- Confidence (low, medium, high)
"""

safe_prompt = """
You are a regulated customer support AI.

Rules:
- Do not hallucinate policies
- Use only retrieved knowledge
- If unsure, say "I am not certain"
- If sensitive, escalate
- Do not include personal data

Query: {query}

Output format:
Answer:
Reasoning:
Confidence:
Escalation Required: Yes/No
"""

## Define the various kinds of prompts for experimetation 

resolution_task_basic = Task(description=basic_prompt, agent=resolution_agent, expected_output="Basic response to customer query")
resolution_task_structured = Task(description=structured_prompt, agent=resolution_agent, expected_output="Structured response with reasoning and confidence")
resolution_task_safe = Task(description=safe_prompt, agent=resolution_agent, expected_output="Safe regulated response with escalation decision")

## Mainfunction to execute the crew and run experiments 


def main() -> None:
    query = "I was charged twice for my subscription"
    logging.info("Crew Agent kickoff started")

    result = support_crew.kickoff(inputs={"query": query})
    print("\n--- Crew AI Agent First System Response ---\n")
    print(result)
    print("-" * 90)
    logging.info("Crew Agent executed successfully")
    logging.info(f"Result: {result}")

    print("\n--- Execute Crew AI Agent Prompt Variants ---\n")
    logging.info("Executing prompt experiments")

## Run Experiments with different prompts for the resolution task to see how it affects the output and escalation decisions 


    output_basic = run_experiment(resolution_task_basic, query)
    output_structured = run_experiment(resolution_task_structured, query)
    output_safe = run_experiment(resolution_task_safe, query)

    print("BASIC OUTPUT:", output_basic)
    print("STRUCTURED OUTPUT:", output_structured)
    print("SAFE OUTPUT:", output_safe)

    logging.info(f"BASIC OUTPUT Prompt Result : {output_basic}")
    logging.info(f"STRUCTURED OUTPUT Prompt Result : {output_structured}")
    logging.info(f"SAFE OUTPUT Prompt Result : {output_safe}")

    print("-" * 90)

## Safe Prompt Workflow with Escalation Logic and execute the task


    safe_resolution_task = Task(description=safe_prompt, agent=resolution_agent, expected_output="Safe regulated response with escalation decision")
    crew_with_safe_task = Crew(
        agents=[
            intent_agent,
            safety_agent,
            retrieval_agent,
            resolution_agent,
            escalation_agent,
            audit_agent,
        ],
        tasks=[
            intent_task,
            safety_task,
            retrieval_task,
            safe_resolution_task,
            escalation_task,
            audit_task,
        ],
        verbose=True,
    )

    ## Execute the crew with the safe prompt and see how it handles the query with the new rules and escalation logic
    
    safe_result = crew_with_safe_task.kickoff(inputs={"query": query})
    print("\n--- Crew AI Agent System Response with Safe Prompt ---\n")
    print(safe_result)
    print("-" * 90)
    logging.info("Executed safe prompt workflow")
    logging.info(f"Safe prompt result: {safe_result}")
    
    ##New Execution again for new Agents
    
    
    safe_resolution_task = Task(description=safe_prompt_with_tools, agent=resolution_agent, expected_output="Safe regulated response with escalation decision")
    crew_with_safe_resolution_task = Crew(
        agents=[
            intent_agent,
            safety_agent,
            retrieval_agent,
            resolution_agent,
            escalation_agent,
            audit_agent,
        ],
        tasks=[
            intent_task,
            safety_task,
            resolution_task_with_tools,
            safe_resolution_task,
            escalation_task,
            audit_task,
        ],
        verbose=True,
    )

    query = "I was charged twice for my subscription"
    safe_result_tools = crew_with_safe_resolution_task.kickoff(inputs={"query": query})
    print("\n--- Crew AI Agent System Response with Safe Prompt ---\n")
    print(safe_result_tools)
    print("-" * 90)
    logging.info("Executed New Crew with Tools in Resolution Task workflow")
    logging.info(f"Safe prompt result: {safe_result_tools}")

if __name__ == "__main__":
    main()
