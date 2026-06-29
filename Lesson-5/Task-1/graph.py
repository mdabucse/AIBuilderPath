from typing import Literal
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage

from agents import supervisor_node, it_node, finance_node, it_tools, finance_tools

# Tool Nodes
it_tool_node = ToolNode(it_tools)
finance_tool_node = ToolNode(finance_tools)

# Define the StateGraph using standard MessagesState
workflow = StateGraph(MessagesState)

# Add Nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("it_agent", it_node)
workflow.add_node("it_tools", it_tool_node)
workflow.add_node("finance_agent", finance_node)
workflow.add_node("finance_tools", finance_tool_node)

# Routing function from Supervisor
def route_to_specialist(state: MessagesState) -> Literal["it_agent", "finance_agent"]:
    # The supervisor node appends an AIMessage with content "IT" or "Finance"
    last_msg = state["messages"][-1]
    if last_msg.content == "IT":
        return "it_agent"
    return "finance_agent"

# Routing functions for agents (to tools or END)
def route_it_agent(state: MessagesState) -> Literal["it_tools", "__end__"]:
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "it_tools"
    return "__end__"

def route_finance_agent(state: MessagesState) -> Literal["finance_tools", "__end__"]:
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "finance_tools"
    return "__end__"

# Add Edges
workflow.add_edge(START, "supervisor")

# Supervisor to specialists
workflow.add_conditional_edges(
    "supervisor",
    route_to_specialist,
    {
        "it_agent": "it_agent",
        "finance_agent": "finance_agent"
    }
)

# IT Agent to Tools or END
workflow.add_conditional_edges(
    "it_agent",
    route_it_agent,
    {
        "it_tools": "it_tools",
        "__end__": END
    }
)
# After IT tools run, go back to IT Agent
workflow.add_edge("it_tools", "it_agent")


# Finance Agent to Tools or END
workflow.add_conditional_edges(
    "finance_agent",
    route_finance_agent,
    {
        "finance_tools": "finance_tools",
        "__end__": END
    }
)
# After Finance tools run, go back to Finance Agent
workflow.add_edge("finance_tools", "finance_agent")

# Compile the graph
app = workflow.compile()
