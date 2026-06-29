import uuid
from langchain_core.messages import HumanMessage
from graph import app

def main():
    print("Welcome to the Multi-Agent Support System (IT & Finance)!")
    print("Type 'exit' or 'quit' to stop.\n")
    
    # Thread config for memory (if we want to use checkpoints later, for now just basic invocation)
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        print("\n--- System Processing ---")
        
        # Invoke the graph with the user's message
        initial_state = {"messages": [HumanMessage(content=user_input)]}
        
        # Stream the events from the graph
        for event in app.stream(initial_state, config=config, stream_mode="values"):
            messages = event.get("messages", [])
            if messages:
                latest_msg = messages[-1]
                # Print output from the agents, not human messages
                if latest_msg.type == "ai":
                    if latest_msg.content:
                        print(f"{latest_msg.name or 'Agent'}: {latest_msg.content}")
                    elif hasattr(latest_msg, "tool_calls") and latest_msg.tool_calls:
                        for tool_call in latest_msg.tool_calls:
                            print(f"[Calling Tool: {tool_call['name']}]")
                elif latest_msg.type == "tool":
                    print(f"[Tool Output from {latest_msg.name}]: {latest_msg.content[:200]}...")
                    
        print("-------------------------\n")

if __name__ == "__main__":
    main()
