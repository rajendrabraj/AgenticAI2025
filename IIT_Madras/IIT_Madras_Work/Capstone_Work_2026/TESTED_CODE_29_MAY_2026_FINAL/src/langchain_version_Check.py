import pkg_resources
print(pkg_resources.get_distribution("langchain").version)

import langchain
print(langchain.__version__)

# from langchain.memory import ConversationBufferMemory


# # pip uninstall langchain -y
# # pip install langchain==1.2.17


# memory = ConversationBufferMemory()
# print("OK")