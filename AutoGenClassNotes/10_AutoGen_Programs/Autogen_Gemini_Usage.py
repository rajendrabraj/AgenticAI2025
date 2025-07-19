from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio

import os

from dotenv import load_dotenv
load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

#exchange_api_key = os.getenv("EXCHANGE_RATE_API")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")


model_client = OpenAIChatCompletionClient(
    model="gemini-1.5-flash-8b",
    api_key=GEMINI_API_KEY,
)

async def some_async_operation():
    response = await model_client.create([UserMessage(content="What is the capital of France?", source="user")])
    print(response)
    await model_client.close()

##Call from the Main Function.
async def main():
    await some_async_operation()

#Execute the request using the model
asyncio.run(main())


