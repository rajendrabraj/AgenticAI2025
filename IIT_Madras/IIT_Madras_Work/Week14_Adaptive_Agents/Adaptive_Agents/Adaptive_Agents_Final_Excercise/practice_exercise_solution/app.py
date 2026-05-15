from core.agent import AdaptiveAgent

def main():
    agent = AdaptiveAgent()

    query = input("Ask a question.")
    print("Agent response (initial):")
    print(agent.get_response(query))

    # feedback_sequence = ["too formal", "too short", "too long", "too casual"]
    # for feedback in feedback_sequence:
    #     print(f"\nUser feedback: {feedback}")
    #     agent.update_strategy(feedback)
    #     print("Agent response (after adapting):")
    #     print(agent.get_response(query))
    #     print("#"*50)

    feedback = input("Please provide your feedback.")
    print(f"\nUser feedback: {feedback}")
    agent.update_strategy(feedback)
    print("Agent response (after adapting):")
    print(agent.get_response(query))
    print("#"*50)
    
    print("\nFeedback memory:", agent.feedback_memory)
    print("Final style:", agent.style)

if __name__ == "__main__":
    main()
