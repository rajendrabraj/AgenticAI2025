##Assigment #1 using Autogen which uses multiple agents
## This program also uses UserProxy Agent
## This will also ask input from users 


import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent,UserProxyAgent,SocietyOfMindAgent

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os

##Load the environment variables

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
model_client = OpenAIChatCompletionClient(model='gpt-4o')

##First Agent will be Cricket Agent


assistant1 = AssistantAgent(
    name='CricketAgent',
    description='You are a Cricket Agent who writes about cricket',
    model_client=model_client,
    system_message='Please provide information about Indian Cricket Teams in less than 50 words'
)


# Second Agent will be Tennis Agent

assistant2 = AssistantAgent(
    name='TennisAgent',
    description='You are a Tennis Agent who writes about tennis',
    model_client=model_client,
    system_message='Please provide information about Grand Slams latest in less than 50 words.'
)

# Third Agent will be Stocks News Editor

assistant3 = AssistantAgent(
    name='StocksNewsEditor',
    description='You are a Stocks News Editor who writes about stock market',
    model_client=model_client,
    system_message='You read the latest Indian stock markets news who writes in less than 50 words..'
)

# User Proxy Agent to take input from user

user_proxy_agent = UserProxyAgent(
    name ='UserProxy',
    description='you are a user proxy agent',
    input_func=input
)

termination_condition = TextMentionTermination(text='APPROVE')

# team = RoundRobinGroupChat(
#     participants=[user_proxy_agent,assistant1, assistant2, assistant3,],
#     termination_condition=termination_condition,
#     max_turns=1
# )

## Use the Society of Mind Agent to manage the inner team



async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4o",api_key=api_key)

    agent1 = AssistantAgent("assistant1", model_client=model_client, system_message="You are a writer, write well under 100 words.")
    agent2 = AssistantAgent(
        "assistant2",
        model_client=model_client,
        system_message="You are an writer, provide critical feedback under 100 words. Respond with 'APPROVE' if the text addresses all feedbacks.",
    )
    inner_termination = TextMentionTermination("APPROVE")
    # Inner Team has 2 agents and proxy agent
    
    inner_team = RoundRobinGroupChat([user_proxy_agent,agent1, agent2], termination_condition=inner_termination)


    society_of_mind_agent = SocietyOfMindAgent("society_of_mind", team=inner_team, model_client=model_client,response_prompt='Output a standalone response to the original request under 50 words, without mentioning any of the intermediate discussion.')

    agent4 = society_of_mind_agent = SocietyOfMindAgent("society_of_mind", team=inner_team, model_client=model_client,response_prompt='Output a standalone response to the original request under 50 words, without mentioning any of the intermediate discussion.')

    agent3 = AssistantAgent(
        "assistant3", model_client=model_client, system_message="Translate the text to Spanish under 50 words."
    )
    team = RoundRobinGroupChat([society_of_mind_agent, agent3], max_turns=2)

    stream = team.run_stream(task="You are agent who provides information under 50 words.")
    await Console(stream)


## Run this finally

asyncio.run(main())