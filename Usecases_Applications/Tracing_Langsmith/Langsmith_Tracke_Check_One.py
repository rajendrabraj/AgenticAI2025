import os
from openai import OpenAI
from langsmith import traceable

from dotenv import load_dotenv, find_dotenv

# Find the .env file, searching upwards in the directory tree
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Now you can access environment variables
print(f"Path to .env file: {dotenv_path}")

openai_api_key = os.getenv("OPENAI_API_KEY", "")

print(f"OpenAI API Key: {openai_api_key[:4]}...")  # Print only the first 4 characters for security 
langsmith_api_key = os.getenv("LANGSMITH_API_KEY", "")      
print(f"LangSmith API Key: {langsmith_api_key[:4]}...")  # Print only the first 4 characters for security


# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@traceable(name="simple_chat")
def ask_llm(query: str) -> str:
    """This function will automatically appear as a LangSmith trace."""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # or any OpenAI model you have access to
        messages=[
            {"role": "user", "content": query}
        ],
    )

    return response.choices[0].message.content


def main():
    while True:
        query = input("\nYou: ")

        if query.lower() in {"exit", "quit"}:
            break

        answer = ask_llm(query)
        print(f"\nAssistant: {answer}")


if __name__ == "__main__":
    main()