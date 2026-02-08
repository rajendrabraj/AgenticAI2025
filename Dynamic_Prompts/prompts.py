# Initialize client
import os
import json
from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, SystemMessage


from textwrap import indent
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import warnings
warnings.filterwarnings('ignore')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def compare_prompts(raw_prompt: str, tuned_prompt: str, title="Prompt Comparison"):
    """
    Compares raw vs Tuned prompt using the same LLM.
    """
    print(title)
    print("+"*50)

    # RAW Prompt and call LLM with it
    raw_message = [
        SystemMessage(content="You are a very helpful assistant."),
        HumanMessage(content=raw_prompt)
    ]

    raw_response = llm.invoke(raw_message)
    raw_content = raw_response.content.strip()


    # Tuned Prompt and call LLM with it
    tuned_message = [
        SystemMessage(content="You are a very helpful assistant."),
        HumanMessage(content=tuned_prompt)
    ]

    tuned_response = llm.invoke(tuned_message)
    tuned_content = tuned_response.content.strip()

    
    # PRINT OUTPUTS
    print("RAW PROMPT:")
    print("--------------------------------")
    print(raw_prompt)
    print("\nRAW RESPONSE:")
    print(indent(raw_content, "    "))

    print("\n\nTUNED PROMPT:")
    print("--------------------------------")
    print(tuned_prompt)
    print("\nTUNED RESPONSE:")
    print(indent(tuned_content, "    "))

    print("\n==============================")
    print("END OF COMPARISON")
# EXAMPLE USAGE — FINTECH LOAN DECISION EXPLAINER

raw_prompt_loan = """
Explain why the customer was denied the loan.
"""
tuned_prompt_loan = """
You are a financial assistant that explains loan decisions clearly.

Rules:
• Do NOT invent reasons — only use provided ones.
• Do NOT mention internal scoring systems.
• Be supportive and simple.
• Provide next steps.

Input:
Loan Status: DENIED
Reason Provided: Low credit history, missing income documents.

Format:
1. Summary
2. Main Factors (bullets)
3. Next Steps
"""

tuned_prompt_vector_db = """
You are explaining to a Product Manager with no machine learning background.

Context:
The listener understands products and user experience but not AI terminology.

Task:
Explain what a Vector Database is.

Instructions:
1. Use one real-life analogy
2. Use one popular app example (Google, Netflix, or Amazon)
3. Explain why it is useful, not how it is built

Constraints:
- No math
- No technical or ML jargon
- Simple, conversational language
- Maximum 120 words

Output format:
- Analogy
- App example
- Why it matters
"""



compare_prompts(raw_prompt_loan, tuned_prompt_loan, title="Loan Decision Explanation Comparison")   


