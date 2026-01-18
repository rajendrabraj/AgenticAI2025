import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.conditions import TextMentionTermination
from autogen import UserProxyAgent,AssistantAgent,GroupChat,GroupChatManager
import autogen
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Load LLM credentials from .env (like OPENAI_API_KEY) needed for all the agents
llm_config = {
"config_list": autogen.config_list_from_dotenv(),
"temperature": 0.5,
}


# === USER-FACING AGENT ===
user_proxy = UserProxyAgent(
    name="UserProxy",
    max_consecutive_auto_reply=8,
    human_input_mode="ALWAYS",
    code_execution_config=False
)

# === OUTER TEAM MANAGER ===
outer_manager = AssistantAgent(
    name="OuterManager",
    human_input_mode="ALWAYS",  # disables manual human input
    system_message="You are the coordinator. Gather opinions from all agents and synthesize a cohesive response.",
    llm_config=llm_config,

)

# === INNER TEAM COORDINATORS ===
backend_coordinator = AssistantAgent(
    name="BackendCoordinator",
    human_input_mode="ALWAYS",  # disables manual human input
    system_message="You are a backend coordinator responsible for managing backend tasks and workers.",
    llm_config=llm_config,
)


frontend_coordinator = AssistantAgent(
    name="FrontendCoordinator",                                      
    human_input_mode="NEVER",  # disables manual human input
    system_message="You are a frontend coordinator responsible for managing frontend tasks and workers.",
    llm_config=llm_config,

)
data_coordinator = AssistantAgent(
    name="DataCoordinator",
    human_input_mode="NEVER",  # disables manual human input
    system_message="You are a data coordinator responsible for managing data tasks and workers.",
    llm_config=llm_config,
    )

# === INNER TEAM WORKERS ===
backend_worker_1 = AssistantAgent(
    name="BackendWorker1",
    human_input_mode="ALWAYS",  # disables manual human input
    system_message="You are a backend worker responsible for implementing backend logic for input or query recieved",
    llm_config=llm_config,
    )
backend_worker_2 = AssistantAgent(
    name="BackendWorker2",
    human_input_mode="ALWAYS",  # disables manual human input
    system_message="You are a backend worker responsible for implementing backend logic for input or query received",
    llm_config=llm_config,
    )
frontend_worker = AssistantAgent(
    name="FrontendWorker",
    human_input_mode="ALWAYS",  # disables manual human input
    system_message="You are a Front end worker to implemented the frontend tasks.",
    llm_config=llm_config,
    )
data_worker = AssistantAgent(
    name="DataWorker",
    human_input_mode="ALWAYS",  # disables manual human input
    system_message="You are a data coordinator responsible for managing data tasks and workers.",
    llm_config=llm_config,
    )

# === BACKEND GROUP CHAT ===
backend_groupchat = GroupChat(
    agents=[backend_coordinator, backend_worker_1, backend_worker_2],
    messages=[],
    max_round=8,
)
backend_chat_manager = GroupChatManager(
    groupchat=backend_groupchat,
    name="BackendGroupManager",llm_config=llm_config
)

# === FRONTEND GROUP CHAT ===
frontend_groupchat = GroupChat(
    agents=[frontend_coordinator, frontend_worker],
    messages=[],
    max_round=8,
)
frontend_chat_manager = GroupChatManager(
    groupchat=frontend_groupchat,
    name="FrontendGroupManager",
    llm_config=llm_config
)

# === DATA TEAM GROUP CHAT ===
data_groupchat = GroupChat(
    agents=[data_coordinator, data_worker],
    messages=[],
    max_round=8,
)
data_chat_manager = GroupChatManager(
    groupchat=data_groupchat,
    name="DataGroupManager",
    llm_config=llm_config
)

# === OUTER TEAM CHAT ===
outer_groupchat = GroupChat(
    agents=[
        outer_manager,
        backend_chat_manager,
        frontend_chat_manager,
        data_chat_manager
    ],
    messages=[],
    max_round=8,
)
outer_chat_manager = GroupChatManager(
    groupchat=outer_groupchat,
    name="OuterGroupManager", llm_config=llm_config
)

# === RUN INTERACTION ===
def execute_multiple_agents():
    user_goal = (
        "Build a simple web application using streamlit where users can submit feedback. "
        "Backend should store data, frontend should be responsive, and include basic analytics."
    )

    chat_result=user_proxy.initiate_chat(outer_chat_manager, message=user_goal)
    print("=================\n")
    print(chat_result.summary)
    print("=================\n")


# === START ===
if __name__ == "__main__":
    execute_multiple_agents()
