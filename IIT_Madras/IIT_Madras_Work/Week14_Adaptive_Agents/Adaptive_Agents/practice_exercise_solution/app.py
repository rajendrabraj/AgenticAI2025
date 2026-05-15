from core.agent import AdaptiveAgent

def main():
    agent = AdaptiveAgent(feedback_memory=None, style="concise")

    #query = "Explain reinforcement learning in simple terms."

    query = input("\n PLEASE ASK YOUR QUESTION :  ")    

    print("Agent response (initial):")
    print(agent.get_response(query))

    # feedback_sequence = ["too formal", "too short", "too long", "too casual"]
    # for feedback in feedback_sequence:
    #     print(f"\nUser feedback: {feedback}")
    #     print("=="*50)
    #     agent.update_strategy(feedback)
    #     print("=="*50)
    #     print("Agent response (after adapting):")
    #     print(agent.get_response(query))
    #     print("=="*50)
    
    feedback = input("Please provide your feedback")    
    print(f"\nUser feedback: {feedback}")
    print("=="*50)
    agent.update_strategy(feedback)
    print("=="*50)
    input_style = input("Please enter Style (concise, detailed,casual,formal)\n  :  ")  
    agent = AdaptiveAgent(feedback_memory=None, style=input_style)
    print("Agent response (after adapting):")
    print(agent.get_response(query))
    print("=="*50)
    

    print("=="*50)
    print("\nFeedback memory:", agent.feedback_memory)
    print("Final style:", agent.style)
    print("=="*50)

if __name__ == "__main__":
    main()
