from dotenv import load_dotenv
load_dotenv()

import os
pinecone_api_key=os.getenv("PINECONE_API_KEY")


from dotenv import load_dotenv, find_dotenv
import os

# Find the .env file, searching upwards in the directory tree
dotenv_path = find_dotenv()

# Load the .env file
load_dotenv(dotenv_path)

# Now you can access environment variables
print(f"Path to .env file: {dotenv_path}")
# print(f"Example variable PINE_CONE_API_KEY : {os.getenv('PINE_CONE_API_KEY')}") 
# print(f"Example variable TAVILY_API_KEY : {os.getenv('TAVILY_API_KEY')}") 
