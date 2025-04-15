# ui/app.py
import streamlit as st
import sys
import os
import json
from pathlib import Path
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import JobApplicationBot

def main():
    st.set_page_config(page_title="Job Application Agent", page_icon="📄", layout="wide")
    
    st.title("🤖 AI Job Application Agent")
    st.subheader("Upload your resume, find jobs, and apply automatically")
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    
    if 'resume_path' not in st.session_state:
        st.session_state.resume_path = None
        
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = None
        
    if 'job_listings' not in st.session_state:
        st.session_state.job_listings = None
        
    if 'improved_resumes' not in st.session_state:
        st.session_state.improved_resumes = None
        
    if 'selected_jobs' not in st.session_state:
        st.session_state.selected_jobs = []
        
    if 'application_results' not in st.session_state:
        st.session_state.application_results = None
    
    # Create tabs for the workflow
    tab1, tab2, tab3, tab4 = st.tabs(["1. Upload Resume", "2. Find Jobs", "3. Improve Resume", "4. Apply"])
    
    with tab1:
        # Step 1: Upload Resume
        st.header("Upload Your Resume")
        
        upload_col, preview_col = st.columns([1, 1])
        
        with upload_col:
            uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "docx", "txt", "json"])
            
            if uploaded_file is not None:
                # Save uploaded file to temp location
                temp_dir = tempfile.gettempdir()
                resume_path = os.path.join(temp_dir, uploaded_file.name)
                
                with open(resume_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.session_state.resume_path = resume_path
                st.success(f"Resume uploaded: {uploaded_file.name}")
                
                # User information form
                st.subheader("Personal Information")
                with st.form("user_info_form"):
                    name = st.text_input("Full Name")
                    email = st.text_input("Email")
                    phone = st.text_input("Phone Number")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        location = st.text_input("Location")
                    with col2:
                        linkedin = st.text_input("LinkedIn URL (optional)")
                        
                    submit_button = st.form_submit_button("Save Information")
                    
                    if submit_button:
                        st.session_state.user_info = {
                            "name": name,
                            "email": email,
                            "phone": phone,
                            "location": location,
                            "linkedin": linkedin
                        }
                        
                        # Save user info to file
                        user_info_path = os.path.join(temp_dir, "user_info.json")
                        with open(user_info_path, "w") as f:
                            json.dump(st.session_state.user_info, f)
                            
                        st.session_state.user_info_path = user_info_path
                        st.success("Personal information saved!")
                
                if st.button("Analyze Resume", key="analyze_resume"):
                    with st.spinner("Analyzing resume..."):
                        # Create job application bot
                        bot = JobApplicationBot()
                        
                        # Only run resume analysis
                        st.session_state.resume_analyzer = bot.resume_analyzer
                        
                        # Use the tool directly instead of through the crew
                        from tools.resume_parser import ResumeParseTool
                        tool = ResumeParseTool()
                        result = tool._run(resume_path=resume_path)
                        
                        st.session_state.resume_data = result
                        st.session_state.step = 2
                        st.experimental_rerun()
        
        with preview_col:
            if st.session_state.resume_data is not None:
                st.subheader("Resume Analysis")
                
                # Contact info
                if "contact_info" in st.session_state.resume_data:
                    st.write("📞 **Contact Information**")
                    contact_info = st.session_state.resume_data["contact_info"]
                    for key, value in contact_info.items():
                        st.write(f"- {key.title()}: {value}")
                
                # Education
                if "education" in st.session_state.resume_data:
                    st.write("🎓 **Education**")
                    for edu in st.session_state.resume_data["education"]:
                        st.write(f"- {edu}")
                
                # Display truncated experience
                if "experience" in st.session_state.resume_data:
                    st.write("💼 **Experience**")
                    experiences = st.session_state.resume_data["experience"]
                    for i, exp in enumerate(experiences):
                        if i < 3:  # Show only first 3 experiences
                            if isinstance(exp, dict) and "description" in exp:
                                st.write(f"- {exp.get('title', 'Role')}: {exp.get('description', '')[:100]}...")
                            else:
                                st.write(f"- {exp[:100]}...")
                    
                    if len(experiences) > 3:
                        st.write(f"...and {len(experiences) - 3} more experiences")
                
                # Skills
                if "skills" in st.session_state.resume_data:
                    st.write("🔧 **Skills**")
                    skills = st.session_state.resume_data["skills"]
                    st.write(", ".join(skills[:10]))
                    if len(skills) > 10:
                        st.write(f"...and {len(skills) - 10} more skills")
    
    with tab2:
        # Step 2: Job Search
        st.header("Find Matching Jobs")
        
        search_col, results_col = st.columns([1, 2])
        
        with search_col:
            with st.form("job_search_form"):
                job_keywords = st.text_input("Job Keywords", 
                                          placeholder="e.g., Python Developer, Data Scientist")
                
                location = st.text_input("Location", 
                                      placeholder="e.g., Remote, New York, San Francisco")
                
                experience_level = st.selectbox("Experience Level",
                                             ["Any", "Entry", "Mid", "Senior"])
                
                search_button = st.form_submit_button("Search Jobs")
                
                if search_button:
                    with st.spinner("Searching for matching jobs..."):
                        # Create job application bot
                        bot = JobApplicationBot()
                        
                        # Only run job search
                        st.session_state.job_searcher = bot.job_searcher
                        
                        # Use the tool directly
                        from tools.web_search import WebSearchTool
                        tool = WebSearchTool()
                        
                        # Prepare experience level
                        exp = None if experience_level == "Any" else experience_level.lower()
                        
                        # Run search
                        result = tool._run(
                            query=job_keywords,
                            location=location if location else None,
                            experience_level=exp
                        )
                        
                        st.session_state.job_listings = result
                        st.session_state.step = 3
                        st.experimental_rerun()
        
        with results_col:
            if st.session_state.job_listings is not None:
                st.subheader("Matching Jobs")
                
                if isinstance(st.session_state.job_listings, list) and len(st.session_state.job_listings) > 0:
                    for i, job in enumerate(st.session_state.job_listings):
                        with st.expander(f"{job.get('title', 'Job')} at {job.get('company', 'Company')}"):
                            st.write(f"🏢 **Company:** {job.get('company', 'N/A')}")
                            st.write(f"📍 **Location:** {job.get('location', 'N/A')}")
                            st.write(f"💰 **Salary Range:** {job.get('salary_range', 'N/A')}")
                            st.write(f"📅 **Posted:** {job.get('posted_date', 'N/A')}")
                            st.write(f"🔗 **URL:** {job.get('url', 'N/A')}")
                            st.write("📝 **Description:**")
                            st.write(job.get('description', 'No description available'))
                            
                            if "requirements" in job:
                                st.write("✅ **Requirements:**")
                                for req in job["requirements"]:
                                    st.write(f"- {req}")
                            
                            # Add checkbox to select jobs
                            job_key = f"{job.get('company', 'Company')}_{job.get('title', 'Job')}"
                            if st.checkbox("Select this job", key=f"select_job_{i}"):
                                if job not in st.session_state.selected_jobs:
                                    st.session_state.selected_jobs.append(job)
                            else:
                                if job in st.session_state.selected_jobs:
                                    st.session_state.selected_jobs.remove(job)
                    
                    # Show button to proceed
                    if len(st.session_state.selected_jobs) > 0:
                        if st.button("Improve Resume for Selected Jobs", key="improve_resume_button"):
                            st.session_state.step = 3
                            st.experimental_rerun()
                else:
                    st.warning("No jobs found matching your criteria. Try different keywords or location.")
    
    with tab3:
        # Step 3: Resume Improvement
        st.header("Improve Your Resume")
        
        # Only show content if jobs are selected
        if len(st.session_state.selected_jobs) > 0:
            if st.session_state.improved_resumes is None:
                with st.spinner("Tailoring your resume for selected jobs..."):
                    # Create job application bot
                    bot = JobApplicationBot()
                    
                    # Only run resume improver
                    st.session_state.resume_improver = bot.resume_improver
                    
                    # Use the tool directly
                    from tools.resume_formatter import ResumeFormatterTool
                    tool = ResumeFormatterTool()
                    
                    # Process each selected job
                    improved_resumes = []
                    for job in st.session_state.selected_jobs:
                        job_desc = job.get("description", "") + " " + " ".join(job.get("requirements", []))
                        result = tool._run(
                            resume_data=st.session_state.resume_data,
                            job_description=job_desc
                        )
                        
                        # Add job info to result
                        result["job"] = job
                        improved_resumes.append(result)
                    
                    st.session_state.improved_resumes = improved_resumes
                    st.session_state.step = 4
                    st.experimental_rerun()
            
            # Display improved resumes
            if st.session_state.improved_resumes is not None:
                for i, improved in enumerate(st.session_state.improved_resumes):
                    job = improved.get("job", {})
                    
                    with st.expander(f"Resume for: {job.get('title', 'Job')} at {job.get('company', 'Company')}"):
                        st.subheader("Improvements Made")
                        
                        if "improvements" in improved:
                            for imp in improved["improvements"]:
                                st.write(f"✅ {imp}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("**Original Resume**")
                            if "original_resume" in improved:
                                original = improved["original_resume"]
                                
                                # Display skills
                                if "skills" in original:
                                    st.write("🔧 **Skills**")
                                    st.write(", ".join(original["skills"][:10]))
                                
                                # Display experience
                                if "experience" in original:
                                    st.write("💼 **Experience**")
                                    for exp in original["experience"][:2]:
                                        if isinstance(exp, dict):
                                            st.write(f"- {exp.get('title', '')}: {exp.get('description', '')[:100]}...")
                                        else:
                                            st.write(f"- {exp[:100]}...")
                        
                        with col2:
                            st.write("**Improved Resume**")
                            if "improved_resume" in improved:
                                optimized = improved["improved_resume"]
                                
                                # Display summary if added
                                if "summary" in optimized:
                                    st.write("📝 **Summary**")
                                    st.write(optimized["summary"])
                                
                                # Display skills
                                if "skills" in optimized:
                                    st.write("🔧 **Skills**")
                                    st.write(", ".join(optimized["skills"][:10]))
                                
                                # Display experience
                                if "experience" in optimized:
                                    st.write("💼 **Experience**")
                                    for exp in optimized["experience"][:2]:
                                        if isinstance(exp, dict):
                                            st.write(f"- {exp.get('title', '')}: {exp.get('description', '')[:100]}...")
                                        else:
                                            st.write(f"- {exp[:100]}...")
                        
                        # Approval checkbox
                        job["approved"] = st.checkbox("Approve this resume", key=f"approve_resume_{i}", value=True)
                
                # Button to proceed to applications
                if st.button("Proceed to Application", key="proceed_to_application"):
                    st.session_state.step = 4
                    st.experimental_rerun()
        else:
            st.info("Please select jobs in step 2 before proceeding to resume improvement.")
    
    with tab4:
        # Step 4: Apply for Jobs
        st.header("Apply for Jobs")
        
        # Show only approved jobs
        approved_jobs = []
        if st.session_state.improved_resumes is not None:
            for improved in st.session_state.improved_resumes:
                job = improved.get("job", {})
                if job.get("approved", False):
                    approved_jobs.append({
                        "job": job,
                        "improved_resume": improved.get("improved_resume")
                    })
        
        if len(approved_jobs) > 0:
            st.write(f"Ready to apply for {len(approved_jobs)} jobs:")
            
            for i, item in enumerate(approved_jobs):
                job = item["job"]
                st.write(f"{i+1}. {job.get('title', 'Job')} at {job.get('company', 'Company')}")
            
            # Check if user info is available
            if hasattr(st.session_state, 'user_info') and st.session_state.user_info:
                if st.button("Submit Applications", key="submit_applications"):
                    with st.spinner("Submitting job applications..."):
                        # Create job application bot
                        bot = JobApplicationBot()
                        
                        # Only run job applicator
                        st.session_state.job_applicator = bot.job_applicator
                        
                        # Use the tool directly
                        from tools.job_submission import JobSubmissionTool
                        tool = JobSubmissionTool()
                        
                        # Process each approved job
                        application_results = []
                        for item in approved_jobs:
                            job = item["job"]
                            
                            # Save improved resume to file
                            temp_dir = tempfile.gettempdir()
                            company_name = job.get("company", "Company").replace(" ", "_")
                            job_title = job.get("title", "Job").replace(" ", "_")
                            resume_filename = f"resume_{company_name}_{job_title}.json"
                            resume_path = os.path.join(temp_dir, resume_filename)
                            
                            with open(resume_path, "w") as f:
                                json.dump(item["improved_resume"], f)
                            
                            # Apply for job
                            result = tool._run(
                                job_url=job.get("url", ""),
                                resume_path=resume_path,
                                user_info=st.session_state.user_info
                            )
                            
                            application_results.append(result)
                        
                        st.session_state.application_results = application_results
                        st.experimental_rerun()
                        
            else:
                st.warning("Please provide your personal information in Step 1 before submitting applications.")
        
        # Display application results
        if st.session_state.application_results is not None:
            st.subheader("Application Results")
            
            for i, result in enumerate(st.session_state.application_results):
                status = result.get("status", "Unknown")
                
                if status == "success":
                    st.success(f"✅ Application {i+1}: Successfully submitted")
                    st.write(f"📝 **ID:** {result.get('application_id', 'N/A')}")
                    st.write(f"🏢 **Platform:** {result.get('platform', 'N/A')}")
                    st.write(f"⏰ **Time:** {result.get('submission_time', 'N/A')}")
                    st.write(f"🔗 **Job URL:** {result.get('job_url', 'N/A')}")
                else:
                    st.error(f"❌ Application {i+1}: Failed")
                    st.write(f"❓ **Reason:** {result.get('error', 'Unknown error')}")
        
        else:
            if len(approved_jobs) == 0:
                st.info("Please approve job-specific resumes in Step 3 before proceeding to application.")

if __name__ == "__main__":
    main()