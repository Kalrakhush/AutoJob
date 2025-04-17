# pages/home.py
import streamlit as st
from config.config import THEME_COLOR, APP_NAME

def render_home(navigate_to):
    """Render the home page with a navigation callback."""
    # Hero section
    st.markdown(f"""
    <div style='text-align:center; padding: 30px 0;'>
        <h1 style='color: {THEME_COLOR};'>{APP_NAME}</h1>
        <p style='font-size: 1.2em;'>Your AI-powered job application assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("## How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. Upload Resume")
        st.markdown("""
        Upload your resume and let our AI analyze your skills, 
        experience, and qualifications to understand your professional profile.
        """)
        if st.button("Upload Resume", key="home_upload_button"):
            navigate_to("Analyze Resume")
    
    with col2:
        st.markdown("### 2. Find Jobs")
        st.markdown("""
        Search for job openings that match your profile. 
        Our AI will scour the web to find the best opportunities based on your skills.
        """)
        if st.button("Search Jobs", key="home_search_button"):
            navigate_to("Search Jobs")
    
    with col3:
        st.markdown("### 3. Improve Resume")
        st.markdown("""
        Get personalized suggestions to improve your resume
        and make it stand out to employers and applicant tracking systems.
        """)
        if st.button("Improve Resume", key="home_improve_button"):
            navigate_to("Improve Resume")
    
    # Benefits section
    st.markdown("## Benefits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        ✅ **Save Time**: Automate job searching and resume tailoring
        
        ✅ **AI-Powered Analysis**: Get expert insights on your resume
        
        ✅ **Personalized Recommendations**: Receive specific suggestions
        """)
    
    with col2:
        st.info("""
        ✅ **Targeted Job Matching**: Find jobs that match your skills
        
        ✅ **ATS Optimization**: Make your resume ATS-friendly
        
        ✅ **Stand Out**: Increase your chances of getting interviews
        """)
    
    # Call to action
    st.markdown("""
    <div style='text-align:center; padding: 30px 0;'>
        <h2>Ready to boost your job search?</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Get Started Now", type="primary", use_container_width=True):
            navigate_to("Analyze Resume")