from typing import List
from pydantic import BaseModel, Field
from langchain.chains.openai_functions import create_qa_with_structure_chain
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

class TableResponseSchema(BaseModel):
    """A table response schema."""
    headers: List[str] = Field(..., description="Headers of the table")
    rows: List[List[str]] = Field(..., description="Rows of the table")

prompt_messages = [
    SystemMessage(
        content=(
            "You are a world class algorithm to answer "
            "questions in a specific format."
        )
    ),
    HumanMessage(content="Answer question using the following context"),
    HumanMessagePromptTemplate.from_template("{context}"),
    HumanMessagePromptTemplate.from_template("Question: {question}"),
    HumanMessage(
        content="Tips: Make sure to answer in the correct format. Return the table with headers and rows."
    ),
]

chain_prompt = ChatPromptTemplate(messages=prompt_messages)

qa_chain_pydantic = create_qa_with_structure_chain(llm, TableResponseSchema, output_parser="pydantic", prompt=chain_prompt
)
final_qa_chain_pydantic = StuffDocumentsChain(
    llm_chain=qa_chain_pydantic,
    document_variable_name="context",
    document_prompt=doc_prompt,
)
retrieval_qa_pydantic = RetrievalQA(
    retriever=docsearch.as_retriever(), combine_documents_chain=final_qa_chain_pydantic
)
print("Executing the query..")
query = "Iphone 16 Product, Specification, price in USD"
result = retrieval_qa_pydantic.run(query)
print("Printing Results in Tablular format..")
print(result)