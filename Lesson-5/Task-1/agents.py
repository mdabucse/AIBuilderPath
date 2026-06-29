from typing import Literal
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState
from tools import read_it_doc, read_finance_doc, web_search_tool

# Initialize the LLM (make sure ollama is running locally with llama3.2:3b)
# You might need to change the model name to one you have pulled (e.g. 'llama3.2', 'qwen2.5-coder')
llm = ChatOllama(model="llama3.2:3b", temperature=0)

# IT Agent setup
it_tools = [read_it_doc, web_search_tool]
it_llm = llm.bind_tools(it_tools)

# Finance Agent setup
finance_tools = [read_finance_doc, web_search_tool]
finance_llm = llm.bind_tools(finance_tools)

class RouteResponse(BaseModel):
    next_agent: Literal["IT", "Finance"] = Field(
        description="The agent to route the query to. 'IT' for IT-related queries, 'Finance' for Finance-related queries."
    )

# Supervisor needs structured output
supervisor_llm = llm.with_structured_output(RouteResponse)

def supervisor_node(state: MessagesState):
    """Classifies user queries as IT or Finance."""
    messages = state["messages"]
    system_msg = SystemMessage(
        content="You are a supervisor routing user queries to specialist agents. "
                "Classify the user's query into one of two categories: 'IT' or 'Finance'. "
                "IT handles software, hardware, VPN, access, and technical issues. "
                "Finance handles budget, reimbursement, payroll, and expenses."
    )
    # Get the latest human message
    human_msg = next((msg for msg in reversed(messages) if isinstance(msg, HumanMessage)), None)
    if not human_msg:
        raise ValueError("No human message found to route.")
        
    response = supervisor_llm.invoke([system_msg, human_msg])
    
    # Store the routing decision in the state. 
    # But for a simpler flow, we can just return a message indicating the route, 
    # or handle the routing in a conditional edge.
    # In LangGraph, usually the supervisor returns a special AIMessage or we extract the route in the edge.
    # We will append an AIMessage containing the routing decision so the edge can read it.
    from langchain_core.messages import AIMessage
    return {"messages": [AIMessage(content=response.next_agent, name="supervisor")]}

def it_node(state: MessagesState):
    """Handles IT-related queries."""
    messages = state["messages"]
    system_msg = SystemMessage(
        content="You are a helpful IT support agent. Use your tools to answer the user's IT query. "
                "For internal processes, use read_it_doc. For external info, use web_search_tool."
    )
    response = it_llm.invoke([system_msg] + messages)
    return {"messages": [response]}

def finance_node(state: MessagesState):
    """Handles Finance-related queries."""
    messages = state["messages"]
    system_msg = SystemMessage(
        content="You are a helpful Finance support agent. Use your tools to answer the user's Finance query. "
                "For internal processes, use read_finance_doc. For external info, use web_search_tool."
    )
    response = finance_llm.invoke([system_msg] + messages)
    return {"messages": [response]}
