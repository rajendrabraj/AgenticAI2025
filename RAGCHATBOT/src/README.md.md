## Rajendra Bichu.  This is to implement the RAG , Vector Search based on Financial documents and FAQ's
----
🧠 This program is to use RAG Search and build a ChatBOT to process the contents of the files stored in one folder for Financial data, Silver data, Infosys quarterly report


🧑‍💻 Objective :  To read all the files of the financial data and process them using Vector Store , FAISS and RAG based search.


----
🧠 How This Program or tool works.


✅ The program reads the files which are there in the folder, Investment FAQ, Financial data, Silver data, Infosys quarterly report and later on we can query using the RAG data.

✅ Injest.py will ensure that the data is loaded by processing one by one files. Once data is loaded it will be indexed using FAISS and stored in FAISS Vector.

✅ Chatbot.py - This program is send queries to search the vector embedding and return the results. This program gives 3 types of different queries.

✅ dataload.log - A Logfile is created to capture the processing which happens during the runtime.

✅ Data Used for processing  - Infosys quarterly report, Silver Report, and AMFI Mutual fund report of 2025 which were downloaded from the internet

----

----
🧠 This program is to use RAG Search and build a ChatBOT to process the contents of the files stored in one folder for Financial data, Silver data, Infosys quarterly report


🧑‍💻 Objective :  To read all the files of the financial data and process them using Vector Store , FAISS and RAG based search.


----
🧠 How This Program or tool works.


✅ The program reads the files which are there in the folder, Investment FAQ, Financial data, Silver data, Infosys quarterly report and later on we can query using the RAG data.

✅ Injest.py will ensure that the data is loaded by processing one by one files. Once data is loaded it will be indexed using FAISS and stored in FAISS Vector.

✅ Chatbot.py - This program is send queries to search the vector embedding and return the results. This program gives 3 types of different queries.

✅ dataload.log - A Logfile is created to capture the processing which happens during the runtime.

✅ Data Used for processing  - Infosys quarterly report, Silver Report, and AMFI Mutual fund report of 2025 which were downloaded from the internet

✅ Retrieve data of records top_k=10 or top_k-15 , this program uses top_k= 10

----

🧠 Chat BOT  Questions to test the program.

What is Net Asset Value (NAV) of a scheme?
What is Silver performance?
what is silver supply in 2024?
what is silver demand in 2025?
What is silver supply outlook ?
what is the Infosys guidance?
what is longterm approach with SIP? 
How is the domestic equity market for funds?
What is a Balanced/Hybrid Scheme ?
What is Index Funds?
What are Tax Saving Schemes?
What are Exchange Traded Funds (ETFs)?

----



----

