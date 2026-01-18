import os
import autogen

# Configure the LLM for the AssistantAgent
# Ensure you have your OpenAI API key set as an environment variable (e.g., OPENAI_API_KEY)
llm_config = {
    "config_list": [
        {
            "model": "gpt-4",  # Or another suitable model like "gpt-3.5-turbo"
            "api_key": os.environ.get("OPENAI_API_KEY")
        }
    ]
}

# Create an AssistantAgent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="You are a helpful AI assistant. You can generate code and answer questions."
)

# Create a UserProxyAgent
# This agent acts as a proxy for the human user and can execute code.
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # Set to "ALWAYS" or "TERMINATE" for human interaction
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",  # Directory for code execution
        "use_docker": False,   # Set to True to use Docker for isolated execution
    },
)

# Initiate a chat between the UserProxyAgent and the AssistantAgent
user_proxy.initiate_chat(
    assistant,
    message="Write a Python script to calculate the factorial of a number."
)