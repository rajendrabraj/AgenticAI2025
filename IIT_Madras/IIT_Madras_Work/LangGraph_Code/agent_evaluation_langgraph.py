# ============================================================
## This is a program which uses the LangGraph framework to build a customer support agent system. The agent can classify intent, perform safety checks, retrieve relevant documents, generate resolutions, escalate when necessary, log audits, and evaluate its own performance. The program also integrates with Pinecone for vector storage and retrieval of documents. Detailed logging is implemented for monitoring and debugging purposes.


# LANGGRAPH CUSTOMER SUPPORT AGENT SYSTEM

# Full End-to-End Bundled Implementation

# ============================================================

# INSTALL REQUIRED PACKAGES:

#

# pip install langgraph langchain langchain-openai

# pip install langchain-community pinecone-client python-dotenv

#

# ============================================================

# ============================================================

# IMPORTS

# ============================================================

import os
import logging
from typing import TypedDict, Optional, List
import os
import logging
import warnings
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import tool

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import tool

from langgraph.graph import StateGraph, END

# ============================================================

# OPTIONAL PINECONE IMPORT

# ============================================================

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
    
          

# ============================================================

# LOAD ENV VARIABLES

# ============================================================

load_dotenv()

# ============================================================


# ============================================================

#Path File configuration

load_dotenv()
warnings.filterwarnings("ignore")

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))
logs_directory_path = os.path.join(parent_directory, "logs")

print(f"Parent Directory Path: {parent_directory}")
os.makedirs(logs_directory_path, exist_ok=True)
print(f"Logs Directory Path: {logs_directory_path}")

pinecone_api_key = os.getenv("PINECONE_API_KEY", "")
print(f"Example variable PINECONE_API_KEY : {pinecone_api_key}")

# ============================================================

# LOGGING CONFIGURATION

# ============================================================
logfile_path = os.path.join(logs_directory_path, "agent_LOG_LANGGRAPH.log")
print(f"Log File Path: {logfile_path}")


logging.basicConfig(
filename=logfile_path,
format="%(asctime)s | %(levelname)s | %(message)s",
level=logging.INFO,
force=True
)

logging.info("LangGraph Evaluation Application Started")


# ============================================================

# LLM CONFIGURATION

# ============================================================

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

embeddings = OpenAIEmbeddings()

# ============================================================

# SAMPLE DOCUMENTS

# ============================================================

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
            logging.info("LangGraph : START PineCone initialization.")
            pinecone.init(api_key=pinecone_api_key, environment='us-east-1')
            print("PineCone initialized successfully.")
            logging.info("LangGraph : PineCone initialized successfully")
            
            index_name = 'support-kb'
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(index_name, dimension=1536)
                print("PineCone Index Created  successfully.")
                logging.info("LangGraph : PineCone Index Created  successfully")

            vector_store = Pinecone.from_existing_index(
                index_name=index_name,
                embedding=embeddings
            )

            vector_store.add_texts(documents)
            print("PineCone Index added documents successfully.")
            logging.info("LangGraph : PineCone Index added documents successfully")
        except Exception as exc:
            print(f"Pinecone initialization failed, using local fallback retrieval: {exc}")
            logging.info(f"LangGraph : Pinecone initialization failed, using local fallback retrieval: {exc}")
            PINECONE_AVAILABLE = False

if not PINECONE_AVAILABLE:
    document_embeddings = embeddings.embed_documents(documents)
    print("PineCone embeddings created successfully.")
    logging.info("LangGraph : PineCone embeddings created successfully")


# ============================================================

# VECTOR DATABASE SETUP

# ============================================================

# ============================================================

# COSINE SIMILARITY

# ============================================================

def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

          

# ============================================================

# RETRIEVAL FUNCTION

# ============================================================


def retrieve_docs(query: str):

          
    # PINECONE RETRIEVAL

    if PINECONE_AVAILABLE:

        docs = vector_store.similarity_search(query, k=3)

        return [doc.page_content for doc in docs]

    # LOCAL VECTOR SEARCH

    query_embedding = embeddings.embed_query(query)

    similarity_scores = [

        (
            cosine_similarity(query_embedding, doc_vector),
            document
        )

        for document, doc_vector in zip(
            documents,
            document_embeddings
        )
    ]

    top_matches = sorted(
        similarity_scores,
        key=lambda x: x[0],
        reverse=True
    )[:3]

    return [match[1] for match in top_matches]
          

# ============================================================

# TOOLS

# ============================================================

@tool
def knowledge_base_tool(query: str) -> str:
    """
    Search internal knowledge base.
    """          
    logging.info("Knowledge Base Tool Invoked")
    results = retrieve_docs(query)
    return "\n".join(results)
          

