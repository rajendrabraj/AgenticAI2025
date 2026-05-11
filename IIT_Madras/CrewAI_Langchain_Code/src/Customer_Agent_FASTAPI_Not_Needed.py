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
from fastapi import FastAPI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from fastapi import FastAPI, HTTPException
from loguru import logger
import pinecone
import time
import traceback

##STEP    4: LOGGING SETUP

logger.add("Deployment.log", rotation="10 MB", level="INFO")


##STEP    3: INITIALIZE APP

app = FastAPI()


# from langchain_community.memory.buffer_memory import ConversationBufferMemory

from langchain.tools import tool

try:
    import pinecone
    import importlib
    Pinecone = importlib.import_module("langchain.vectorstores").Pinecone
    PINECONE_AVAILABLE = True
except Exception as exc:
    pinecone = None
    Pinecone = None
    PINECONE_AVAILABLE = False
    print(f"Pinecone integration unavailable: {exc}")

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

embeddings = OpenAIEmbeddings()

documents = [
    "Refund policy: Users can request refund within 7 days of duplicate charge.",
    "Subscription billing issues can be resolved by verifying transaction ID.",
    "Technical issues should be escalated if unresolved within 24 hours.",
    "Personal data must never be shared with unauthorized users."
]

if PINECONE_AVAILABLE:
    pinecone_api_key = os.getenv("PINECONE_API_KEY", "")
    
    if not pinecone_api_key:
        print("PINECONE_API_KEY not found, using local fallback retrieval.")
        logging.info("PINECONE_API_KEY not found, using local fallback retrieval.")
        PINECONE_AVAILABLE = False
    else:
        try:
            print("START PineCone initialization.")
            logging.info("START PineCone initialization.")
            pinecone_client = pinecone.Pinecone(api_key=pinecone_api_key, environment='us-east-1')
            print("PineCone initialized successfully.")
            logging.info("PineCone initialized successfully")
            
            index_name = 'support-kb'
            try:
                pinecone_client.describe_index(index_name)
                print("PineCone Index exists.")
                logging.info("PineCone Index exists.")
            except:
                pinecone_client.create_index(name=index_name, dimension=1536)
                print("PineCone Index Created successfully.")
                logging.info("PineCone Index Created successfully")

            vector_store = Pinecone.from_existing_index(
                index_name=index_name,
                embedding=embeddings
            )

            vector_store.add_texts(documents)
            print("PineCone Index added documents successfully.")
            logging.info("PineCone Index added documents successfully")
        except Exception as exc:
            print(f"Pinecone initialization failed, using local fallback retrieval: {exc}")
            logging.info(f"Pinecone initialization failed, using local fallback retrieval: {exc}")
            PINECONE_AVAILABLE = False

if not PINECONE_AVAILABLE:
    document_embeddings = embeddings.embed_documents(documents)
    print("PineCone embeddings created successfully.")
    logging.info("PineCone embeddings created successfully")


def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

## RETRIEVAL FUNCTION

def retrieve_docs(query):
    if PINECONE_AVAILABLE:
        docs = vector_store.similarity_search(query, k=3)
        return [doc.page_content for doc in docs]

    query_embedding = embeddings.embed_query(query)
    similarity_scores = [
        (cosine_similarity(query_embedding, doc_vector), document)
        for document, doc_vector in zip(documents, document_embeddings)
    ]
    top_matches = sorted(similarity_scores, key=lambda pair: pair[0], reverse=True)[:3]
    return [match[1] for match in top_matches]

## TOOLS DEFINITION

##  Define the Knowledge Base Tool 

def search_knowledge_base(query: str) -> str:
    """Search internal knowledge base for accurate answers."""    
    print("Inside Knowledge Base Tool successfully.")
    logging.info("Inside Knowledge Base Tool successfully.")
    results = retrieve_docs(query)
    print(f"Retrieved documents: {results}")
    logging.info(f"Retrieved documents: {results}")
    return "\n".join(results)

def escalation_tool_human(query: str) -> str:
    """Escalate query to human agent when needed."""
    return "Escalation triggered for query: " + query


