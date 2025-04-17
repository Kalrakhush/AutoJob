import os
import json
from agents.job_application_crew import jobApplicationCrew
from crewai import Crew, Process
from services.llm_service import LLMService

llm = LLMService()

def execute_resume_analysis(resume_data):
    """
    Execute the resume analysis task.
    
    Args:
        resume_data (str): Resume data as string
        
    Returns:
        dict: Results of the resume analysis
    """
    try:
        # Initialize the crew
        crew_base = jobApplicationCrew()
        
        # Create the crew with just the resume analyzer agent and task
        crew = Crew(
            agents=[crew_base.resume_analyzer()],
            tasks=[crew_base.analyze_resume()],
            verbose=True,
            process=Process.sequential,
        )
        
        # Execute the task
        result = crew.kickoff(inputs={"resume": str(resume_data)})
        
        # Try to parse the result as JSON
        try:
            return json.loads(result)
        except:
            return result
    except Exception as e:
        return f"Error analyzing resume: {str(e)}"

def execute_job_search(resume_data, job_title="", location="Remote"):
    """
    Execute the job search task.
    
    Args:
        resume_data (str): Resume data as string
        job_title (str): Job title or keywords
        location (str): Job location
        
    Returns:
        list: Results of the job search
    """
    try:
        # Initialize the crew
        crew_base = jobApplicationCrew()
        
        # Create the crew with just the job searcher agent and task
        crew = Crew(
            agents=[crew_base.job_searcher()],
            tasks=[crew_base.search_jobs()],
            verbose=True,
            process=Process.sequential,
        )
        
        # Execute the task
        result = crew.kickoff(
            inputs={
                "resume": str(resume_data),
                "job_title": job_title,
                "location": location
            }
        )
        
        # Try to parse the result as JSON
        try:
            return json.loads(result)
        except:
            return result
    except Exception as e:
        return f"Error searching jobs: {str(e)}"

def execute_resume_improvement(resume_data, job_results=None, job_title="", location=""):
    """
    Execute the resume improvement task.
    
    Args:
        resume_data (str): Resume data as string
        job_results (str, optional): Job search results
        job_title (str): Job title or keywords
        location (str): Job location
        
    Returns:
        dict: Results of the resume improvement
    """
    try:
        # Initialize the crew
        crew_base = jobApplicationCrew()
        
        # Create the crew with just the resume improver agent and task
        crew = Crew(
            agents=[crew_base.resume_improver()],
            tasks=[crew_base.improve_resume()],
            verbose=True,
            process=Process.sequential,
        )
        
        # Prepare inputs
        inputs = {
            "resume": str(resume_data),
            "job_title": job_title,
            "location": location
        }
        
        # Add job results if available
        if job_results:
            inputs["job_results"] = str(job_results)
        
        # Execute the task
        result = crew.kickoff(inputs=inputs)
        
        # Try to parse the result as JSON
        try:
            return json.loads(result)
        except:
            return result
    except Exception as e:
        return f"Error improving resume: {str(e)}"