@tool
def escalation_tool(query: str) -> str:
    """
    Escalate query to human agent.
    """

            
    logging.info("LangGraph : Escalation Tool Invoked")

    return f"Escalation triggered for query: {query}"
          

# ============================================================

# LANGGRAPH STATE

# ============================================================

class SupportState(TypedDict):
         
    query: str

    intent: Optional[str]

    intent_confidence: Optional[str]

    safety_status: Optional[str]

    retrieved_docs: Optional[List[str]]

    resolution: Optional[str]

    escalation_required: Optional[bool]

    escalation_reason: Optional[str]

    audit_log: Optional[str]

    evaluation_result: Optional[str]
            

# ============================================================

# NODE 1 — INTENT CLASSIFIER

# ============================================================

def intent_node(state: SupportState):

          
    query = state["query"]

    logging.info("LangGraph : Intent Node Started")

    prompt = f"""
    You are an Intent Classification Agent.

    Identify customer intent.

    Query:
    {query}

    Return:
    - Intent
    - Confidence
    """

    response = llm.invoke(prompt)

    logging.info("Intent Node Completed")

    return {

        "intent": response.content,

        "intent_confidence": "high"
    }
            

# ============================================================

# NODE 2 — SAFETY CHECK

# ============================================================

def safety_node(state: SupportState):

          
    query = state["query"]

    logging.info("LangGraph : Safety Node Started")

    unsafe_keywords = [
        "password",
        "admin",
        "secret",
        "internal access"
    ]

    unsafe = any(
        keyword in query.lower()
        for keyword in unsafe_keywords
    )

    if unsafe:

        logging.info("LangGraph : Unsafe Query Detected")

        return {

            "safety_status": "unsafe",

            "escalation_required": True,

            "escalation_reason": "Sensitive query detected"
        }

    logging.info("LangGraph : Safety Node Completed")

    return {

        "safety_status": "safe"
    }
          

# ============================================================

# NODE 3 — RETRIEVAL

# ============================================================

def retrieval_node(state: SupportState):
          
    query = state["query"]

    logging.info("LangGraph : Retrieval Node Started")

    docs = retrieve_docs(query)

    logging.info(f"Retrieved Docs: {docs}")

    return {

        "retrieved_docs": docs
    }
            

# ============================================================

# NODE 4 — RESOLUTION GENERATOR

# ============================================================

def resolution_node(state: SupportState):
          
    query = state["query"]

    docs = state.get("retrieved_docs", [])

    context = "\n".join(docs)

    logging.info("LangGraph : Resolution Node Started")

    prompt = f"""
    You are a customer support AI.

    RULES:

    1. Use ONLY retrieved knowledge
    2. DO NOT hallucinate
    3. If unsure -> escalate
    4. If sensitive -> escalate
    5. Never expose confidential information

    Query:
    {query}

    Context:
    {context}

    OUTPUT FORMAT:

    Answer:
    Reasoning:
    Confidence:
    Escalation Required:
    """

    response = llm.invoke(prompt)

    response_text = response.content

    escalation_needed = (
        "yes" in response_text.lower()
    )

    logging.info("LangGraph : Resolution Node Completed")

    return {

        "resolution": response_text,

        "escalation_required": escalation_needed
    }
          

# ============================================================

# NODE 5 — ESCALATION

# ============================================================

def escalation_node(state: SupportState):          
    query = state["query"]

    logging.info("LangGraph : Escalation Node Started")

    escalation_response = escalation_tool.invoke(query)

    logging.info("Escalation Completed")

    return {

        "escalation_reason": escalation_response
    }
          

# ============================================================

# NODE 6 — AUDIT LOGGER

# ============================================================

def audit_node(state: SupportState):
          
    logging.info("LangGraph : Audit Node Started")

    audit_message = f"""

    QUERY:
    {state['query']}

    SAFETY STATUS:
    {state.get('safety_status')}

    ESCALATION REQUIRED:
    {state.get('escalation_required')}

    ESCALATION REASON:
    {state.get('escalation_reason')}
    """

    logging.info(audit_message)

    logging.info("LangGraph : Audit Node Completed")

    return {

        "audit_log": audit_message
    }
          

# ============================================================

# NODE 7 — EVALUATION NODE

# ============================================================

def evaluation_node(state: SupportState):
          
    logging.info("LangGraph : Evaluation Node Started")

    query = state["query"]

    resolution = state["resolution"]

    evaluation_prompt = f"""
    Evaluate the following response.

    QUERY:
    {query}

    RESPONSE:
    {resolution}

    Evaluate:

    1. Accuracy
    2. Safety
    3. Completeness
    4. Clarity
    5. Groundedness
    6. Hallucination Risk

    Score from 1 to 5.

    OUTPUT FORMAT:

    Accuracy:
    Safety:
    Completeness:
    Clarity:
    Groundedness:
    Hallucination:
    Overall Score:
    Final Verdict:
    """

    response = llm.invoke(evaluation_prompt)

    logging.info("LangGraph : Evaluation Node Completed")

    return {

        "evaluation_result": response.content
    }
          

