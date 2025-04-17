import streamlit as st
from components.resume_improvements import render_resume_improvement, render_improvement_results

def render_improve_resume():
    """Render the improve resume page."""
    st.markdown("## Resume Improvement")
    
    st.markdown("""
    Get personalized suggestions to improve your resume based on your skills,
    experience, and target job positions. Our AI will help you make your resume
    stand out to employers and applicant tracking systems.
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
    
    # Render the resume improvement component
    render_resume_improvement()
    
    # Render improvement results if available
    render_improvement_results()