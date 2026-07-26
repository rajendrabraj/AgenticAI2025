## July 2026
## This program will fire the queries against the models and output can be seen in the logfire dashboard.


from dotenv import load_dotenv
load_dotenv()

import os
import time 


from dotenv import load_dotenv, find_dotenv
import os

# Find the .env file, searching upwards in the directory tree
dotenv_path = find_dotenv()

# Load the .env file
load_dotenv(dotenv_path)

# Now you can access environment variables
print(f"Path to .env file: {dotenv_path}")


openai_api_key = os.getenv("OPENAI_API_KEY", "")
pinecone_api_key=os.getenv("PINECONE_API_KEY")
serper_api_key=os.getenv("SERPER_API_KEY")

logfire_token=os.getenv("LOGFIRE_TOKEN")




print(f"Example variable PINE_CONE_API_KEY : {os.getenv('PINE_CONE_API_KEY')}") 
##print(f"Example variable TAVILY_API_KEY : {os.getenv('TAVILY_API_KEY')}") 
# Now you can access environment variables
print(f"Path to .env file: {dotenv_path}")
print(f"Example variable PINE_CONE_API_KEY : {os.getenv('PINE_CONE_API_KEY')}") 
print(f"Example variable TAVILY_API_KEY : {os.getenv('TAVILY_API_KEY')}") 
print(f"Example variable SERPER_API_KEY : {os.getenv('SERPER_API_KEY')}") 



print(f"OpenAI API Key: {openai_api_key[:4]}...")  # Print only the first 4 characters for security 
langsmith_api_key = os.getenv("LANGSMITH_API_KEY", "")      
print(f"LangSmith API Key: {langsmith_api_key[:4]}...")  # Print only the first 4 characters for security

serper_api_key=os.getenv("SERPER_API_KEY")
print(f"Serper API Key: {serper_api_key[:10]}...")  # Print only the first 4 characters for security


logfire_token=os.getenv("LOGFIRE_TOKEN")
print(f"Logfire Token: {logfire_token[:10]}...")  # Print only the first 4 characters for security

gemini_api_key=os.getenv("GEMINI_API_KEY")
print(f"Gemini API Key: {gemini_api_key[:10]}...")  # Print only the first 4 characters for security

gemini_api_key=os.getenv("GEMINI_API_KEY")
print(f"Gemini API Key: {gemini_api_key[:10]}...")  # Print only the first 4 characters for security

groq_api_key=os.getenv("GROQ_API_KEY")
print(f"GROQ API Key: {groq_api_key[:10]}...")  # Print only the first 4 characters for security


import logfire

logfire.configure()
logfire.info('Hello, {place}!', place='UDEMY')

logfire.configure(
    token=os.getenv("LOGFIRE_TOKEN"),
    service_name="llm-observability-course"
)

# logfire.info("notebook_started",
#             part="PART 1 - BASICS",
#             instructer = "Rajendra",
#             tool = "Pydantic Logfire"
#             )


from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


logfire.instrument_openai()

llm_groq = ChatOpenAI(
    base_url= "https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    model = "llama-3.3-70b-versatile",
    temperature=0.3
)

# Make a call — watch the trace appear in the dashboard automatically
print("Calling Groq (llama-3.3-70b)…")
response = llm_groq.invoke([
    HumanMessage(content="Explain what an observability 'span' is, in exactly 2 sentences.")
])

print(response.content)


# Gemini's OpenAI-compatible endpoint (no extra setup needed)
llm_gemini = ChatOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini-2.0-flash",
    temperature=0.3
)


print("Calling Gemini (gemini-2.0-flash)…")
try:
    response = llm_gemini.invoke([
        HumanMessage(content="Explain what an observability 'trace' is, in exactly 2 sentences.")
    ])
    print(f"\n🔵 Gemini Response:\n{response.content}")
except Exception as e:
    print(f"⚠️  Gemini call failed: {e}")
    print("    Check your GEMINI_API_KEY in .env")


## Groq Model

query = "What is the difference between RAG and fine-tuning? Give 3 bullet points."

# with logfire.span("model_comparison", query=query, num_models=2):

#     # ── Groq ─────────────────────────────────────────────────────────────
#     with logfire.span("groq_call", model="llama-3.3-70b-versatile", provider="groq"):
#         t0 = time.time()
#         r_groq = llm_groq.invoke([HumanMessage(content=query)])
#         groq_ms = round((time.time() - t0) * 1000, 1)
#         logfire.info("groq_done", latency_ms=groq_ms, answer_len=len(r_groq.content))

# ── Gemini ────────────────────────────────────────────────────────────
with logfire.span("gemini_call", model="gemini-2.5-flash-lite", provider="google"):
    t0 = time.time()
    try:
        r_gemini = llm_gemini.invoke([HumanMessage(content=query)])
        gemini_ms = round((time.time() - t0) * 1000, 1)
        logfire.info("gemini_done", latency_ms=gemini_ms, answer_len=len(r_gemini.content))
        gemini_answer = r_gemini.content
    except Exception as e:
        logfire.warning("gemini_failed", error=str(e))
        gemini_ms = 0
        gemini_answer = f"[Error: {e}]"

# # ── Print results ─────────────────────────────────────────────────────────
# print(f"🟢 Groq ({groq_ms}ms):\n{r_groq.content}")


print(f"\n🔵 Gemini ({gemini_ms}ms):\n{gemini_answer}")
