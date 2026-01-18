import os
from dotenv import load_dotenv
import os
from autogen import ConversableAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

##Load the environment variables

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
# Model client
model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)

# 1. Define LLM Configuration
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",           # or "gpt-4o", "gpt-3.5-turbo", etc.
            "api_key": os.environ["OPENAI_API_KEY"],
        }
    ],
    "temperature": 0.5,               # creativity level
    "max_tokens": 2048,               # response length
    "seed": 42                        # for reproducibility
}



student_agent = ConversableAgent(
    name="Student_Agent",
    system_message="You are a student willing to learn.",
    llm_config=llm_config,
)
teacher_agent = ConversableAgent(
    name="Teacher_Agent",
    system_message="You are a data science teacher.",
    llm_config=llm_config,
)

chat_result = student_agent.initiate_chat(
    teacher_agent,
    message="Explain more about crewai and use cases?",
    summary_method="reflection_with_llm",
    max_turns=2,
)

print(chat_result.summary)