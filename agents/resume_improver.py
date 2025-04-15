# resume_improver.py
from crewai import Agent
from tools.resume_formatter import ResumeFormatterTool

class ResumeImproverAgent:
    @staticmethod
    def create():
        """Create a ResumeImprover agent from YAML definition."""
        agent = Agent.from_yaml(
            "agents/definitions/resume_improver.yaml",
            tools=[ResumeFormatterTool()]
        )
        return agent
    
    @staticmethod
    def improve_resume(resume_data, job_description):
        """Improve a resume based on a job description."""
        return {
            "resume_data": resume_data,
            "job_description": job_description
        }