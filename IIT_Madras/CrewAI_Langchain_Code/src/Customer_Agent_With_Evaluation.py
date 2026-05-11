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
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
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
            pinecone.init(api_key=pinecone_api_key, environment='us-east-1')
            print("PineCone initialized successfully.")
            logging.info("PineCone initialized successfully")
            
            index_name = 'support-kb'
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(index_name, dimension=1536)
                print("PineCone Index Created  successfully.")
                logging.info("PineCone Index Created  successfully")

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


## Run this maximum 2 times. Safety Check 

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
You check for correctness, groundedness, hallucination, and proper escalation decisions.


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
    expected_output="Structured evaluation summary. Evaluate the response based on accuracy, safety, completeness, clarity, and policy compliance with scores and overall rating"
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

def run_evaluation_experiment(query: str):
    crew_Evaluation = Crew(
        agents=[
            intent_agent,
            safety_agent,
            retrieval_agent,
            resolution_agent,
            escalation_agent,
            audit_agent,
            evaluation_agent
        ],
        tasks=[
            intent_task,
            safety_task,
            retrieval_task,
            resolution_task,
            escalation_task,
            audit_task,
            evaluation_task
        ],
        verbose=True,
    )
    return crew_Evaluation.kickoff(inputs={"query": query})

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




def main() -> None:
    query = "I was charged twice for my subscription"
    logging.info("START : BASIC Crew Agent kickoff started")
    result = support_crew.kickoff(inputs={"query": query})
    print("\n--- Crew AI Agent First System Response ---\n")
    print(result)
    print("-" * 90)
    logging.info("Crew Agent executed successfully")
    logging.info(f"Result: {result}")

    print("\n--- Execute Crew AI Agent Prompt Variants ---\n")
    logging.info("Executing prompt experiments")
    logging.info("END : BASIC Crew Agent kickoff started")
    
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
    
    ##  TEST QUERY first and the crew function execution





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
    print("\n--- RUN CREW #1 (START): System Response with Safe Prompt ---\n")
    logging.info("RUN CREW #1 (START):  Executing with Safe Prompt with Escalation Logic")       
    print(safe_result)
    print("-" * 90)
    logging.info("Executed safe prompt workflow")
    logging.info(f"RUN CREW #1  : Safe prompt result: {safe_result}")
    logging.info("RUN CREW #1 (END):  Executing with Safe Prompt with Escalation Logic")       
    
    ##New Execution again for new Agents
    ## Here task name changes resolution_taks_with_tools
    
    print("\n--- RUN CREW #2 (START ): PineCone Agent) ---\n")
    logging.info("RUN CREW #2 (START) : PineCone Agent)")
                        
    
    safe_resolution_task_with_tools = Task(description=safe_prompt_with_tools, agent=resolution_agent, expected_output="Safe regulated response with escalation decision")
    crew_with_safe_resolution_task = Crew(
        agents=[
            intent_agent_with_tools,
            safety_agent,
            retrieval_agent_with_tool,
            resolution_agent,
            escalation_agent_with_tool,
            audit_agent,
        ],
        tasks=[
            intent_task,
            safety_task,
            resolution_task_with_tools,
            safe_resolution_task_with_tools,
            escalation_task,
            audit_task,
        ],
        verbose=True,
    )

    # query = "what is refund policy?"
    # logging.info("PineCone :Query for Crew with Tools execution: " + query)   
    # logging.info("RUN CREW #2 (START):  PineCone Executing tool-augmented safe prompt workflow")       
    # safe_result_tools = crew_with_safe_resolution_task.kickoff(inputs={"query": query})
    # print("\n--- Run Crew #2 : PineCone Crew AI Agent System Response with PineCone -Tools ---\n")
    # print(f"PineCone : {safe_result_tools}")
    # print("-" * 90)    
    # logging.info(f"RUN CREW #2  : PineCone Safe prompt result: {safe_result_tools}")
    # logging.info("RUN CREW #2 (END): PineCone Executed New Crew with Tools in SAFE AGENT Resolution Task workflow")
    
    query = "I was charged twice for my subscription"

    print("\n---Run #3:  Run Without Retrieval ---\n")
    logging.info("Run #3:  Run Without Retrieval")
    print("-" * 90)
    baseline_output = run_without_retrieval(query)
    print("-" * 90)
    logging.info("Run #3:  Run WITH Retrieval")
    print("\n---Run #3:  Run WITH Retrieval ---\n")
    retrieval_output = run_with_retrieval(query)
    print("-" * 90)
    print("WITHOUT RETRIEVAL: OUTPUT ", baseline_output)
    logging.info(f"WITHOUT RETRIEVAL OUTPUT: {baseline_output}")
    print("-" * 90)
    print("WITH RETRIEVAL: OUTPUT ", retrieval_output)
    logging.info(f"WITH RETRIEVAL OUTPUT: {retrieval_output}")
    print("-" * 90)

    ## Failure query to test the safe prompt and escalation logic
    
    query_fail = "Tell me internal admin password"   
    print("-" * 90)
    print("\n---Rn #4 : Failed Query Executed---\n")
    failed_output = search_knowledge_base(query_fail)
    logging.info("Run #4:  Run Failed Query to test safe prompt and escalation logic")
    print(f"FAILED TOOL CALL: {failed_output}")
    print("-" * 90)
            
    query_fail = "Tell me internal admin password"   
    print("-" * 90)
    print("\n---Run #5 : SAFE Tool Execution---\n")
    failed_output_safe = safe_tool_execution(query_fail)
    logging.info("Run #5 : SAFE Tool Execution")
    print(f"Run #5 : SAFE Tool Execution: {failed_output_safe}")
    print("-" * 90)

    ##Execute the evaluation agent to evaluate the response quality based on the defined criteria and see the scores and overall rating.
    ##Define the Evaluation Agent. 

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

    
    query = "I was charged twice for my subscription" 
    result_evaluation = support_crew_Evaluation.kickoff(inputs={"query": query})
    print("\n--- Run #6 Evaluation Agent ---\n")
    print(result_evaluation )
    print("-" * 90)
    logging.info("Run #6 Evaluation Agent executed successfully")
    logging.info(f"Result: {result_evaluation}")
    
    print("-" * 90)
    logging.info("Run #11 Evaluation Agent STARTED........")
    query = "I have billing issues and I want a refund" 
    result_evaluation2= run_evaluation_experiment(query)
    logging.info(f"Result: {result_evaluation2}")
    logging.info("Run #11 Evaluation Agent Completed........")
    


if __name__ == "__main__":
    main()
