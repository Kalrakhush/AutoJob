# main.py
from crewai import Crew, Process
from agents.resume_analyzer import ResumeAnalyzerAgent
from agents.job_searcher import JobSearcherAgent
from agents.resume_improver import ResumeImproverAgent
from agents.job_applicator import JobApplicatorAgent
from tasks import tasks
import os
import argparse
import json

class JobApplicationBot:
    def __init__(self):
        """Initialize the Job Application Bot."""
        # Create agents
        self.agents = {
            'resume_analyzer': ResumeAnalyzerAgent.create(),
            'job_searcher': JobSearcherAgent.create(),
            'resume_improver': ResumeImproverAgent.create(),
            'job_applicator': JobApplicatorAgent.create()
        }

        # Create tasks
        self.tasks = tasks(self.agents)

        # Create the crew
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            process=Process.sequential,
            verbose=True
        )
        
    def run(self, resume_path, job_keywords=None, location=None, experience_level=None, user_info=None):
        """Run the job application workflow."""
        # Ensure user_info is a dictionary
        if user_info is None:
            user_info = {}
            
        # 1. Analyze resume
        print(f"🔍 Analyzing resume: {resume_path}")
        # Inject context into tasks
        self.tasks['analyze_resume'].context = {
            "resume_path": resume_path
        }
        
        # 2. Search for jobs
        print(f"🔎 Searching for jobs matching resume skills")
        self.tasks['search_jobs'].context = {
            "resume_data": "{analyze_resume.output}",
            "job_keywords": job_keywords,
            "location": location,
            "experience_level": experience_level
        }
        
        # 3. Improve resume for each job
        print(f"✏️ Tailoring resume to match job descriptions")
        self.tasks['improve_resume'].context = {
            "resume_data": "{analyze_resume.output}",
            "job_listings": "{search_jobs.output}"
        }
        
        # 4. Apply for jobs
        print(f"📤 Preparing job applications")
        self.tasks['apply_to_job'].context = {
            "improved_resumes": "{improve_resume.output}",
            "job_listings": "{search_jobs.output}",
            "user_info": user_info
        }
        
        # Create output directory
        os.makedirs("data/user_data", exist_ok=True)
        self.tasks['analyze_resume'].output_file = "data/user_data/parsed_resume.json"
        self.tasks['search_jobs'].output_file = "data/user_data/job_listings.json"
        self.tasks['improve_resume'].output_file = "data/user_data/improved_resumes.json"
        self.tasks['apply_to_job'].output_file = "data/user_data/application_results.json"
        
        # Run the crew
        result = self.crew.run()
        
        return {
            "resume_analysis": result[self.tasks['analyze_resume'].id],
            "job_search": result[self.tasks['search_jobs'].id],
            "resume_improvements": result[self.tasks['improve_resume'].id],
            "job_applications": result[self.tasks['apply_to_job'].id]
        }

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Job Application Bot")
    parser.add_argument("--resume", required=True, help="Path to resume file")
    parser.add_argument("--keywords", help="Job keywords to search for")
    parser.add_argument("--location", help="Job location")
    parser.add_argument("--experience", choices=["entry", "mid", "senior"], help="Experience level")
    parser.add_argument("--user-info", help="Path to JSON file with user information")
    
    args = parser.parse_args()
    
    # Load user info if provided
    user_info = {}
    if args.user_info:
        try:
            with open(args.user_info, 'r') as f:
                user_info = json.load(f)
        except Exception as e:
            print(f"Error loading user info: {e}")
            return
    
    # Create data directory if it doesn't exist
    os.makedirs("data/user_data", exist_ok=True)
    
    # Run the job application bot
    bot = JobApplicationBot()
    result = bot.run(
        resume_path=args.resume,
        job_keywords=args.keywords,
        location=args.location,
        experience_level=args.experience,
        user_info=user_info
    )
    
    # Print results summary
    print("\n=== Job Application Results ===")
    if "job_applications" in result:
        applications = result["job_applications"]
        if isinstance(applications, list):
            print(f"Applied to {len(applications)} jobs:")
            for app in applications:
                if isinstance(app, dict):
                    print(f"- {app.get('platform', 'Unknown')}: {app.get('status', 'Unknown')}")
        else:
            print("No applications submitted")
    else:
        print("No application results available")

if __name__ == "__main__":
    main()