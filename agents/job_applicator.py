# job_applicator.py
from crewai import Agent
from tools.job_submission import JobSubmissionTool

class JobApplicatorAgent:
    @staticmethod
    def create():
        """Create a JobApplicator agent from YAML definition."""
        agent = Agent.from_yaml(
            "agents/definitions/job_applicator.yaml",
            tools=[JobSubmissionTool()]
        )
        return agent
    
    @staticmethod
    def apply_for_job(job_url, resume_path, user_info, cover_letter=None):
        """Apply for a job with the improved resume."""
        return {
            "job_url": job_url,
            "resume_path": resume_path,
            "cover_letter": cover_letter,
            "user_info": user_info
        }