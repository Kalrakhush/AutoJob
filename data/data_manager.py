import os
import json
import shutil
from datetime import datetime
from pathlib import Path

class DataManager:
    """Manages data storage and retrieval for the job application agent."""
    
    def __init__(self, base_dir="data"):
        self.base_dir = Path(base_dir)
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Creates necessary directories if they don't exist."""
        directories = [
            "user_data/resumes",
            "user_data/improved_resumes",
            "user_data/cover_letters",
            "user_data/job_listings",
            "user_data/application_status",
            "templates/resume_templates",
            "templates/cover_letter_templates",
            "cache"
        ]
        
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def save_resume(self, resume_content, filename=None):
        """Save original resume."""
        if filename is None:
            filename = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        file_path = self.base_dir / "user_data/resumes" / filename
        
        with open(file_path, 'wb') as f:
            f.write(resume_content)
        
        return str(file_path)
    
    def save_improved_resume(self, resume_content, job_id, filename=None):
        """Save tailored resume for a specific job."""
        if filename is None:
            filename = f"improved_resume_{job_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        file_path = self.base_dir / "user_data/improved_resumes" / filename
        
        with open(file_path, 'wb') as f:
            f.write(resume_content)
        
        return str(file_path)
    
    def save_job_listing(self, job_data):
        """Save job listing data."""
        job_id = job_data.get('id', str(int(datetime.now().timestamp())))
        filename = f"job_{job_id}.json"
        
        file_path = self.base_dir / "user_data/job_listings" / filename
        
        with open(file_path, 'w') as f:
            json.dump(job_data, f, indent=2)
        
        return job_id, str(file_path)
    
    def update_application_status(self, job_id, status, details=None):
        """Update application status for a job."""
        filename = f"status_{job_id}.json"
        file_path = self.base_dir / "user_data/application_status" / filename
        
        status_data = {
            "job_id": job_id,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        
        with open(file_path, 'w') as f:
            json.dump(status_data, f, indent=2)
        
        return str(file_path)
    
    def get_resume_template(self, template_name="standard"):
        """Get a resume template."""
        template_path = self.base_dir / "templates/resume_templates" / f"{template_name}.template"
        
        if not template_path.exists():
            return None
        
        with open(template_path, 'r') as f:
            return f.read()
    
    def get_cover_letter_template(self, template_name="standard"):
        """Get a cover letter template."""
        template_path = self.base_dir / "templates/cover_letter_templates" / f"{template_name}.template"
        
        if not template_path.exists():
            return None
        
        with open(template_path, 'r') as f:
            return f.read()
    
    def get_cached_data(self, cache_key):
        """Retrieve cached data."""
        cache_file = self.base_dir / "cache" / f"{cache_key}.json"
        
        if not cache_file.exists():
            return None
        
        with open(cache_file, 'r') as f:
            return json.load(f)
    
    def save_cached_data(self, cache_key, data):
        """Save data to cache."""
        cache_file = self.base_dir / "cache" / f"{cache_key}.json"
        
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(cache_file)
    
    def list_saved_resumes(self):
        """List all saved original resumes."""
        resume_dir = self.base_dir / "user_data/resumes"
        return [f.name for f in resume_dir.glob("*")]
    
    def list_job_listings(self):
        """List all saved job listings."""
        job_dir = self.base_dir / "user_data/job_listings"
        return [f.name for f in job_dir.glob("*")]