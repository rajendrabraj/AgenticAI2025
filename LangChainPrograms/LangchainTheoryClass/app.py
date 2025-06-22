## Rajendra.  10th June 2025 
## Program for Assignment #4 


import os
import streamlit as st
import operator
from dotenv import load_dotenv 
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
#from langchain.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_community.tools.tavily_search.tool import TavilySearchResults

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

from langchain_core.runnables import RunnableConfig
from langchain_community.vectorstores import Chroma


DEBUG_MODE = True


# Load environment variables
load_dotenv()

# Set environment variables
#os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN", "")
tvly_api_key = os.getenv("TAVILY_API_KEY", "")

print("Passed the Loaded Env ..........")
print("\n")

# Initialize LLM

# model = ChatOpenAI(model="gpt-4o", temperature=0.2)

@st.cache_resource
def get_llm():
    return ChatOpenAI(model="gpt-4o", temperature=0.5)

print("Passed the LLM Execution function..........")
print("\n")
      

# Initialize embeddings
#BAAI/bge-small-en-v1.5

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")


# Get the path of the current file
current_file_path = os.path.abspath(__file__)
# If you only need the directory containing the current file:
current_file_directory = os.path.dirname(current_file_path)
data_file_path = current_file_directory + "\data2"

print(data_file_path)


print("\n")

print("-"*100)

#loader=DirectoryLoader("./data2",glob="./*.txt",loader_cls=TextLoader)
# loader=DirectoryLoader(data_file_path,glob="./*.txt",loader_cls=TextLoader)



# # Load and process documents
@st.cache_resource
def get_retriever():
    # Load documents
    print("Inside get retriever..")
    st.info("Calling Inside get retriever..")

    loader = DirectoryLoader(data_file_path, glob="**/usa.txt", loader_cls=TextLoader)  

    docs = loader.load()
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = text_splitter.split_documents(docs)
    
    # Create vector store
    #embeddings = get_embeddings()
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
    

    # db = FAISS.from_documents(chunks, embeddings)
    db=Chroma.from_documents(chunks,embeddings)
    st.info("Searching Chroma database..")
    return db.as_retriever(search_kwargs={"k": 3})



# class AgentState(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], operator.add]

# Define agent state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_action: str
    generation: str
    validation_passed: bool


# # Define agent state
# class AgentState(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], operator.add]
#     next_action: str
#     generation: str
#     validation_passed: bool

print("Passed the Class : AgentState..........")
print("\n")


# Define nodes
def llm_node(state: AgentState):
    """A node that calls an LLM for a general purpose answer."""
    st.info("Calling LLM Node")
    model = get_llm()
    response = model.invoke(state["messages"])
    print("LLM Node #1 : response:", response)  
    return {"messages": [response], "generation": response.content}


print("Passed the Function.. : llm_node..........")
print("\n")




# loader = DirectoryLoader(data_file_path, glob="**/tp.txt", loader_cls=TextLoader)  
# docs = loader.load()

# Split documents
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
# chunks = text_splitter.split_documents(docs)

lstr_file_path="C:\Rajendra_2015\AgenticAI_Programs\Agentic_Batch2\2-Langchain Basics\2.5_LangChain_Graph\data2\."
# Get the path of the current file
current_file_path = os.path.abspath(__file__)
# If you only need the directory containing the current file:
current_file_directory = os.path.dirname(current_file_path)



