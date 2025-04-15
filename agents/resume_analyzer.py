# resume_analyzer.py
from crewai import Agent
from tools.resume_parser import ResumeParseTool

class ResumeAnalyzerAgent:
    @staticmethod
    def create():
        """Create a ResumeAnalyzer agent from YAML definition."""
        agent = Agent.from_yaml(
            "agents/definitions/resume_analyzer.yaml",
            tools=[ResumeParseTool()]
        )
        return agent
    
    @staticmethod
    def analyze_resume(resume_path):
        """Analyze a resume and return structured information."""
        return {
            "resume_path": resume_path
        }