## Run this maximum 2 times. 

MAX_TOOL_CALLS = 2

def safe_tool_execution(query):
    calls = 0
    while calls < MAX_TOOL_CALLS:
        result = search_knowledge_base(query)
        if "No relevant" not in result:
            return result
        calls += 1
    return escalation_tool_human(query)


@tool
def knowledge_base_tool(query: str) -> str:
    """Search internal knowledge base for accurate answers."""    
    print("Inside Knowledge Base Tool successfully.")
    logging.info("Inside Knowledge Base Tool successfully.")
    results = retrieve_docs(query)
    print(f"Retrieved documents: {results}")
    logging.info(f"Retrieved documents: {results}")
    return "\n".join(results)

@tool
def escalation_tool(query: str) -> str:
    """Escalate query to human agent when needed."""
    return "Escalation triggered for query: " + query

knowledge_tool = knowledge_base_tool
escalation_tool_def = escalation_tool

##  Define the right Tools here 

tools = [knowledge_tool, escalation_tool_def]


## Prompt with the Tools usage 

safe_prompt_with_tools = """
You are a customer support AI.

You have access to the following tools:
- knowledge_tool: Search internal knowledge base for accurate answers
- escalation_tool: Escalate the query to a human agent when necessary


Rules:

RULES:

1. For factual or support-related queries:
   - ALWAYS call `knowledge_tool` first.

2. After using `knowledge_tool`:
   - If relevant information is found → answer using it.
   - If NO relevant information is found → respond with:
     "No relevant information found"
     AND call `escalation_tool`.

3. Call `escalation_tool` immediately if:
   - The query is sensitive (legal, financial risk, personal data)
   - The query requires human judgment
   - Confidence in the answer is low

4. DO NOT hallucinate.
5. DO NOT make up answers.
6. Use only tool outputs to answer factual queries.


---
Query: {query}
Tools : knowledge_base_tool, escalation_tool
---

Available Tools:
- KnowledgeBaseSearch: Search internal knowledge base for accurate answers
- EscalationTool: Escalate query to human agent when needed

Output format (STRICT):

Answer: <final answer to the user or "No relevant information found">
Reasoning: <brief explanation of what you did>
Tool Used: <knowledge_tool / escalation_tool / none>
Confidence: <high / medium / low>
Escalation Required: <yes / no>

"""

##Evaluation Prompt

evaluation_prompt = """
You are a customer support AI. Evaluate the response quality based on:

Accuracy: Is the response factually correct based on the knowledge base?
Safety: Does the response comply with safety and policy guidelines?
Completeness: Does it fully address the customer's query?
Clarity: Is the response clear and well-structured?
Policy Compliance: Does it follow company policies?

Query: {query}

Review the resolution provided in the previous task context.

Evaluate the following:

    Query: {query}
   

    
Score each dimension from 1 to 5.

Output:
Accuracy: [1-5]
Safety: [1-5]
Completeness: [1-5]
Clarity: [1-5]
Hallucination: [Yes/No]
Groundedness: [1-5]
Escalation Correct: [Yes/No]
Overall Score: [average]
Final Verdict (Pass/Fail)
Summary: [brief evaluation summary]



"""


## Define the Agents 

def build_agent(role: str, goal: str, backstory: str, verbose: bool = True, tools=None) -> Agent:
    return Agent(role=role, goal=goal, backstory=backstory, llm=llm, verbose=verbose, allow_delegation=False, tools=tools if tools else [])

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
    backstory="Expert in semantic search and vector databases"
    
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
    backstory="Compliance logging specialist"
)

##Evaluation AGent
##Evaluation AGent
evaluation_agent  = build_agent(
    role="Evaluator",
    goal="Evaluate response quality",
    backstory="""
    You are responsible for auditing AI responses.
    You check for correctness, groundedness, hallucination, and proper escalation decisions.
    """
)


## Agents with Tools defined. 

retrieval_agent_with_tool = build_agent(
    role="Knowledge Retriever",
    goal="Fetch accurate answers from the internal knowledge base",
    backstory="Expert in semantic search and vector databases"
    
)

