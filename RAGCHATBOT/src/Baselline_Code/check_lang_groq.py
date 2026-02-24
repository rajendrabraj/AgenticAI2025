from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

#Load Env Variables
import os
GROQ_API_KEY=os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="groq/compound-mini"
)

print(llm.invoke("what is Agentic AI"))
