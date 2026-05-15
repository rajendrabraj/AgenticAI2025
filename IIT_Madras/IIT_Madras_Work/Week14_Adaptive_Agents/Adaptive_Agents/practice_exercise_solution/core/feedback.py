from config.settings import client

# def adapt_style(current_style: str, feedback: str) -> str:
#     rules = {
#         "too short": "detailed",
#         "too long": "concise",
#         "too formal": "casual",
#         "too casual": "formal"
#     }
#     return rules.get(feedback.lower(), current_style)


# def adapt_style(current_style: str, feedback: str) -> str:
#         prompt = f"""
#             Current style: {current_style}
#             User feedback: {feedback}
#             Based on the feedback, return a new style descriptor 
#             (e.g., concise, detailed, casual, formal).
#             Only return the style word.
#             """

#         response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0
#     )

#     return rules.get(feedback.lower(), current_style)


from config.settings import client

def adapt_style(current_style: str, feedback: str) -> str:
    """
    calls LLM
    instucts to look at the feedback and provide an updated style
    Output instructions
    """
    prompt = f"""You are a style defining agent. You take a look at user feedback and provide an updated style accordingly.
    
    Instructions:
    These are possible values for style: detailed, concise, casual and formal.
    Ensure to took at the feedback and you must choose ONLY one of these styles to improve style based on the feedabck.

    Feedback:
    {feedback}
    
    Output format:
    MUST BE 1-word STRING

    example output:
    "detailed"
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()

