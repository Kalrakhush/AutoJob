# ui/components/resume_upload.py
import streamlit as st
import os
import tempfile

def render_resume_upload():
    """Render the resume upload component."""
    st.subheader("Upload Your Resume")
    
    uploaded_file = st.file_uploader("Choose your resume file", type=["pdf", "docx", "txt", "json"])
    
    if uploaded_file is not None:
        # Save uploaded file to temp location
        temp_dir = tempfile.gettempdir()
        resume_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(resume_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Resume uploaded: {uploaded_file.name}")
        return resume_path
    
    return None

# ui/components/job_selector.py
import streamlit as st

def render_job_selector(jobs):
    """Render the job selection component."""
    st.subheader("Select Jobs to Apply For")
    
    selected_jobs = []
    
    if not jobs:
        st.warning("No jobs available to select.")
        return selected_jobs
    
    for i, job in enumerate(jobs):
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
            if st.checkbox("Select this job", key=f"select_job_{i}"):
                selected_jobs.append(job)
    
    return selected_jobs

# ui/components/confirmation.py
import streamlit as st

def render_confirmation(job_applications):
    """Render the confirmation component."""
    st.subheader("Application Confirmation")
    
    if not job_applications:
        st.warning("No job applications to confirm.")
        return False
    
    st.write(f"You are about to apply to {len(job_applications)} jobs:")
    
    for i, app in enumerate(job_applications):
        job = app.get("job", {})
        st.write(f"{i+1}. {job.get('title', 'Job')} at {job.get('company', 'Company')}")
    
    # Add confirmation checkbox
    confirm = st.checkbox("I confirm that I want to submit these applications")
    
    if confirm:
        if st.button("Submit Applications"):
            return True
    
    return False