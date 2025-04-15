# main.py
from crewai import Crew, Process
from agents.resume_analyzer import ResumeAnalyzerAgent
from agents.job_searcher import JobSearcherAgent
from agents.resume_improver import ResumeImproverAgent
from agents.job_applicator import JobApplicatorAgent
import os
import argparse
import json

class JobApplicationBot:
    def __init__(self):
        """Initialize the Job Application Bot."""
        # Create agents
        self.resume_analyzer = ResumeAnalyzerAgent.create()
        self.job_searcher = JobSearcherAgent.create()
        self.resume_improver = ResumeImproverAgent.create()
        self.job_applicator = JobApplicatorAgent.create()
        
        # Create the crew
        self.crew = Crew(
            agents=[
                self.resume_analyzer,
                self.job_searcher,
                self.resume_improver,
                self.job_applicator
            ],
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
        resume_task = self.crew.add_task(
            task="Analyze the resume to extract skills, experiences, and education",
            agent=self.resume_analyzer,
            expected_output="Structured JSON with resume information",
            output_file="data/user_data/parsed_resume.json",
            context={
                "resume_path": resume_path
            }
        )
        
        # 2. Search for jobs
        print(f"🔎 Searching for jobs matching resume skills")
        job_search_task = self.crew.add_task(
            task="Find relevant job postings based on the resume",
            agent=self.job_searcher,
            expected_output="List of relevant job opportunities",
            output_file="data/user_data/job_listings.json",
            context={
                "resume_data": "{resume_task.output}",
                "job_keywords": job_keywords,
                "location": location,
                "experience_level": experience_level
            }
        )
        
        # 3. Improve resume for each job
        print(f"✏️ Tailoring resume to match job descriptions")
        resume_improvement_task = self.crew.add_task(
            task="Improve the resume for each job opportunity",
            agent=self.resume_improver,
            expected_output="Improved resume versions for each job",
            output_file="data/user_data/improved_resumes.json",
            context={
                "resume_data": "{resume_task.output}",
                "job_listings": "{job_search_task.output}"
            }
        )
        
        # 4. Apply for jobs
        print(f"📤 Preparing job applications")
        job_application_task = self.crew.add_task(
            task="Apply for selected jobs with improved resumes",
            agent=self.job_applicator,
            expected_output="Application submission results",
            output_file="data/user_data/application_results.json",
            context={
                "improved_resumes": "{resume_improvement_task.output}",
                "job_listings": "{job_search_task.output}",
                "user_info": user_info
            }
        )
        
        # Run the crew
        result = self.crew.run()
        
        return {
            "resume_analysis": result[resume_task.id],
            "job_search": result[job_search_task.id],
            "resume_analysis": result[resume_task.id],
            "job_search": result[job_search_task.id],
            "resume_improvements": result[resume_improvement_task.id],
            "job_applications": result[job_application_task.id]
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