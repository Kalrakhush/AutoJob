# tools/web_search.py
from pydantic import PrivateAttr
from crewai.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

class DuckDuckGoSearchTool(BaseTool):
    name: str = "duckduckgo_search_tool"
    description: str = "A tool for performing web searches using DuckDuckGo."
    
    # Declare a private attribute to hold our search instance.
    _search_instance: DuckDuckGoSearchRun = PrivateAttr()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the search tool using DuckDuckGoSearchRun
        self._search_instance = DuckDuckGoSearchRun(**kwargs)

    def _run(self, query: str) -> dict:
        """Run the search query and return the result as a dictionary."""
        # Call the underlying search tool's run method.
        return self._search_instance.run(query)



class TavilySearchTool(BaseTool):
    """
    A tool for performing web searches using the Tavily search API.
    Input: query string
    Output: dict of search results
    """
    name: str = "tavily_search_tool"
    description: str = (
        "A search engine optimized for comprehensive, accurate, and trusted results. "
        "Useful for when you need current events or recent information."
    )

    # Private attribute to hold the wrapped Tavily search results tool
    _search_instance: TavilySearchResults = PrivateAttr()

    def __init__(self, tavily_api_key: str = None, **kwargs):
        super().__init__(**kwargs)
        # Initialize the underlying API wrapper and search results tool
        api_wrapper = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
        self._search_instance = TavilySearchResults(api_wrapper=api_wrapper, description=self.description)

    def _run(self, query: str) -> dict:
        """
        Run the search query through Tavily and return the results as a dictionary.
        """
        return self._search_instance.run(query)
