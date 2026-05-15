from core.agent import AdaptiveAgent

def main():
    agent = AdaptiveAgent()

    query = "Explain reinforcement learning in simple terms."
    print("Agent response (initial):")
    print(agent.get_response(query))

    feedback_sequence = ["too formal", "too short", "too long", "too casual"]
    for feedback in feedback_sequence:
        print(f"\nUser feedback: {feedback}")
        print("=="*50)
        agent.update_strategy(feedback)
        print("=="*50)
        print("Agent response (after adapting):")
        print(agent.get_response(query))
        print("=="*50)
    
    print("=="*50)
    print("\nFeedback memory:", agent.feedback_memory)
    print("Final style:", agent.style)
    print("=="*50)

if __name__ == "__main__":
    main()
