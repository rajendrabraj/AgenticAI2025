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
