import uuid
import streamlit as st
from dotenv import load_dotenv
from dotenv import load_dotenv, find_dotenv
import os

#load_dotenv()

# Find the .env file, searching upwards in the directory tree
dotenv_path = find_dotenv()
# Load the .env file
load_dotenv(dotenv_path)
# Now you can access environment variables
print(f"Path to .env file: {dotenv_path}")

openai_api_key = os.getenv("OPENAI_API_KEY", "")
print(f"OpenAI API Key: {openai_api_key[:4]}...")  # Print only the first 4 characters for security 
langsmith_api_key = os.getenv("LANGSMITH_API_KEY", "")      
print(f"LangSmith API Key: {langsmith_api_key[:4]}...")  # Print only the first 4 characters for security

# serper_api_key = os.getenv("SERPER_API_KEY", "")      
# print(f"Example variable SERPER_API_KEY : {serper_api_key}") 

serper_api_key=os.getenv("SERPER_API_KEY")
print(f"Serper API Key: {serper_api_key}...")  # Print only the first 4 characters for security


# ── One-time init (cached across Streamlit reruns) ────────────────────────
@st.cache_resource
def init():
    print("Initializing LangGraph...")
    from agent.graph import build_graph
    return build_graph()

graph = init()

# ── Page ──────────────────────────────────────────────────────────────────
st.title("Document Intelligence Agent")
st.caption("LangGraph · LangSmith · Groq · Gemini · Google Serper")



# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Session")
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    st.code(st.session_state.session_id)
    print(f"Session ID: {st.session_state.session_id}")
    
    st.divider()
    st.subheader("Agent pipeline")
    st.markdown(
        "1. **Planner** — refines your question  \n"
        "2. **Document Reader** — searches local guide  \n"
        "3. **Web Enricher** — Google Serper live search  \n"
        "4. **Synthesizer** — combines sources (Groq)  \n"
        "5. **Report Writer** — formats report (Gemini)"
    )

    st.divider()
    st.subheader("Try these")
    st.markdown(
        "_What are the biggest LLM security risks?_  \n"
        "_How does RAG reduce hallucinations?_  \n"
        "_What is LLM-as-Judge evaluation?_  \n"
        "_Best practices for deploying LLM agents?_"
    )

    st.divider()
    st.link_button("View LangSmith traces →", "https://smith.langchain.com")
    
    
# ── Chat history ──────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("meta"):
            with st.expander("Pipeline details"):
                st.json(msg["meta"])
                
                
# ── Input ─────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask anything about LLM production..."):
    print(f"User prompt: {prompt}")
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Running pipeline (traced in LangSmith)..."):
            result = graph.invoke({
                "question":         prompt,
                "session_id":       st.session_state.session_id,
                "refined_question": "",
                "doc_sections":     [],
                "web_results":      "",
                "synthesis":        "",
                "final_report":     "",
                "steps_taken":      [],
            })

        st.markdown(result["final_report"])

        meta = {
            "refined_question": result["refined_question"],
            "pipeline":         " → ".join(result["steps_taken"]),
            "doc_sections_found": len(result["doc_sections"]),
            "session_id":       result["session_id"],
        }
        with st.expander("Pipeline details"):
            st.json(meta)

    st.session_state.messages.append({
        "role":    "assistant",
        "content": result["final_report"],
        "meta":    meta,
    })
