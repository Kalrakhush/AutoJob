import streamlit as st
from components.resume_upload import render_resume_upload
from components.resume_analysis import render_resume_analysis

def render_analyze_resume():
    """Render the analyze resume page."""
    st.markdown("## Resume Analysis")
    
    st.markdown("""
    Upload your resume to get a detailed analysis of your skills, experience, and qualifications.
    This will help you understand how your resume is perceived by employers and applicant tracking systems.
    """)
    
    # Render the resume upload component
    render_resume_upload()
    
    # Render the resume analysis if resume is uploaded
    if "resume_data" in st.session_state and st.session_state.resume_data:
        render_resume_analysis()
        
        # Add next step button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next: Search for Jobs", type="primary", use_container_width=True):
                st.session_state["sidebar_navigation"] = "Search Jobs"
                st.rerun()