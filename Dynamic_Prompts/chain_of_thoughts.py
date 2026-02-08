# Initialize client
import os
import json
from langchain_openai import ChatOpenAI

from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, SystemMessage

from textwrap import indent
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

import warnings
warnings.filterwarnings('ignore')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

######-==========


# Define reasoning templates for different problem types
REASONING_TEMPLATES = {
    "math_word_problem": """
Let's think through this step by step:
1. First, identify what the problem is asking for
2. Extract the relevant numbers and variables
3. Determine the mathematical operations needed
4. Set up the equation or calculation
5. Solve step by step
6. Verify the answer makes sense
""",

    "logical_deduction": """
Let's reason through this logically:
1. List all the given facts and constraints
2. Identify relationships between elements
3. Look for contradictions or implications
4. Make inferences from the available information
5. Build conclusions step by step
6. Check for consistency
""",

    "code_debugging": """
Let's debug this systematically:
1. Understand what the code should do vs what it actually does
2. Identify the specific error or unexpected behavior
3. Trace through the code execution step by step
4. Check variable values and data flow
5. Isolate the problematic section
6. Propose and test fixes
"""
}
# Example problems - you can replace these dynamically
problems = {
    "math_problem": "If a store has 15 apples and sells 8, then receives a shipment of 12 more apples, how many apples do they have now?",
    
    "logic_puzzle": "There are three people: Alice, Bob, and Charlie. Alice is taller than Bob. Charlie is shorter than Bob. Who is the tallest?",
    
    "debugging_issue": "This Python function should return the sum of even numbers in a list, but it's returning incorrect results:\n\n```python\ndef sum_even_numbers(numbers):\n    total = 0\n    for num in numbers:\n        if num % 2 == 0:\n            total += num\n    return total\n\n# Test case: sum_even_numbers([1, 2, 3, 4, 5, 6]) returns 9 instead of 12\n```"
}


problem = problems["math_problem"]
problem_type = "math_word_problem"


prompt = f"""
You are an AI reasoning assistant. Your task is to solve prolems using step-by-step reasoning.

PROBLEM:
{problem}

REASONING_APPROACH:
{REASONING_TEMPLATES[problem_type]}

Please work through this problem sytematically and show your reasoning at each step before providing the final answer.

Format the response like this:
Step 1: <....>
step 2: <....>
.
.

Final Answer: <>

"""

print(prompt)

messages = [
    SystemMessage(content="You are a helpful, clear and careful assistant. Provide a concise final answer and a brief, high level stepwise summary."),
    HumanMessage(content=prompt)
]

# response = llm(messages)
# response_content = response.content


print("-----"*50)
response_to_new_prompt = llm.invoke(messages)
print(response_to_new_prompt.content)

print("-----"*50)


##problem = problems["math_problem"]

problem = problems["logic_puzzle"]
problem_type = "logical_deduction"


messages2 = [
    SystemMessage(content="You are a helpful, clear and careful assistant. Provide a concise final answer and a brief, high level stepwise summary."),
    HumanMessage(content=prompt)
]


print("-----"*50)
response_logical_prompt = llm.invoke(messages2)
print(response_logical_prompt.content)

print("-----"*50)
