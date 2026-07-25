## Rajendra Bichu , Load BAsic settings, Load env Variables and set folder paths



## Import necessary libraries and modules 


import os
import logging
import warnings
from dotenv import load_dotenv
#from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import tool


load_dotenv()
warnings.filterwarnings("ignore")

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
parent_directory = os.path.abspath(os.path.join(script_dir, os.pardir))

print("=" * 80)
set_data_path = os.path.join(parent_directory, "Cash_Flow_Prediction\data")
os.makedirs(set_data_path, exist_ok=True)
logs_directory_path = os.path.join(parent_directory, "Cash_Flow_Prediction\logs")
os.makedirs(logs_directory_path, exist_ok=True)

print("=" * 80)

print(f"Data directory path: {set_data_path}")
print(f"Logs directory path: {logs_directory_path}")

print("=" * 80)

# pinecone_api_key = os.getenv("PINECONE_API_KEY", "")
# print(f"Example variable PINECONE_API_KEY : {pinecone_api_key}")


## Enable logging to a file with INFO level and a specific format


logging.basicConfig(
    filename=os.path.join(logs_directory_path, "Cash_Flow_Logging.log"),
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
    force=True
)

import logging
logging.info("Logging is configured and working")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

embeddings = OpenAIEmbeddings()
