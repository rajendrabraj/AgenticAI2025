
# from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os
import autogen
import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent,UserProxyAgent
from autogen_agentchat.agents import SocietyOfMindAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from autogen_agentchat.teams import SelectorGroupChat

##Load the environment variables

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
model_client = OpenAIChatCompletionClient(model='gpt-4o')

llm_config = {
"config_list": autogen.config_list_from_dotenv(),
"temperature": 0.5,
}


    async def main() -> None:

   
# Define sub-agents (minds)
    memory_agent = AssistantAgent(
        name="MemoryAgent",
        system_message="You are responsible for recalling relevant facts, history, and previously known information.",
        model_client=model_client,
        # is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
        )

    logic_agent = AssistantAgent(
    name="LogicAgent",
    system_message="You are responsible for applying logical reasoning and formal analysis.",
    model_client=model_client,
    # is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    )

    emotion_agent = AssistantAgent(
    name="EmotionAgent",
    system_message="You are responsible for evaluating emotional context and empathic response.",
    model_client=model_client,
    # is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    )

    creative_agent = AssistantAgent(
    name="CreativeAgent",
    system_message="You are responsible for producing imaginative ideas.",
    model_client=model_client,
    # is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    )

    # Meta-mind to orchestrate others
    manager_agent = AssistantAgent(
    name="ManagerAgent",
    system_message="You are the coordinator. Gather opinions from all agents and synthesize a cohesive response.",
    model_client=model_client,
    )

# User (you) as input agent
# user = UserProxyAgent("User", code_execution_config=False)

    # Society of Mind: Group Chat with multiple specialized agents
    groupchat = GroupChat(
        agents=[memory_agent, logic_agent],
        messages=[],
        max_round=8,
        speaker_selection_method="round_robin",  # With two agents, this is equivalent to a 1:1 conversation.
        allow_repeat_speaker=False,
    )



    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
        llm_config=llm_config,
    )




#chat_manager=manager,



# society_of_mind_agent = SocietyOfMindAgent(
#     "society_of_mind",
#     chat_manager=manager,
#     llm_config=llm_config,
# )

    inner_termination = TextMentionTermination("APPROVE")
    inner_team = RoundRobinGroupChat([memory_agent, logic_agent], termination_condition=inner_termination)




    #agent4 = society_of_mind_agent = SocietyOfMindAgent("society_of_mind", team=inner_team, model_client=model_client,response_prompt='Output a standalone response to the original request under 50 words, without mentioning any of the intermediate discussion.')

    society_of_mind_agent = SocietyOfMindAgent(
        "society_of_mind",
        team=inner_team, 
        model_client=model_client,    
        response_prompt='Collate all the previous responses and provide a final answer in 100 words\n',
        
    )
    
    team = RoundRobinGroupChat([society_of_mind_agent, creative_agent], max_turns=2)
    task_details = "what is agentic AI ? Please explain using different perspectives?"
    stream = team.run_stream(task=task_details)    
    await Console(stream)

asyncio.run(main())

# user_proxy = autogen.UserProxyAgent(
#     "user_proxy",
#     human_input_mode="NEVER",
#     code_execution_config=False,
#     default_auto_reply="TERMINATE",
#     is_termination_msg=lambda x: True,
# )

# #Initiate the chat with the society of mind agent
# print("Initiating chat with Society of Mind Agent...\n")
# print("===========================\n")
# user_proxy.initiate_chat(society_of_mind_agent, message=task)
# print("===========================\n")

