# ### 
# A single Agent can only say create a short story for us.
# but with a team whre many agents work together towards a common goal they can help us in writing or even helping to review, edit etc.

import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from dotenv import load_dotenv
from autogen_agentchat.ui import Console
import os
import asyncio


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
##Initialize the model client using a specific model

model_client = OpenAIChatCompletionClient(model='gpt-4o', api_key=api_key)
model_client_2 = OpenAIChatCompletionClient(model='gpt-4',api_key=api_key)

from autogen_agentchat.agents import AssistantAgent

##Initialize and configure the agent.

dsa_solver = AssistantAgent(
    name = 'Complex_DSA_Solver',
    model_client=model_client,
    description='A DSA solver',
    system_message="You give code in python to solve complex DSA problems. Give under 100 words"
)

code_reviewer = AssistantAgent(
    name = 'CODE_REVEIWER',
    model_client=model_client_2,
    description='A Code Reviewer',
    system_message="You review the code given by the complex_dsa_solver and make sure it is optimized.Give under 10 words"
)

code_editor = AssistantAgent(
    name = 'CODE_EDITOR',
    model_client=model_client,
    description='A Code editor',
    system_message="You make the code easy to understand and add comments wherever required.Give under 10 words"
)

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage

## Round Robin
team = RoundRobinGroupChat(
    participants=[dsa_solver,code_reviewer,code_editor],
    max_turns=15 # -----># maximum number of Message before it stops between the agents.
)

print("Round Robin Agent (START)")

## Test the TEAM agent.

async def test_team():
    task = TextMessage(content='Write a simple program Hello World using python ?',source='User')
    print("Round Robin Agent (TEST THE TEAM)")
    result = await team.run(task=task)

    for each_agent_message in result.messages:
        print(f'{((each_agent_message))} ' )
        print('\n \n')


## await test_team()

from autogen_agentchat.base import TaskResult
async def test_team2():
    print("CALLING FROM TEST_TEAM2\n")
    await team.reset()  # Reset the team for a new task.
    async for message in team.run_stream(task="Write a simple Hello world code ?"):  # type: ignore
        if isinstance(message, TaskResult):
            print("Stop Reason:", message.stop_reason)
        else:
            print(message.source,message)


from autogen_agentchat.ui import Console
async def test_team3():
    print("CALLING FROM TEST_TEAM2\n")
    await team.reset()  # Reset the team for a new task.
    await Console(team.run_stream(task="Write a simple Hello world code."))  # Stream the messages to the console.
    await Console(team.run_stream(task="continue."))


from autogen_agentchat.agents import AssistantAgent
add_1_agent_first = AssistantAgent(
    name = 'add_1_agent_first',
    model_client=model_client,
    system_message="Add 1 to the number, first number is 0. Give result as output"
)

add_1_agent_second = AssistantAgent(
    name = 'add_1_agent_second',
    model_client=model_client,
    system_message="Add 1 to the number you got from previous run. Give result as output."
)
 
add_1_agent_third = AssistantAgent(
    name = 'add_1_agent_third',
    model_client=model_client,
    system_message="Add 1 to the number from previous run. Give result as output."
)

add_1_agent_third = AssistantAgent(
    name = 'add_1_agent_third',
    model_client=model_client,
    system_message="Add 1 to the number from previous run. Give result as output."
)


agent_cricket_info = AssistantAgent(
    name = 'agent_cricket_info',
    model_client=model_client,
    description="A helpful assistant that provide cricket stats.",
    system_message="Provide incremental information and stats about Virat Kohli and Give results in 100 words."
)


agent_Medicine_info = AssistantAgent(
    name = 'agent_Medicine_info',
    model_client=model_client,
    description="A helpful assistant that provides information about medicine.",
    system_message="Provide incremental information about Aravst 5 mg uses and side effects,and Give results in 100 words.."
)

agent_news_info = AssistantAgent(
    name = 'agent_news_info',
    model_client=model_client,
    description="A helpful assistant that reads top 3 news.",
    system_message="Provide me top 5 NEWS from BBC and Give results in 50 words."
)

agent_extra_news = AssistantAgent(
    name = 'agent_extra_news',
    model_client=model_client,
    description="A helpful assistant that reads more news of a newspaper.",
    system_message="From previous RUN for news fetch more news from Times of India newspaper Give results in 50 words."
)

my_increment_team = RoundRobinGroupChat(participants=[add_1_agent_first,add_1_agent_second,add_1_agent_third],max_turns=6)
my_increment_team2 = RoundRobinGroupChat(participants=[agent_cricket_info,agent_Medicine_info,agent_news_info,agent_extra_news],max_turns=6)

# ##Resume a team
async def test_team3():
    print("CALLING FROM TEST TEAM #3 (round Robin) \n")
    print("================\n")
    await Console(my_increment_team.run_stream())
    print("my_increment_team : Run Stream Attempt 1\n")
    await Console(my_increment_team.run_stream())
    print("my_increment_team : Run Stream Attempt 2\n")    
    await team.reset()
    await Console(my_increment_team.run_stream())
    print("my_increment_team : Run Stream Attempt 3\n")
    await my_increment_team.reset()
    print("my_increment_team : Run Stream Attempt 4\n")
    await Console(my_increment_team.run_stream())
    print("================\n")
    print("my_increment_team : COMPLETED\n")

# ##Resume a team
async def test_team4():
    print("CALLING SMART AGENTS TEAM #4 (round Robin) \n")
    print("================\n")
    await Console(my_increment_team2.run_stream())
    print("my_increment_team2 : Run Stream Attempt 1\n")
    await Console(my_increment_team2.run_stream())
    print("my_increment_team2 : Run Stream Attempt 2\n")    
    await team.reset()
    await Console(my_increment_team2.run_stream())
    print("my_increment_team2 : Run Stream Attempt 3\n")
    await my_increment_team2.reset()
    print("my_increment_team2 : Run Stream Attempt 4\n")
    await Console(my_increment_team2.run_stream())
    print("================\n")
    print("my_increment_team2 :SMART AGENTS TEAM #4 : COMPLETED\n")

#Execute the request using the model
##Call from the Main Function.
async def main():
    print("STARTED FROM THE MAIN FUNCTION\n")
    await test_team()
    print("================\n")
    await test_team2()
    print("================\n")
    await test_team3()
    print("================\n")
    await test_team4()
    print("================\n")
    print("COMPLETED FROM THE MAIN FUNCTION\n")
    


#Execute the request using the model
asyncio.run(main())   

