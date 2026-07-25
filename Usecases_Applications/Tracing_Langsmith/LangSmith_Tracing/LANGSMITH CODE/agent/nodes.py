"""
Sequential Document Intelligence Agent — nodes.
All LangChain / LangGraph calls are auto-traced to LangSmith via env vars.
No explicit tracing code needed in these nodes.
"""
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.utilities import GoogleSerperAPIWrapper
import os
from dotenv import load_dotenv, find_dotenv

if __package__ in {None, ""}:
    from state import AgentState
    from tools import search_document
else:
    from .state import AgentState
    from .tools import search_document


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Now you can access environment variables
print(f"Path to .env file: {dotenv_path}")

openai_api_key = os.getenv("OPENAI_API_KEY", "")
print(f"OpenAI API Key: {openai_api_key[:4]}...")  # Print only the first 4 characters for security 

serper_api_key = os.getenv("SERPER_API_KEY", "")
print(f"Example variable SERPER_API_KEY : {serper_api_key}") 

print("loading env variables from .env file completed successfully. ")



# ── LLM clients ──────────────────────────────────────────────────────────
_groq = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
)

_gemini = ChatOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-2.5-flash-lite",
    temperature=0.3,
)

print(f"Initialize the Google Serper API wrapper with key: {serper_api_key[:20]}...")

_serper = GoogleSerperAPIWrapper(api_key=serper_api_key)

# ── Nodes ─────────────────────────────────────────────────────────────────

def planner(state: AgentState) -> dict:
    print("Planner node: refining the user question...\n")
    
    """Rewrites the user question for clarity and precision."""
    response = _groq.invoke([
        SystemMessage(content=(
            "You are a research question refiner. "
            "Rewrite the user question to be more specific and searchable. "
            "Return ONLY the rewritten question, nothing else."
        )),
        HumanMessage(content=state["question"]),
    ])
    return {
        "refined_question": response.content.strip(),
        "steps_taken": state.get("steps_taken", []) + ["planner"],
    }


def document_reader(state: AgentState) -> dict:
    print("Document Reader node: searching local knowledge-base...\n")
    
    """Searches the local knowledge-base document for relevant sections."""
    sections = search_document(state["refined_question"], top_k=3)
    return {
        "doc_sections": sections,
        "steps_taken": state.get("steps_taken", []) + ["document_reader"],
    }


def web_enricher(state: AgentState) -> dict:
    print("Web Enricher node: fetching latest information from the web...\n")
    
    """Fetches the latest information from the web using Google Serper."""
    try:
        web_text = _serper.run(state["refined_question"])
    except Exception as exc:
        web_text = f"[Web search unavailable: {exc}]"
    return {
        "web_results": web_text,
        "steps_taken": state.get("steps_taken", []) + ["web_enricher"],
    }


def synthesizer(state: AgentState) -> dict:
    print("Synthesizer node: combining document and web knowledge...\n")
    """Combines document knowledge and web results into a coherent analysis."""
    doc_context = "\n\n---\n\n".join(state["doc_sections"])
    synthesis = _groq.invoke([
        SystemMessage(content=(
            "You are a research synthesizer. Given knowledge from a document and "
            "from the web, combine both into a clear, structured analysis. "
            "Cite sources where possible. Use markdown formatting."
        )),
        HumanMessage(content=(
            f"Question: {state['refined_question']}\n\n"
            f"=== DOCUMENT KNOWLEDGE ===\n{doc_context}\n\n"
            f"=== WEB SEARCH RESULTS ===\n{state['web_results']}"
        )),
    ])
    return {
        "synthesis": synthesis.content,
        "steps_taken": state.get("steps_taken", []) + ["synthesizer"],
    }


def report_writer(state: AgentState) -> dict:
    print("Report Writer node: formatting the final report...\n")
    """Formats the synthesis into a polished final report using Gemini."""
    try:
        report = _gemini.invoke([
            SystemMessage(content=(
                "You are a technical report writer. Format the given analysis into "
                "a clean, well-structured report with: a one-sentence TL;DR at the top, "
                "key findings as bullet points, and a brief conclusion. "
                "Keep it under 400 words."
            )),
            HumanMessage(content=state["synthesis"]),
        ])
        final = report.content
    except Exception:
        # Fallback to raw synthesis if Gemini is unavailable
        final = state["synthesis"]

    return {
        "final_report": final,
        "steps_taken": state.get("steps_taken", []) + ["report_writer"],
    }
