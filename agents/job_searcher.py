# job_searcher.py
from crewai import Agent
from tools.web_search import WebSearchTool

class JobSearcherAgent:
    @staticmethod
    def create():
        """Create a JobSearcher agent from YAML definition."""
        agent = Agent.from_yaml(
            "agents/definitions/job_searcher.yaml",
            tools=[WebSearchTool()]
        )
        return agent
    
    @staticmethod
    def search_jobs(skills, preferences, location=None, experience_level=None):
        """Search for jobs based on skills and preferences."""
        query = f"Jobs for {skills} {experience_level if experience_level else ''}"
        return {
            "query": query,
            "location": location,
            "experience_level": experience_level
        }
