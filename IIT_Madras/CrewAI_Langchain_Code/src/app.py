## Rajendra Bichu : Date : 29.04.2026 , Version 1.0

## Customer Support — AI Support Resolution Agent
## This script builds a CrewAI workflow for customer support.
## It classifies intent, checks safety, retrieves knowledge, generates a response,
## escalates unresolved or sensitive cases, and logs decisions safely.

## This program is to test using the FAST_API and execution calls.


from fastapi import FastAPI
import uvicorn
import os
import sys
import logging
import warnings
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from fastapi import FastAPI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from fastapi import FastAPI, HTTPException

# Ensure the parent src folder is importable when this file is executed from elsewhere.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from cust_agent_app import get_support_crew, get_evaluation_crew, execute_deployment_tracking
from loguru import logger
import pinecone
import time
import traceback


app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working"}


@app.post("/support")
def support_endpoint(request: dict):
    query = request.get("query")
    logging.info("START- Running #10 End point /support called with query: " + str(query))
    if not query:
        raise HTTPException(status_code=400, detail="Query missing")

    return execute_deployment_tracking(query)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)