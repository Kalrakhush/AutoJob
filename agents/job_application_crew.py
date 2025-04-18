from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.resume_parser import ResumeParseTool
from crewai_tools import SerperDevTool
from tools.web_search import DuckDuckGoSearchTool, TavilySearchTool
from services.llm_service import LLMService
import os
import yaml
@CrewBase
class jobApplicationCrew():
    """Job application crew"""

    def __init__(self):
        super().__init__()
        # Load agent and task configs
        with open("agents/config/agents.yaml", "r") as file:
            self.agents_config = yaml.safe_load(file)
        with open("agents/config/tasks.yaml", "r") as file:
            self.tasks_config = yaml.safe_load(file)
        # Initialize tools
        self.resume_parser = ResumeParseTool()
        self.search = DuckDuckGoSearchTool()
        self.tavily_search = TavilySearchTool()
        self.search_tool = SerperDevTool()
        self.llm = LLMService()

    @agent
    def ResumeAnalyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['ResumeAnalyzer'],
            verbose=True,
        )

    @agent
    def ResumeImprover(self) -> Agent:
        return Agent(
            config=self.agents_config['ResumeImprover'],
            verbose=True,
        )

    @agent
    def JobSearcher(self) -> Agent:
        return Agent(
            config=self.agents_config['JobSearcher'],
            verbose=True,
            tools=[self.tavily_search, self.search_tool, self.search]
        )

    @task
    def analyze_resume(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_resume']
        )

    @task
    def search_jobs(self) -> Task:
        return Task(
            config=self.tasks_config['search_jobs']
        )

    @task
    def improve_resume(self) -> Task:
        return Task(
            config=self.tasks_config['improve_resume']
        )
    

    