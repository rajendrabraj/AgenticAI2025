from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient
import asyncio

# Assuming your Ollama server is running locally on port 11434.
ollama_model_client = OllamaChatCompletionClient(model="llama3.2")

async def some_async_operation():
    response = await ollama_model_client.create([UserMessage(content="What is the capital of France?", source="user")])
    print(response)    
    await ollama_model_client.close()

##Call from the Main Function.
async def main():
    await some_async_operation()

#Execute the request using the model
asyncio.run(main())




