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
        try:
            with open("agents/config/agents.yaml", "r") as f:
                self.agents_config = yaml.safe_load(f)
        except FileNotFoundError:
            # Default configurations if file not found
            self.agents_config = {
                'ResumeAnalyzer': {
                    'role': 'Resume Analyzer',
                    'goal': 'Analyze resumes to extract key information and provide insights',
                    'backstory': 'Expert in resume analysis with years of HR experience',
                    'verbose': True,
                    'allow_delegation': False
                },
                'ResumeImprover': {
                    'role': 'Resume Improver',
                    'goal': 'Provide suggestions to improve resumes based on job postings',
                    'backstory': 'Expert in resume optimization with deep knowledge of recruitment',
                    'verbose': True,
                    'allow_delegation': False
                },
                'JobSearcher': {
                    'role': 'Job Searcher',
                    'goal': 'Find job postings that match the candidate\'s profile',
                    'backstory': 'Expert in job search and recruitment',
                    'verbose': True,
                    'allow_delegation': False
                }
            }
        
        try:
            with open("agents/config/tasks.yaml", "r") as f:
                self.tasks_config = yaml.safe_load(f)
        except FileNotFoundError:
            # Default configurations if file not found
            self.tasks_config = {
                'analyze_resume': {
                    'description': 'Analyze the resume to extract key information',
                    'expected_output': 'A detailed analysis of the resume',
                    'agent': 'ResumeAnalyzer'
                },
                'search_jobs': {
                    'description': 'Search for jobs that match the candidate\'s profile',
                    'expected_output': 'A list of job postings that match the candidate\'s profile',
                    'agent': 'JobSearcher'
                },
                'improve_resume': {
                    'description': 'Provide suggestions to improve the resume',
                    'expected_output': 'A list of suggestions to improve the resume',
                    'agent': 'ResumeImprover'
                }
            }
        
        # Initialize tools
        self.resume_parser = ResumeParseTool()
        self.search = DuckDuckGoSearchTool()
        self.tavily_search = TavilySearchTool()
        self.search_tool = SerperDevTool()
        self.llm = LLMService()

    @agent
    def resume_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['ResumeAnalyzer'],
            verbose=True,
        )

    @agent
    def resume_improver(self) -> Agent:
        return Agent(
            config=self.agents_config['ResumeImprover'],
            verbose=True,
        )

    @agent
    def job_searcher(self) -> Agent:
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
    

    