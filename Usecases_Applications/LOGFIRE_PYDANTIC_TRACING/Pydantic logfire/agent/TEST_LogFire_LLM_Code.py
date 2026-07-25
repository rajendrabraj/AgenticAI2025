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

logfire.info("notebook_started",
            part="PART 1 - BASICS",
            instructer = "Rajendra",
            tool = "Pydantic Logfire"
            )


from pydantic import BaseModel
from typing import Optional

# MOCK DATA nOT REAL DATA

class LLMRequest(BaseModel):
    user_id: str
    session_id: str
    query: str
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None


class LLMResponse(BaseModel):
    answer: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    model_used: str    


# ── Simulate logging a real LLM request/response ──────────────────────────
request = LLMRequest(
    user_id="priya",
    session_id="sess_abc123",
    query="What is Retrieval-Augmented Generation?",
    model="llama-3.3-70b-versatile",
    max_tokens=500
)

with logfire.span("llm_CALL",
                  user_id = request.user_id,
                  session_id = request.session_id,
                  model_used = request.model):
    logfire.info("request_received" , **request.model_dump())
    
    time.sleep(0.1)

    response = LLMResponse(
        answer="RAG is a technique that retrieves relevant documents...",
        input_tokens=18,
        output_tokens=120,
        latency_ms=342.5,
        model_used="llama-3.3-70b-versatile"
    )
    logfire.info("response_sent", **response.model_dump())


print(response)
