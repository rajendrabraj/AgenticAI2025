# AgenticAI2025

**AI , Generative AI and Agentic Repository and Github**

---


Creation Date : 2025


**This is my GitHub repository for Agentic AI , RAG , LLM, Autogen, MCP and programs in python in order to implement the concepts in a practical world.  **

My Linkedin address ( if you want to connect )  :    https://in.linkedin.com/in/rajendrabichu

---


**🧠 Agentic AI 2.0-Introduction.**

---



**🤖 What is Agentic AI**



Agentic AI refers to a type of artificial intelligence that can make decisions, take actions, and learn autonomously without constant human oversight. It's like a virtual assistant that can think, reason, and adapt to changing circumstances. Unlike traditional AI that is often narrowly focused on specific tasks, agentic AI has a broader understanding of context and objectives, allowing it to dynamically solve problems and take action in the real world. 
In essence, agentic AI combines the flexibility of large language models (LLMs) with the structured, deterministic features of traditional programming, allowing agents to "think" and "do" in a more human-like fashion. 

**🤖 What is a AI Agent**

An AI agent is a software system that uses artificial intelligence to interact with its environment, gather information, and autonomously perform tasks to achieve specific goals set by humans. These agents can reason, plan, and make decisions based on the data they collect, and they can learn and adapt their behavior over time. 

**🤖What is Agentic RAG**