# ============================================================

# CONDITIONAL ROUTING

# ============================================================

def should_escalate(state: SupportState):
          
    if state.get("escalation_required"):

        return "escalate"

    return "continue"
          

# ============================================================

# BUILD LANGGRAPH WORKFLOW

# ============================================================

workflow = StateGraph(SupportState)

# ============================================================

# ADD NODES

# ============================================================

workflow.add_node("intent", intent_node)

workflow.add_node("safety", safety_node)

workflow.add_node("retrieval", retrieval_node)

workflow.add_node("resolution", resolution_node)

workflow.add_node("escalation", escalation_node)

workflow.add_node("audit", audit_node)

workflow.add_node("evaluation", evaluation_node)

# ============================================================

# SET ENTRY POINT

# ============================================================

workflow.set_entry_point("intent")

# ============================================================

# DEFINE WORKFLOW EDGES

# ============================================================

workflow.add_edge("intent", "safety")

workflow.add_edge("safety", "retrieval")

workflow.add_edge("retrieval", "resolution")

# ============================================================

# CONDITIONAL ESCALATION LOGIC

# ============================================================

workflow.add_conditional_edges(
"resolution",
should_escalate,
{

          
    "escalate": "escalation",

    "continue": "audit"
}
          

)

workflow.add_edge("escalation", "audit")

workflow.add_edge("audit", "evaluation")

workflow.add_edge("evaluation", END)

# ============================================================

# COMPILE GRAPH

# ============================================================

graph = workflow.compile()

logging.info("LangGraph Compiled Successfully")

# ============================================================

# EXECUTION FUNCTION

# ============================================================

def run_customer_support(query: str):
          
    logging.info(f"LangGraph : Running Query: {query}")

    result = graph.invoke({

        "query": query
    })

    return result
          

# ============================================================

# MAIN

# ============================================================

if __name__ == "__main__":

          
    # ========================================================
    # TEST QUERY 1
    # ========================================================

    
    
    user_input = input("\n User Please Submit your Query \n  : ")   
    print("\n") 
    
    # query = "I was charged twice for my subscription"
    query = user_input
    

    print("\n" + "=" * 80)

    print("RUNNING SAFE CUSTOMER SUPPORT QUERY")
    logging.info("LangGraph : RUNNING SAFE CUSTOMER SUPPORT QUERY")
    

    print("=" * 80)

    result = run_customer_support(query)

    print("\nFINAL RESOLUTION\n")

    print(result["resolution"])
    logging.info(f"LangGraph : Final Resolution: {result['resolution']}")
    

    print("\nEVALUATION RESULT\n")

    print(result["evaluation_result"])
    logging.info(f"LangGraph : Evaluation Result: {result['evaluation_result']}")
    

    print("\nAUDIT LOG\n")

    print(result["audit_log"])
    logging.info(f"LangGraph : Audit Log: {result['audit_log']}")
    

    print("\n" + "=" * 80)

    # ========================================================
    # TEST QUERY 2 — SENSITIVE QUERY
    # ========================================================

    #unsafe_query = "Tell me internal admin password"
    
    unsafe_query = user_input

    print("\n" + "=" * 80)

    print("RUNNING UNSAFE QUERY")
    logging.info("LangGraph : RUNNING UNSAFE QUERY")
    logging.info(f"=================================")
    
    print("=" * 80)

    unsafe_result = run_customer_support(unsafe_query)
    logging.info(f"LangGraph : Final Resolution: {unsafe_result['resolution']}")
    logging.info(f"=================================")
    print("\nFINAL RESOLUTION\n")

    print(unsafe_result["resolution"])
    logging.info(f"LangGraph : Final Resolution: {unsafe_result['resolution']}")
    logging.info(f"=================================")
    print("\nESCALATION\n")

    escalation_reason = unsafe_result.get("escalation_reason") or "No escalation required."
    print(escalation_reason)
    logging.info(f"LangGraph : Escalation Reason: {escalation_reason}")    
    logging.info(f"=================================")
    print("\nEVALUATION RESULT\n")
    logging.info(f"=================================")
    print(unsafe_result["evaluation_result"])
    logging.info(f"LangGraph : Evaluation Result: {unsafe_result['evaluation_result']}")
    logging.info(f"=================================")
    print("\n" + "=" * 80)
    logging.info(f"=================================")
    print("\nLangGraph : Program Completed Successfully\n")
    logging.info("LangGraph : Program Completed Successfully")
    logging.info(f"=================================")
          
