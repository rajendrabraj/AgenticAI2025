##Assigment #1 using Autogen which uses multiple agents
## This program also uses UserProxy Agent
## This will also ask input from users 


import asyncio
from codecs import StreamReader
from autogen_agentchat.agents import AssistantAgent,UserProxyAgent

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
    system_message='Please provide information about Indian Cricket Teams in less than 100 words'
)


# Second Agent will be Tennis Agent

assistant2 = AssistantAgent(
    name='TennisAgent',
    description='You are a Tennis Agent who writes about tennis',
    model_client=model_client,
    system_message='Please provide information about Grand Slams latest in less than 100 words.'
)

# Third Agent will be Stocks News Editor

assistant3 = AssistantAgent(
    name='StocksNewsEditor',
    description='You are a Stocks News Editor who writes about stock market',
    model_client=model_client,
    system_message='You read the latest Indian stock markets news who writes in less than 30 words..'
)

# User Proxy Agent to take input from user

user_proxy_agent = UserProxyAgent(
    name ='UserProxy',
    description='you are a user proxy agent',
    input_func=input
)

termination_condition = TextMentionTermination(text='APPROVE')

team = RoundRobinGroupChat(
    participants=[assistant1, assistant2, assistant3,user_proxy_agent],
    termination_condition=termination_condition,
    max_turns=1
)


async def main():
    task = 'You are agent who provides information'

    while True:
        stream = team.run_stream(task=task)
        
        await Console(stream)

        feedback_from_user_or_application=input('Please choose what you want to do : EXIT , MORE , OVERRIDE')

        if(feedback_from_user_or_application.lower().strip()=='exit'):
            break

        if(feedback_from_user_or_application.lower().strip()=='more'):
            task= "Please give me more information and execute the task again"            
            continue
        if(feedback_from_user_or_application.lower().strip()=='override'):
            task= "Please Override the information and re-execute the task again"            
            continue

#        task = feedback_from_user_or_application

    
if (__name__ == '__main__'):
    asyncio.run(main())