# RAG Function
def rag_node(state:AgentState):
    print("-> RAG Call ->")
    st.write("Inside RAG Node")
    # data_file_path = current_file_directory + "\data2"

    loader=DirectoryLoader(data_file_path,glob="./*.txt",loader_cls=TextLoader)
    docs=loader.load()
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
    st.write("RAG Docs Loaded element....") 

    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    st.write("Text Splitting completed....") 

    new_docs=text_splitter.split_documents(documents=docs)
    db=Chroma.from_documents(new_docs,embeddings)
    retriever=db.as_retriever(search_kwargs={"k": 10})

    question = state["messages"][-1].content
    # retriever = get_retriever()

    docs = retriever.invoke(question)
    rag_content = "\n".join([doc.page_content for doc in docs])

    st.write("Accessing Chroma DB....") 

    # Initialize LLM

    model = ChatOpenAI(model="gpt-4o", temperature=0.2)


    question = state["messages"][0]
    
    st.write("LLM of RAG now ....") 

    prompt=PromptTemplate(
        template="""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\nQuestion: {question} \nContext: {context} \nAnswer:""",
        input_variables=['context', 'question']
    )
    
    st.write("LLM of Prompt Completed ....") 
    chain = prompt | model

    # rag_chain = (
    #     {"context": retriever |  "question": RunnablePassthrough()}
    #     | prompt
    #     | model
    #     | StrOutputParser()
    # )
    st.write("LLM of Invoking response Completed ....") 
    response = chain.invoke({"context": rag_content, "question": question})
    return {"messages": [response], "generation": response.content}




def web_search_node(state: AgentState):
    """A node that performs a web search using Tavily for real time information."""
    st.info("Calling Web Search Node")
    question = state["messages"][-1].content
    web_search_tool = TavilySearchResults(max_results=2, api_key=tvly_api_key)
    st.write("Web Search Tool initialized")
    search_results = web_search_tool.invoke({"query": question})
    generation = "\n".join([res["content"] for res in search_results])
    response_message = AIMessage(content=generation)
    print("web_search_node Response :", response_message)  
    return {"messages": [response_message], "generation": generation}

print("Passed the Function.. : web_search_node..........")
print("\n")


def validation_node(state: AgentState):
    """A node that validates the generated output. 
    It uses an LLM to check if the generation is relevant to the question asked and fully answers it."""
    st.info("Calling Validation Node")
    question = state["messages"][0].content
    print("Inside the validation function..")
    print(question)

    generation = state["generation"]
    validation_prompt = ChatPromptTemplate.from_template(
        """Given the original user question and generated answer, please validate the following
        1. Does the answer directly address the user's question?
        2. Is the answer accurate and not hallucinated?
        3. Is the answer complete and detailed enough?

        Original Question: {question}
        Generated Answer: {generation}

        Please answer with a single word 'yes' or 'no' only.
         If the answer is valid, respond with only the word "VALID".
    If the answer is invalid, respond with "INVALID" followed by a brief, constructive critique on how to improve it for the next attempt.
    For example: "INVALID: The answer is too generic. The user asked for a specific number."
            """
    )
    model = get_llm()
    validation_chain = validation_prompt | model
    validation_response = validation_chain.invoke({"question": question, "generation": generation})
    validation_text = validation_response.content

    if "VALID" in validation_text:
        st.success("VALIDATION OK")
        return {"validation_passed": True}
    else:
        st.error("VALIDATION Failure")
        # Add the critique to the message history so the supervisor can use it
        critique_message = HumanMessage(content=f"Critique from validator: {validation_text}")
        return {"validation_passed": False, "messages": [critique_message]}

print("Passed the Function.. : validation_node..........")
print("\n")

import re 
import json

def supervisor_node(state: AgentState):
    """A node that supervises the conversation and decides which node to call next."""
    st.info("Calling Supervisor Node")
    print("Inside Supervisor Node")
    
    
    context = "\n".join([msg.pretty_repr() for msg in state["messages"][-3:]])
    last_message=state["messages"][-1]
      
    # print(last_message)
    # print(context)


    prompt = f"""You are a supervisor in a multi-agent system. Your job is to decide the next action based on the conversation history.
    The user's request is the first message. Subsequent messages might be previous attempts or critiques from a validator.

    Choose the best tool for the next step:
    - 'llm': LLM Specific data
    - 'rag': Internal Knowledge base
    - 'web_search': Searching webased questions.

    Conversation History:
    {context}

    Based on the history, what is the best next action? Respond with only one of the following: 'llm', 'rag', 'web_search'.
    """
    st.write("Showing Context....") 
    st.write(context)    

    st.write("Showing the Global input given....") 
    st.write(input_question) 

    last_message=state["messages"][-1]          
    st.write(last_message)   

    mylist = list(input_question)
    first_element = mylist[0]

    st.write("Extracted element....") 
    st.write(first_element) 

    #make everything lower for comparison
    first_element = first_element.lower()

    pattern = r"usa"
    match = re.findall( pattern , first_element)     

    
    if match:
        st.write("Matched USA")  
        ## call the RAG function to check and load the documents
        return {"next_action": "rag"}
    else:
        st.write("Did not Match USA")    
        ## Call Web Serach or LLM functions.
        model = get_llm()
        response = model.invoke(prompt)      
        st.write(response.content)
        next_action = response.content.strip().lower()
        st.write(f"Supervisor decided to call: {next_action}")
        st.write(next_action)
        return {"next_action": next_action}
            

