# import os
# import logging
# from unittest import result
# from urllib import response
# import warnings
# from dotenv import load_dotenv
# from crewai import Agent, Task, Crew
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# from langchain.memory import ConversationBufferMemory

# from langchain.tools import tool


# ##Define the Memory  add the memory functions 
# ### Add the memory Setup 

# short_term_memory = ConversationBufferMemory(
# memory_key="chat_history",
# return_messages=True
# )

# long_term_memory = []


# def save_to_long_term_memory(query, response):
#     long_term_memory.append({
#     "query": query,
#     "response": response
# })


# ## Define the long term context 

# def get_long_term_context():
#     history = " " 
#     for item in long_term_memory[-5:]:
#         history += "User: " + item["query"] + "\n"
#         history += "AI: " + item["response"] + "\n"
#     return history


# ## Reset of the memory

# def reset_memory():
#    short_term_memory.clear()
#    long_term_memory.clear()



# ## Defining the : Multi Turn Conversation functions and Memory


# ##Define Memory and save the Conversational History

# def run_conversation(query):
#    memory_context = get_long_term_context()

# ##support_crew_Evaluation.kickoff(inputs={"query": query})


#     result_memory_check = support_crew_Evaluation.kickoff(inputs={
#         "query": query,
#         "memory": memory_context
#     })

#     short_term_memory.save_context(
#         {"input": query},
#         {"output": str(result)}
#     )
#     )

#     save_to_long_term_memory(query, str(result_memory_check))

#     return result_memory_check


