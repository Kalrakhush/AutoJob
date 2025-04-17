import streamlit as st
from components.job_search import render_job_search, render_job_results

def render_search_jobs():
    """Render the search jobs page."""
    st.markdown("## Job Search")
    
    st.markdown("""
    Search for jobs that match your skills and experience. Our AI will analyze your resume
    and find the best opportunities that align with your profile.
    """)
    
    # Check if resume is uploaded
    if "resume_data" not in st.session_state or not st.session_state.resume_data:
        st.warning("Please upload and analyze your resume first!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Go to Resume Upload", type="primary", use_container_width=True):
                st.session_state["sidebar_navigation"] = "Analyze Resume"
                st.rerun()
        return
    
    # Render the job search component
    render_job_search()
    
    # Render job results if available
    render_job_results()
    
    # Add next step button if job results exist
    if "job_search_results" in st.session_state and st.session_state.job_search_results:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next: Improve Your Resume", type="primary", use_container_width=True):
                st.session_state["sidebar_navigation"] = "Improve Resume"
                st.rerun()