"""Research Agent assembly for Presidio."""

from __future__ import annotations

from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from config import Settings
from tools.mcp_docs_tool import create_google_docs_tools_sync
from tools.rag_tool import create_hr_policy_tool
from tools.web_search_tool import create_web_search_tool


def get_research_agent(settings: Settings | None = None) -> AgentExecutor:
    """Create and configure the Presidio research agent with its tools."""
    settings = settings or Settings.from_env()

    # 1. Initialize ChatOllama LLM
    llm = ChatOllama(
        model=settings.ollama_chat_model,
        base_url=settings.ollama_base_url,
        temperature=0.0,
    )

    # 2. Gather all tools
    hr_tool = create_hr_policy_tool(settings)
    web_tool = create_web_search_tool(settings)
    mcp_tools = create_google_docs_tools_sync(settings)

    tools = [hr_tool, web_tool] + mcp_tools

    # 3. Define ReAct prompt template
    # ReAct agents expect: tools, tool_names, input, agent_scratchpad
    template = (
        "Answer the following questions as best you can. You have access to the following tools:\n\n"
        "{tools}\n\n"
        "Use the following format:\n\n"
        "Question: the input question you must answer\n"
        "Thought: you should always think about what to do\n"
        "Action: the action to take, should be one of [{tool_names}]\n"
        "Action Input: the input to the action\n"
        "Observation: the result of the action\n"
        "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
        "Thought: I now know the final answer\n"
        "Final Answer: the final answer to the original input question\n\n"
        "Begin!\n\n"
        "Question: {input}\n"
        "Thought: {agent_scratchpad}"
    )

    prompt = PromptTemplate.from_template(template)

    # 4. Create ReAct agent
    agent = create_react_agent(llm, tools, prompt)

    # 5. Return AgentExecutor
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
    )
