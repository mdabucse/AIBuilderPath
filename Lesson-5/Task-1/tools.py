import os
from langchain_core.tools import tool
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper

# Initialize wikipedia search
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
web_search = WikipediaQueryRun(api_wrapper=api_wrapper)

@tool
def read_it_doc() -> str:
    """Reads the internal IT documentation."""
    file_path = os.path.join(os.path.dirname(__file__), "mock_data", "it_docs.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return "IT documentation not found."

@tool
def read_finance_doc() -> str:
    """Reads the internal Finance documentation."""
    file_path = os.path.join(os.path.dirname(__file__), "mock_data", "finance_docs.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return "Finance documentation not found."

@tool
def web_search_tool(query: str) -> str:
    """Useful for searching the web for current events or external knowledge.
    Use this when the user query requires external knowledge that is not in the internal docs."""
    return web_search.invoke(query)
