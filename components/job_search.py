import streamlit as st
from config.config import DEFAULT_LOCATION, SESSION_LOCATION, SESSION_JOB_TITLE
from services.crew_service import execute_job_search
import json

def render_job_search():
    """Render the job search component."""
    st.markdown("### Find Matching Jobs")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        job_title = st.text_input(
            "Job Title/Keywords",
            value=st.session_state.get(SESSION_JOB_TITLE, ""),
            key="job_title_input"
        )
    
    with col2:
        location = st.text_input(
            "Location",
            value=st.session_state.get(SESSION_LOCATION, DEFAULT_LOCATION),
            key="location_input"
        )
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("Search Jobs", type="primary", use_container_width=True)
    
    # Store values in session state
    st.session_state[SESSION_JOB_TITLE] = job_title
    st.session_state[SESSION_LOCATION] = location
    
    # Execute search if button clicked
    if search_button:
        if not st.session_state.get("resume_data"):
            st.warning("Please upload and analyze your resume first!")
            return
        
        with st.spinner("Searching for jobs..."):
            # Call the job search function from crew service
            job_results = execute_job_search(
                resume_data=st.session_state.resume_data,
                job_title=job_title,
                location=location
            )
            
            # Store results in session state
            st.session_state.job_search_results = job_results
            
            # Success message
            st.success("Job search completed!")
            
            # Force a rerun to update the UI
            st.rerun()

def render_job_results():
    """Render the job search results."""
    if "job_search_results" not in st.session_state or not st.session_state.job_search_results:
        return
    
    job_results = st.session_state.job_search_results
    
    st.markdown("### Job Recommendations")
    
    # Try to parse job results if it's a string
    if isinstance(job_results, str):
        try:
            job_results = json.loads(job_results)
        except:
            # If not valid JSON, display as is
            st.markdown(job_results)
            return
    
    # Display job results
    if isinstance(job_results, list):
        for i, job in enumerate(job_results):
            with st.expander(f"{i+1}. {job.get('title', 'Job Title')} - {job.get('company', 'Company')}"):
                st.markdown(f"**Location:** {job.get('location', 'Not specified')}")
                st.markdown(f"**Salary:** {job.get('salary', 'Not specified')}")
                st.markdown(f"**Posted:** {job.get('posted_date', 'Not specified')}")
                st.markdown("**Description:**")
                st.markdown(job.get('description', 'No description available'))
                
                if 'url' in job and job['url']:
                    st.markdown(f"[Apply Now]({job['url']})")
                
                # Match score
                if 'match_score' in job:
                    match_score = int(float(job['match_score']) * 100)
                    st.progress(match_score / 100)
                    st.caption(f"Match Score: {match_score}%")
    elif isinstance(job_results, dict):
        # Handle case where job results are in a different format
        st.json(job_results)
    else:
        st.markdown(str(job_results))