print("Passed the Function.. : supervisor_node..........")
print("\n")


def router_function(state: AgentState):
    """A router that decides which node to call next based on the next action."""
    return state["next_action"]
    
    

print("Passed the Function.. : router_function..........")
print("\n")

def validation_router(state: AgentState):
    """A router that decides which node to call next based on the validation result."""
    if state["validation_passed"]:
        return END
    else:
        return "supervisor"
    
print("Passed the Function.. : validation_router..........")
print("\n")


## Create and show the graph.

def create_workflow():
    workflow = StateGraph(AgentState)
    print("Inside workflow..")

    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("llm", llm_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("web_search", web_search_node)

    #workflow.add_node("validation", validation_node)

    # workflow.add_node("Supervisor",function_1)
    # workflow.add_node("RAG",function_2)
    # workflow.add_node("LLM",function_3)

    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        router_function,
        {
            "llm": "llm",
            "rag": "rag",
            "web_search": "web_search",
        }
    )

    # workflow.add_edge("llm", "validation")   
    # workflow.add_edge("rag", "validation")
    # workflow.add_edge("web_search", "validation")
    # workflow.add_edge("rag", "validation")

    workflow.add_edge("llm", END)   
    workflow.add_edge("rag", END)    
    workflow.add_edge("web_search", END)
    #workflow.add_edge("validation", END)


    print("Edges added to the  workflow..")

    # workflow.add_conditional_edges(
    #     "validation",
    #     validation_router,
    #     {
    #         "supervisor": "supervisor",
    #         END: END,
    #     },
    # )

    return workflow.compile()

print("Passed the Function.. : create_workflow and Graph..........")
print("\n")

# Streamlit app
def main():
    st.title("LangGraph Multi-Agent System")

    st.write("This app demonstrates a multi-agent system using LangGraph that can answer questions using different tools.")

    
    # Create a sidebar with information
    with st.sidebar:
        st.header("About")
        st.write("""
        This app uses a multi-agent system built with LangGraph to answer questions.
        This app includes :
        SuperVisor agent, LLM agent, Web Search and RAG Agent.     
        """)
        
        st.header("Available Tools")
        st.write("- LLM: To query General Questions")
        st.write("- RAG: Search the document for information")
        st.write("- Web Search")
    
    # User input
    query = st.text_input("Ask a question:", "Tell me about iPhone 13")

    global input_question 
    input_question = {query}
    
    st.write(input_question)

    
    if st.button("Submit"):
        with st.spinner("Processing your question..."):
            # Initialize the workflow
            app = create_workflow()
            
            # Create initial state
            initial_state = {"messages": [HumanMessage(content=query)]}
            
            # Create a container for the processing steps
            process_container = st.container()
            
            # Create a container for the final answer
            answer_container = st.container()
            
            config = RunnableConfig(recursion_limit=15)

            #result = my_runnable.invoke("Initial Input", config=config)

            #for output in app.stream(initial_state, config={"recursion_limit": 10}):

            with process_container:
                st.subheader("Processing Steps:")
                # Stream the output to see the steps
                for output in app.stream(initial_state, config=config):
                    pass  # Steps are displayed via st.info/st.success/st.error in the node functions
            
            # Get the final answer
            # final_state = app.invoke(initial_state, config={"recursion_limit": 10})
            final_state = app.invoke(initial_state, config=config)
            
            with answer_container:
                st.subheader("Final Answer:")
                st.write(final_state["generation"])

if __name__ == "__main__":
    main()

print("Passed the Function.. : main()..........")
print("\n")


