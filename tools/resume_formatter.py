# resume_formatter.py
import json
from crewai import Tool
from pydantic import BaseModel, Field
from typing import Dict, Any

class ResumeFormatterInput(BaseModel):
    resume_data: Dict[str, Any] = Field(description="Parsed resume data")
    job_description: str = Field(description="Target job description")

class ResumeFormatterTool(Tool):
    def __init__(self):
        super().__init__(
            name="ResumeFormatterTool",
            description="Reformats and tailors resumes to specific job descriptions",
            input_schema=ResumeFormatterInput
        )
    
    def _run(self, resume_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """Tailor a resume to match a specific job description."""
        try:
            # Extract keywords from job description
            job_keywords = self._extract_keywords(job_description)
            
            # Generate improved resume
            improved_resume = self._tailor_resume(resume_data, job_keywords)
            
            # Return both the original and improved resume for comparison
            return {
                "original_resume": resume_data,
                "improved_resume": improved_resume,
                "matched_keywords": job_keywords,
                "improvements": self._generate_improvement_summary(resume_data, improved_resume)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _extract_keywords(self, job_description):
        """Extract important keywords from job description."""
        # In a production environment, this would use NLP techniques
        # For demonstration, we'll use a simple approach
        
        # List of common technical skills and qualifications
        tech_skills = ["python", "javascript", "java", "c++", "react", "angular", "node", "django", 
                       "flask", "sql", "nosql", "aws", "azure", "gcp", "docker", "kubernetes",
                       "machine learning", "data science", "agile", "scrum", "ci/cd", "devops"]
        
        soft_skills = ["leadership", "communication", "teamwork", "problem solving", 
                       "time management", "analytical", "creativity", "adaptability"]
                       
        qualifications = ["bachelor", "master", "phd", "degree", "certification", "experience"]
        
        keywords = {
            "tech_skills": [],
            "soft_skills": [],
            "qualifications": []
        }
        
        job_desc_lower = job_description.lower()
        
        # Extract technical skills
        for skill in tech_skills:
            if skill in job_desc_lower:
                keywords["tech_skills"].append(skill)
                
        # Extract soft skills
        for skill in soft_skills:
            if skill in job_desc_lower:
                keywords["soft_skills"].append(skill)
                
        # Extract qualifications
        for qual in qualifications:
            if qual in job_desc_lower:
                keywords["qualifications"].append(qual)
                
        return keywords
    
    def _tailor_resume(self, resume_data, job_keywords):
        """Tailor resume to better match job keywords."""
        # Create a deep copy of the resume
        improved = resume_data.copy()
        
        # Prioritize skills that match job keywords
        if "skills" in improved:
            original_skills = improved["skills"]
            prioritized_skills = []
            other_skills = []
            
            # Check each skill against job keywords
            for skill in original_skills:
                skill_lower = skill.lower()
                matched = False
                for tech_skill in job_keywords["tech_skills"]:
                    if tech_skill in skill_lower:
                        prioritized_skills.append(skill)
                        matched = True
                        break
                if not matched:
                    other_skills.append(skill)
            
            # Combine prioritized skills with others
            improved["skills"] = prioritized_skills + other_skills
        
        # Modify experience descriptions to highlight relevant keywords
        if "experience" in improved:
            experiences = improved["experience"]
            for i, exp in enumerate(experiences):
                if isinstance(exp, str):
                    # Enhance string experience entries
                    for keyword in job_keywords["tech_skills"] + job_keywords["soft_skills"]:
                        if keyword.lower() not in exp.lower():
                            # Don't add keywords that don't make sense for this experience
                            continue
                        # Add emphasis to existing mentions of keywords
                        exp = exp.replace(keyword, f"**{keyword}**")
                    
                    experiences[i] = exp
                elif isinstance(exp, dict) and "description" in exp:
                    # Enhance dictionary experience entries
                    desc = exp["description"]
                    for keyword in job_keywords["tech_skills"] + job_keywords["soft_skills"]:
                        if keyword.lower() not in desc.lower():
                            continue
                        # Add emphasis to existing mentions of keywords
                        desc = desc.replace(keyword, f"**{keyword}**")
                    
                    exp["description"] = desc
                    experiences[i] = exp
            
            improved["experience"] = experiences
        
        # Add a summary section if not present
        if "summary" not in improved:
            tech_skills_str = ", ".join(job_keywords["tech_skills"][:3])
            soft_skills_str = ", ".join(job_keywords["soft_skills"][:2])
            
            summary = f"Professional with experience in {tech_skills_str}. "
            summary += f"Skilled in {soft_skills_str} with a focus on delivering high-quality results."
            
            improved["summary"] = summary
        
        return improved
    
    def _generate_improvement_summary(self, original, improved):
        """Generate a summary of improvements made to the resume."""
        improvements = []
        
        # Check for added summary
        if "summary" in improved and "summary" not in original:
            improvements.append("Added professional summary highlighting key skills")
        
        # Check for skill prioritization
        if "skills" in improved and "skills" in original:
            if improved["skills"] != original["skills"]:
                improvements.append("Prioritized relevant skills based on job requirements")
        
        # Check for experience enhancements
        if "experience" in improved and "experience" in original:
            if improved["experience"] != original["experience"]:
                improvements.append("Enhanced experience descriptions to highlight relevant keywords")
        
        # If no specific improvements detected
        if not improvements:
            improvements.append("Formatted resume for better presentation")
            
        return improvements

