from config.settings import client
from core.prompts import build_prompt
from core.feedback import adapt_style
from core.memory import load_memory, save_memory

class AdaptiveAgent:
    def __init__(self):
        self.feedback_memory = load_memory()
        self.style = "concise"
    
    def get_response(self, query):
        prompt = build_prompt(query, self.style)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    
    def update_strategy(self, feedback):
        self.feedback_memory.append(feedback)
        style_as_per_feedback = adapt_style(self.style, feedback)
        if style_as_per_feedback in ["detailed", "concise", "casual", "formal"]:
            self.style = style_as_per_feedback
        
        save_memory(self.feedback_memory)
