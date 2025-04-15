# web_search.py
import json
import requests
from crewai import Tool
from pydantic import BaseModel, Field
from typing import Optional

class WebSearchInput(BaseModel):
    query: str = Field(description="Search query for job listings")
    location: Optional[str] = Field(None, description="Location for job search")
    experience_level: Optional[str] = Field(None, description="Experience level (entry, mid, senior)")

class WebSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name="WebSearchTool",
            description="Searches for job listings across multiple platforms",
            input_schema=WebSearchInput
        )
    
    def _run(self, query: str, location: Optional[str] = None, experience_level: Optional[str] = None) -> list:
        """Search for job listings using the provided parameters."""
        # In a production environment, this would use actual API calls to job boards
        # For now, we'll simulate the search functionality
        
        # Construct search query
        search_query = query
        if location:
            search_query += f" in {location}"
        if experience_level:
            search_query += f" {experience_level} level"
            
        try:
            # Simulate API call to job boards
            # In production, replace with actual API calls
            mock_results = self._simulate_job_search(search_query, location, experience_level)
            return mock_results
        except Exception as e:
            return {"error": str(e)}
    
    def _simulate_job_search(self, query, location, experience_level):
        """Simulate job search API calls."""
        # This is a mock implementation - replace with actual API calls
        # For demonstration purposes only
        
        # Parse query to find relevant keywords
        keywords = query.lower().split()
        tech_keywords = ["python", "javascript", "react", "developer", "engineer", "data", "scientist"]
        relevant_keywords = [k for k in keywords if k in tech_keywords]
        
        # Generate mock job listings based on query components
        job_listings = []
        
        if "python" in keywords or "data" in keywords:
            job_listings.extend([
                {
                    "title": "Python Developer",
                    "company": "TechCorp",
                    "location": location or "Remote",
                    "description": "We're looking for a Python developer with experience in Flask or Django.",
                    "requirements": ["Python", "Flask/Django", "SQL", "Git"],
                    "salary_range": "$80,000 - $120,000",
                    "url": "https://example.com/jobs/python-dev",
                    "posted_date": "2025-04-01"
                },
                {
                    "title": "Data Scientist",
                    "company": "AnalyticsPro",
                    "location": location or "New York, NY",
                    "description": "Join our data science team to build machine learning models.",
                    "requirements": ["Python", "Pandas", "scikit-learn", "SQL", "Statistics"],
                    "salary_range": "$90,000 - $140,000",
                    "url": "https://example.com/jobs/data-scientist",
                    "posted_date": "2025-04-05"
                }
            ])
            
        if "javascript" in keywords or "react" in keywords:
            job_listings.extend([
                {
                    "title": "Frontend Developer",
                    "company": "WebSolutions",
                    "location": location or "San Francisco, CA",
                    "description": "Build responsive web applications using React.",
                    "requirements": ["JavaScript", "React", "HTML/CSS", "Git"],
                    "salary_range": "$85,000 - $130,000",
                    "url": "https://example.com/jobs/frontend-dev",
                    "posted_date": "2025-04-10"
                }
            ])
            
        if "engineer" in keywords or "developer" in keywords:
            job_listings.extend([
                {
                    "title": "Software Engineer",
                    "company": "InnovateInc",
                    "location": location or "Austin, TX",
                    "description": "Join our team to build scalable software solutions.",
                    "requirements": ["Java/Python/C++", "Cloud Services", "Algorithms", "CI/CD"],
                    "salary_range": "$95,000 - $150,000",
                    "url": "https://example.com/jobs/software-engineer",
                    "posted_date": "2025-04-08"
                }
            ])
        
        # If no relevant keywords, return general tech jobs
        if not job_listings:
            job_listings = [
                {
                    "title": "IT Support Specialist",
                    "company": "TechHelp",
                    "location": location or "Chicago, IL",
                    "description": "Provide technical support to users.",
                    "requirements": ["Troubleshooting", "Windows/Linux", "Network basics"],
                    "salary_range": "$60,000 - $80,000",
                    "url": "https://example.com/jobs/it-support",
                    "posted_date": "2025-04-12"
                }
            ]
            
        # Filter by experience level if provided
        if experience_level:
            if experience_level.lower() == "entry":
                for job in job_listings:
                    job["title"] = "Junior " + job["title"]
                    job["salary_range"] = "$60,000 - $80,000"
            elif experience_level.lower() == "senior":
                for job in job_listings:
                    job["title"] = "Senior " + job["title"]
                    job["salary_range"] = "$120,000 - $180,000"
        
        return job_listings