![image](https://github.com/user-attachments/assets/dc413044-ad08-481d-a0a5-692f640125d5)

**Source is google and credits to respective creators of the diagrams.

---

**🤖 What is LLM**

Large Language Models (LLMs) like GPT-4 are incredibly powerful — but they have limitations. They don’t “know” your private data, they can hallucinate, and their training data is static. That’s where Retrieval-Augmented Generation (RAG) steps in.

LLMs can’t help unless they’ve seen that document before. But with RAG, you can fetch relevant content (your own data!) and feed it to the model on-the-fly — like giving it a custom memory.

Deep learning models:
  LLMs are a specific type of deep learning model, which are neural networks that learn by analyzing large datasets to recognize complex patterns.
Transformer-based:
  Many LLMs use the transformer architecture (a type of neural network) with self-attention mechanisms. This allows the model to understand the relationships between words and phrases in a sequence of text.
Self-supervised learning:
LLMs learn by being trained on massive amounts of text, where they predict the next word or phrase in a sequence without explicit labeling. 

---


**🤖What LLMs can do**

•	Text generation: LLMs can generate human-like text, including articles, stories, poems, and even code. 

•	Translation: They can translate text from one language to another. 

•	Summarization: LLMs can condense large amounts of text into shorter summaries. 

•	Question answering: They can answer questions based on a given text or knowledge base. 

•	Code generation: LLMs can be used to assist in writing code. 

•	Other applications: LLMs are also used in areas like sentiment analysis, chatbot development, and content creation.


---
  
**🤖How RAG helps you**

•	Inject up-to-date, domain-specific knowledge

•	Avoid hallucinations from model guesswork

•	Keep models lightweight while enabling deeper knowledge 

•	RAG is the backbone of many AI-powered apps — from PDF Q&A bots and internal search tools to legal assistants and chatbots over private data.

---

**🤖RAG Architecture**

![image](https://github.com/user-attachments/assets/165196d4-3ecb-4ea2-8ee2-8276a8501d42)


**Source is google and credits to respective creators of the diagrams.

---

**🤖How goes RAG Work**

1-Query: The question in text format is sent to the RAG flow through any virtual assistant or interface.

2-(Retrieval) Document Search: The model performs a search step to collect relevant information from external sources. These sources may include a database, a set of documents, or even search engine results. The search process aims to find text fragments or documents containing information relevant to the given input or request.

3-Augmentation: The information obtained during the search phase is then combined with the original input or prompt and enriched by creating a prompt engineering draft that the model can use to create the output. The model is brought to the format expected by the large language model by including external information in this draft created through prompt engineering.

4-Generation: Finally, the model produces the answer by taking into account the received information and the original input. Here, the first form of the question posed to the system, the document obtained from the vector database and other arguments are evaluated together to ensure that the large language model produces the most accurate output text.

5-Answering: New content created by the large language model is transferred to the user.

![image](https://github.com/user-attachments/assets/6f5079d6-83e7-4452-aae2-13a62427e2ba)


**Source is google and credits to respective creators of the diagrams.


---

##  **🤖Initial Setup** 

Used VSS (**Visual Studio** with Python 3.13.2 can be downloaded for Windows from Google.

**🤖Install Packages  :**    requirements.txt - used for installing all the packages as required.
https://github.com/rajendrabraj/AgenticAI2025/blob/main/LangChainPrograms/LangChain_Assignments/requirements.txt

Streamlit used for running apps on web.  Link :   https://streamlit.io/

**Tavily** is a search engine tailored for AI agents, delivering real-time, accurate results, intelligent query suggestions, and in-depth research capabilities. https://tavily.com/ 

**Pinecone** is the leading vector database for building accurate and performant AI applications at scale in production. Link :  https://docs.pinecone.io/guides/projects/manage-api-keys

**LangChain** is a framework for developing applications powered by large language models (LLMs). LangChain simplifies every stage of the LLM application lifecycle : Link : https://python.langchain.com/docs/introduction/

---

**🤖Vector Datbaase and what is Vector database**

A vector database is a specialized type of database that stores, manages, and searches high-dimensional vector data. It's designed to handle data represented as vectors, which are numerical representations of information like text, images, or audio. These databases excel at finding similar data points based on their proximity in a multi-dimensional space, making them ideal for applications like recommendation systems, semantic search, and AI models. 

Milvus: An open-source vector database designed for handling massive-scale vector data with features like GPU acceleration and distributed querying. It is highly scalable and supports various indexing methods. Milvus is the world's most advanced open-source vector database.

Chroma: An open-source embedding database focused on simplifying LLM application development by managing, querying, and filtering vector embeddings. It is known for its intuitive API. Chroma is the open-source embedding database.

Pinecone: A fully managed, cloud-native vector database designed for high-performance, real-time AI applications. It handles scaling and infrastructure automatically. Pinecone.

Qdrant: An open-source vector database and search engine written in Rust, known for its speed and reliability. It offers an API for storing, searching, and managing vector embeddings with additional payload data. Qdrant is an Open-Source Vector Database and Vector Search Engine written in Rust.

Weaviate: A cloud-native, open-source vector database focused on speed and scalability. It supports both vector and object storage and provides a GraphQL API. Weaviate.

Faiss (Facebook AI Similarity Search): An open-source library by Meta AI for high-performance similarity search and clustering. It provides control over indexing methods and supports GPU acceleration.

---


**📝Project Structure**

It is necessary to define the folders, files, env, programs in a well defined format, hence refer to the project structure as below.


https://github.com/rajendrabraj/AgenticAI2025/blob/main/Assignment_One/Project_Struture.png


---


**📝Environmental Variables and Keys (Required)** 

PHI_API_KEY="XXXXXXXXXXXXXXXXXXXXXXX”

GROQ_API_KEY="XXXXXXXXXXXXXXXXXXXXXXX”

OPENAI_API_KEY"XXXXXXXXXXXXXXXXXXXXXXX”

folder_path= <Folder_Name>

HUGGING_FACE_TOKEN=    "XXXXXXXXXXXXXXXXXXXXXXX”

LANGCHAIN_KEY=   "XXXXXXXXXXXXXXXXXXXXXXX”

LANGCHAIN_PROJECT=   "Agentic2.0"

LANGCHAIN_TRACING_V2=   "true"

LANGCHAIN_API_KEY=    "XXXXXXXXXXXXXXXXXXXXXXX”



LANGCHAIN_TRACING_V2=   "true"

HUGGING_FACE_TOKEN=    "XXXXXXXXXXXXXXXXXXXXXXX”

LANGCHAIN_API_KEY=    "XXXXXXXXXXXXXXXXXXXXXXX”


TAVILY_API_KEY=    "XXXXXXXXXXXXXXXXXXXXXXX”

PINE_CONE_API_KEY=    "XXXXXXXXXXXXXXXXXXXXXXX”

---

**🧑‍💻Assignments Repository and KnowledgeBase**

---


##  **Assignment One** 



![image](https://github.com/user-attachments/assets/7b3fad73-e161-43c4-993a-b7646a43eb28)


Programs and assignment are here :

##   **📝Assignment One** 

These are the JSON related Programs

https://github.com/rajendrabraj/AgenticAI2025/tree/main/Assignment_One

---

##  **📝Document Loaders (Programs)**

These are the PDF and Document Parsers i.e Wikipedia , HTML based parsers , PDFParsers, Text Loaders and Text Parsers.

https://github.com/rajendrabraj/AgenticAI2025/tree/main/Document_Loaders

---

##  **📝LangChain , Langgraph Assignments  (Programs)**

https://github.com/rajendrabraj/AgenticAI2025/tree/main/LangChainPrograms/LangChain_Assignments

---

##  **🤝Know About me**

Seasoned Leader with 24+ years of experience in leading large scale digital transformation programs, technology modernization, and regulatory initiatives across
Banking Financial Services , Corporate Finance, and AgriTech industries. Proven track record in end to end program execution, aligning technology with business strategy to drive operational efficiency, customer experience, and compliance adherence.  I have passion for new technologies like Agentic AI , Generative AI and much more.


🤝 My Linkedin address ( if you want to connect )  :    https://in.linkedin.com/in/rajendrabichu

**BY : Rajendra Bichu**

#artificialintelligence #ai #machinelearning #aiart #digitalart #technology #datascience #generativeart #innovation #tech #deeplearning #python
#generativeai #chatgpt #machinelearning  #aiarchitecture #openai #aigenerated #architecture #generativearchitecture 

