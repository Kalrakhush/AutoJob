from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.resume_parser import ResumeParseTool
from crewai_tools import BraveSearchTool
from crewai_tools import SerperDevTool
from tools.web_search import DuckDuckGoSearchTool , TavilySearchTool
from services.llm_service import LLMService
from config import GEMINI_API_KEY, SERPER_API_KEY
import os
import yaml

llm=LLMService()
# Load agent and task configs
with open("agents/config/agents.yaml", "r") as f:
    agents_config = yaml.safe_load(f)

with open("agents/config/tasks.yaml", "r") as f:
    tasks_config = yaml.safe_load(f)

resume_parser = ResumeParseTool()
search = DuckDuckGoSearchTool()
tavilly_search = TavilySearchTool()


search_tool = SerperDevTool()

os.environ["SERPER_API_KEY"] = SERPER_API_KEY
os.environ['TAVILY_API_KEY'] = os.environ.get("TAVILY_API_KEY", "your-tavily-api-key")

res= resume_parser._run({"resume_path": r"C:\Users\15038\Documents\Khushpreet's Resume.pdf"})
@CrewBase
class jobApplicationCrew():
    """Job application crew"""

    agents_config = r"D:\Projects\Pytorch\agents\config\agents.yaml"
    tasks_config = r'D:\Projects\Pytorch\agents\config\tasks.yaml'

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
            tools=[tavilly_search, search_tool, search]
        )

    # @agent
    # def job_applicator(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['JobApplicator'],
    #         verbose=True
    #     )

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

    # @task
    # def apply_to_job(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['apply_to_job']
    #     )


# Instantiate the crew and kickoff the process
if __name__ == "__main__":
    crew_base = jobApplicationCrew()
    
    crew = Crew(
        agents=[
            crew_base.resume_analyzer(),
            crew_base.resume_improver(),
            crew_base.job_searcher(),
            # crew_base.job_applicator()
        ],
        tasks=[
            crew_base.analyze_resume(),
            crew_base.search_jobs(),
            crew_base.improve_resume(),
            # crew_base.apply_to_job()
        ],
        verbose=True,
        process=Process.sequential,
        # planning=True,
        # planning_llm = llm,
        #     # Enable planning feature
    )
    
    result = crew.kickoff(inputs={"resume":str(res) , "location": "Delhi NCR"})
    print("\n\n✅ Final Result:")
    print(result)