escalation_agent_with_tool = Agent(
    role="Escalation Manager",
    goal="Escalate unresolved or risky queries",
    backstory="Customer experience manager",
    llm=llm,
    
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
    expected_output="Relevant documents retrieved from knowledge base or Vector database"
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

##Evaluation TAsk (Define it)
evaluation_task = build_task(
    description=evaluation_prompt,
    agent=evaluation_agent,
    expected_output="Evaluate the response based on accuracy, safety, completeness, clarity, and policy compliance with scores and overall rating"
)

#evaluation_task = Task(description=evaluation_prompt, agent=evaluation_agent, expected_output="Evaluate the response based on accuracy, safety, completeness, clarity, and policy compliance with scores and overall rating")







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
Score:
    - Accuracy (0-10)
    - Groundedness (0-10)
    - Relevance (0-10)
    - Hallucination (Yes/No)
    - Final Verdict (Pass/Fail)
    
    
"""

## Define the various kinds of prompts for experimetation 

resolution_task_basic = Task(description=basic_prompt, agent=resolution_agent, expected_output="Basic response to customer query")
resolution_task_structured = Task(description=structured_prompt, agent=resolution_agent, expected_output="Structured response with reasoning and confidence")
resolution_task_safe = Task(description=safe_prompt, agent=resolution_agent, expected_output="Safe regulated response with escalation decision")

## Mainfunction to execute the crew and run experiments 

intent_agent_with_tools = build_agent(
    role="Intent Classifier",
    goal="Identify customer intent and assign confidence score",
    backstory="Expert in NLP classification for customer support"
    
)


intent_agent_with_tools = build_agent(
    role="Intent Classifier",
    goal="Identify customer intent and assign confidence score",
    backstory="Expert in NLP classification for customer support"
    
)

## Execute this without retrieval and LLM 

def run_without_retrieval(query):
    simple_prompt = f"Answer the query: {query}"
    response = llm.invoke(simple_prompt)
    return response.content


##  Execute this WITH retrieval logic 

def run_with_retrieval(query):
    return support_crew.kickoff(inputs={"query": query})


##Define the Memory  add the memory functions 
## Add the memory Setup 

# from langchain.memory.buffer import ConversationBufferMemory

# short_term_memory = ConversationBufferMemory(
# memory_key="chat_history",
# return_messages=True
# )

long_term_memory = []


def save_to_long_term_memory(query, response):
    long_term_memory.append({
    "query": query,
    "response": response
})


## Define the long term context 

def get_long_term_context():
    history = " " 
    for item in long_term_memory[-5:]:
        history += "User: " + item["query"] + "\n"
        history += "AI: " + item["response"] + "\n"
    return history




##Store the Feedback 
feedback_store = []
def store_feedback(query, response, rating, comments):
    

    feedback_store.append({
        "query": query,
        "response": response,
        "rating": rating,
        "comments": comments
    })

def get_feedback_summary():
    negative_patterns = []
    for item in feedback_store[-10:]:
        if item["rating"] < 3:
            negative_patterns.append(item["query"])
    return "\n".join(negative_patterns)



## Reset of the memory

def reset_memory():
   # short_term_memory.clear()
   long_term_memory.clear()



## Defining the : Multi Turn Conversation functions and Memory

##Define Memory Crew

def run_experiment_memory(query: str, memory: str):
    memory_crew = Crew(
        agents=[
            intent_agent,
            safety_agent,
            retrieval_agent,
            resolution_agent,
            escalation_agent,
            audit_agent,
            evaluation_agent,
        ],
        tasks=[
            intent_task,
            safety_task,
            retrieval_task,
            resolution_task,
            escalation_task,
            audit_task,
            evaluation_task,
        ],
        verbose=True,
    )
    return memory_crew.kickoff(inputs={"query": query,"memory": memory})




##Define Memory and save the Conversational History
### Memory Functions

def run_memory_conversation(query):
    logging.info("START : Inside run_memory_conversation function with query: " + query)
    
    memory_context = get_long_term_context()
    logging.info(f"Memory History: {memory_context}")
    
    logging.info("START Inside Function   : Call Experiment Memory Crew : ")    
    result_memory_check = run_experiment_memory(query, memory_context)
    logging.info("END Inside Function : Call Experiment Memory Crew : ")
    logging.info(f"Memory CREW Result(Inside Function): {result_memory_check}")    

    # short_term_memory.save_context(
    #     {"input": query},
    #     {"output": str(result_memory_check)}
    # )

    save_to_long_term_memory(query, str(result_memory_check))

    return result_memory_check


## Define the Memory with Feedback Context Agent 
def run_experiment_memory_with_context(query: str, memory: str, feedback_context : str ):
    memory_crew_with_context = Crew(
        agents=[
            intent_agent,
            safety_agent,
            retrieval_agent,
            resolution_agent,
            escalation_agent,
            audit_agent,
            evaluation_agent,
        ],
        tasks=[
            intent_task,
            safety_task,
            retrieval_task,
            resolution_task,
            escalation_task,
            audit_task,
            evaluation_task,
        ],
        verbose=True,
    )
    return memory_crew_with_context.kickoff(inputs={"query": query,"memory": memory ,"feedback_context" : feedback_context })


def run_conversation_memory_context(query):
    memory_context = get_long_term_context()
    feedback_context = get_feedback_summary()

    logging.info("START : Inside run_conversation_memory_context function with query: " + query)
    logging.info("START : Inside run_conversation_memory_context function with memory context : " + memory_context)
    logging.info("START : Inside run_conversation_memory_context function with feedback context : " + feedback_context)

    logging.info("START Inside Function   : Call Experiment memory_crew_with_context  : ")    
    
    ##Execute with Memory Context Crew Agent 
    result_memory_context = run_experiment_memory_with_context(query, memory_context, feedback_context)

    logging.info("END Inside Function : Call Experiment memory_crew_with_context : ")

    save_to_long_term_memory(query, str(result_memory_context))
    return result_memory_context



##This is the main function

def execute_deployment_tracking(query):
    start_time = time.time()
    logging.info("START- Running #10 Deployment : Crew Agent Defined")
    support_crew_Evaluation= Crew(
        agents=[
            intent_agent,
            safety_agent,
            retrieval_agent,
            resolution_agent,
            escalation_agent,
            audit_agent,
            evaluation_agent,
        ],
        tasks=[
            intent_task,
            safety_task,
            retrieval_task,
            resolution_task,
            escalation_task,
            audit_task,
            evaluation_task,
        ],
        verbose=True,
    )


    try:
        print("\n---START Running #10 Deployment Agent Test ---\n")
        logging.info("START- Running #10 Deployment Agent Test")

        result_evaluation = support_crew_Evaluation.kickoff(
            inputs={"query": query}
            
            
        )

        print("Result Deployment Agent Test: " + str(result_evaluation))
        print("-" * 90)

        logging.info("END- Running #10 Deployment Agent Test")
        logging.info(f"Result: {result_evaluation}")

        latency = time.time() - start_time

        logging.info("SUCCESS")
        logging.info("Latency: " + str(latency))

        return {
            "result": str(result_evaluation),
            "latency": latency,
            "status": "SUCCESS"
        }

    except Exception as e:
        latency = time.time() - start_time

        logging.error("FAILURE")
        logging.error(traceback.format_exc())

        return {
            "result": "RUN -#10 Deployment Agent: System error. Escalating to human agent.",
            "latency": latency,
            "status": "FAILED"
        }




def main() -> None:
    from fastapi import FastAPI, HTTPException    
    print("\n---START Running #10 FAST API loaded successfully ---\n")
    logging.info("START- Running #10 FAST API loaded successfully")
    app = FastAPI()

    @app.post("/support")
    def support_endpoint(request: dict):
        query = request.get("query")
        logging.info("START- Running #10 End point /support called with query: " + str(query))        
        if not query:
            raise HTTPException(status_code=400, detail="Query missing")

        return execute_deployment_tracking(query)




if __name__ == "__main__":
    main()
