
** 🧠 **Crew AI Capstone Project Work**

---
💡  **Problem Statement** 
        AI Engineer or Applied AI Consultant inside a ecommerce company. The organization wants to deploy an AI agent that can assist users in real workflows — handling ambiguity, reasoning across steps, using tools, learning from feedback, and operating safely in production. You must design an AI agent that supports a realistic business workflow in one chosen industry scenario. The agent should demonstrate reliability, explainability, safety-first behavior, and practical usefulness for real users, with evidence through artefacts and test logs.

** 💡 **Multi Agent Setup (Agents) **

🧠  Customer Agent Chabot   User Inputs using Queries of the Interactive Customer Agent Chabot
    •	Interactive (Chatbot) – This will ask queries in a loop unless “Exit or quit” 
    •	Multi Agents are executed using the Safe Prompts and different prompts. 
    •	Agents process the User input queries. 

🧠 Intent Agent :  Understands what the user actually wants. It classifies the query (billing, technical, refund, etc.) and extracts intent so the system routes the request correctly.

💡  Memory Agent:  Manages conversation context across turns. It combines short-term memory (current chat) and long-term memory (history/preferences) to make responses context-aware.

🔍 Retrieval Agent :  Fetches relevant information from the knowledge base. Uses vector search (Pinecone + OpenAI embeddings) via LangChain to find the most relevant documents for the query.

💡 Reasoning Agent :  Analyzes retrieved data and generates the final answer. Applies logic, business rules, and LLM reasoning to produce accurate, user-friendly responses.

🚨 Escalation Agent :  Decides when a human should take over. Triggers escalation for sensitive queries, low-confidence answers, or unresolved issues.

📝 Audit Agent :  Tracks and logs everything for compliance and improvement.  Stores conversations, decisions, and tool usage for monitoring, debugging, and governance.

🧠 Final Integrated Agents Workflow -  :  Intent → Memory → Retrieval → Reasoning → (Escalation if needed) → Audit

---

**  🧠 **Streamlit Integration**

📝 This will be like a “Front end” to Enter the query , submit the query(using the Submit Button)  and show the results in a Text Area.

---

** 💡  **Agent Tasks** 

📝  Intent Task
📝  Identifies the user’s intent from the input query and assigns a confidence score for accuracy. Helps route the request to the appropriate workflow or downstream processing agent.

Safety Task
📝 Scans user input for unsafe, harmful, or policy-violating content before processing. Detects and redacts sensitive personal information (PII) to ensure secure handling.

Retrieval Task
📝 Fetches relevant documents and contextual information from the knowledge base. Ensures the response generation process is grounded in accurate and domain-specific data.

📝 Resolution Task with Tools
Uses tools and external knowledge sources to generate context-aware resolutions. Retrieves supporting information from the knowledge base or vector database when required.

Resolution Task
📝 Generates the final user-facing response using retrieved knowledge and context.  Provides clear explanations and accurate resolutions tailored to the user query.

Escalation Task
📝 Evaluates whether the issue requires intervention from a human support agent. Produces an escalation decision along with reasoning for transparency and traceability.

Audit Task
📝 Records the decision flow and processing steps for compliance and monitoring purposes. Ensures logs are stored securely without retaining any personal or sensitive information.

Evaluation Task
📝 Assesses the generated response across multiple quality dimensions such as accuracy, safety, completeness, clarity, and policy compliance.  Produces a structured evaluation summary with category-wise scores and an overall performance rating.

---

** 🔍 **Stream Lit Interface(Front End)**

<img width="846" height="965" alt="image" src="https://github.com/user-attachments/assets/7ad6b1e6-db1f-497d-abdb-8ea3cb1dba2b" />

