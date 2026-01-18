import autogen
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# Load LLM credentials from .env (like OPENAI_API_KEY)
llm_config = {
"config_list": autogen.config_list_from_dotenv(),
"temperature": 0.5,
}

# Define sub-agents (minds)
memory_agent = AssistantAgent(
name="MemoryAgent",
human_input_mode="NEVER",  # disables manual human input
system_message="You are responsible for recalling relevant facts, history, and previously known information.",
llm_config=llm_config,
)

logic_agent = AssistantAgent(
name="LogicAgent",
human_input_mode="NEVER",  # disables manual human input
system_message="You are responsible for applying logical reasoning and formal analysis.",
llm_config=llm_config,
)

emotion_agent = AssistantAgent(
name="EmotionAgent",
human_input_mode="NEVER",  # disables manual human input
system_message="You are responsible for evaluating emotional context and empathic response.",
llm_config=llm_config,
)

creative_agent = AssistantAgent(
name="CreativeAgent",
human_input_mode="NEVER",  # disables manual human input
system_message="You are responsible for producing imaginative and novel ideas or metaphors.",
llm_config=llm_config,
)

# Meta-mind to orchestrate others
manager_agent = AssistantAgent(
name="ManagerAgent",
human_input_mode="NEVER",  # disables manual human input
system_message="You are the coordinator. Gather opinions from all agents and synthesize a cohesive response.",
llm_config=llm_config,
)

# User (you) as input agent
user = UserProxyAgent("User", 
                      max_consecutive_auto_reply=2,
                      code_execution_config=False
                      )

# Society of Mind: Group Chat with multiple specialized agents
groupchat = GroupChat(
agents=[
user,
manager_agent,
memory_agent,
logic_agent,
emotion_agent,
creative_agent,
],
messages=[],
max_round=2,
)

# Manager runs the dialogue and aggregates the society’s thoughts
group_manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Begin the conversation — simulate a thought prompt
chat_result = user.initiate_chat(
group_manager,
message="What does it mean to be truly intelligent? Please explain using different perspectives.",
)


# Display the summary of the conversation

print("=================\n")
print(chat_result.summary)
print("=================\n")
