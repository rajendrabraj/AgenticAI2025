import uuid

import streamlit as st
from dotenv import load_dotenv

from dotenv import load_dotenv, find_dotenv
import os



def load_environment() -> None:
        # Find the .env file, searching upwards in the directory tree
    dotenv_path = find_dotenv()
    # Load the .env file
    load_dotenv(dotenv_path)



@st.cache_resource
def init():
    from agent.tracing import setup_tracing
    from agent.graph import build_graph

    setup_tracing()
    return build_graph()


def main() -> None:
    load_environment()
    graph = init()

    st.title("Multi-Specialist AI Agent")
    st.caption("LangGraph · Logfire · Groq · Gemini · Tavily")

    with st.sidebar:
        st.header("Session")
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())[:8]
        st.code(st.session_state.session_id)

        st.divider()
        st.subheader("Routing map")
        st.markdown(
            "**explain** → 🎓 Explainer  \n"
            "**analyze** → 🔍 Analyst  \n"
            "**create**  → ✨ Creator  \n"
            "**search**  → 🌐 Web Search"
        )

        st.divider()
        st.subheader("Try these")
        st.markdown(
            "_What is the attention mechanism?_  \n"
            "_Compare RAG vs fine-tuning_  \n"
            "_Give me 5 ideas for an LLM security blog_  \n"
            "_Latest news on OpenAI GPT-5_"
        )

        st.divider()
        st.link_button("View Logfire traces →", "https://logfire.pydantic.dev")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("meta"):
                with st.expander("Trace details"):
                    st.json(msg["meta"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Routing and thinking..."):
                result = graph.invoke({
                    "question": prompt,
                    "session_id": st.session_state.session_id,
                    "intent": "",
                    "specialist_output": "",
                    "search_results": "",
                    "final_answer": "",
                    "model_used": "",
                    "node_path": [],
                })

            st.markdown(result["final_answer"])

            meta = {
                "intent": result["intent"],
                "path": " → ".join(result["node_path"]),
                "model_used": result["model_used"],
                "session_id": result["session_id"],
            }

            with st.expander("Trace details"):
                st.json(meta)

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["final_answer"],
            "meta": meta,
        })


if __name__ == "__main__":
    main()
