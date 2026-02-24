from groq import Groq
import os

# Set your API key as environment variable:
# export GROQ_API_KEY="your_api_key_here"

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

completion = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about artificial intelligence."}
    ],
    temperature=0.7,
    max_tokens=200,
)

print(completion.choices[0].message.content)