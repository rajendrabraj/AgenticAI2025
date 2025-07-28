##This program uses Autogen and Memory Content and MemoryMimeTypes
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.memory import ListMemory, MemoryContent, MemoryMimeType
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio

userMemory = ListMemory()
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

##Define User_Memory relate Tasks

async def configure_memory()-> None:
    await userMemory.add(    
        MemoryContent(content='The weather should be in degree celsius(metric) ',
        mime_type= MemoryMimeType.TEXT ))

    await userMemory.add(    
        MemoryContent(content='The user is vegetarian',
        mime_type= MemoryMimeType.TEXT ))




async def get_weather(city: str,units : str="imperial") -> str:
    if units == "imperial":
        return f"The weather in {city} is 73 degrees and Sunny."
    elif units == "metric":
        return f"The weather in {city} is 23 degrees and Sunny."
    else:
        return f"I don't know the weather in a particular city"
    

# Define a model client. You can use other model client that implements

assistant_agent = AssistantAgent(
    'weather_assistant',
    model_client=OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key),
    tools=[get_weather],
    memory=[userMemory]
)


# Run the agent and stream the messages to the console.
async def main() -> None:
    
    print("Printing Weather of a city\n")
    stream = assistant_agent.run_stream(task='What is the weather in Mumbai ?')
    await Console(stream)
    print("High Protein Diet\n")
    stream = assistant_agent.run_stream(task='Can you give me a good high protein diet ?')
    await Console(stream)

# NOTE: if running this inside a Python script you'll need to use asyncio.run(main()).
# await main()

asyncio.run(main())

    



                     




