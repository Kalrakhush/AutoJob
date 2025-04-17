import streamlit as st
from config.config import APP_NAME, VERSION, THEME_COLOR

def render_about():
    """Render the about page."""
    st.markdown("## About Us")
    
    st.markdown(f"""
    ### {APP_NAME} - v{VERSION}
    
    {APP_NAME} is an AI-powered job application assistant that helps job seekers optimize their
    resumes and find matching job opportunities. Our platform leverages advanced AI technology
    to provide personalized resume analysis, job matching, and improvement suggestions.
    """)
    
    # How it works
    st.markdown("### Technologies")
    
    st.markdown("""
    Our platform is built using cutting-edge technologies:
    
    - **CrewAI**: For orchestrating multiple AI agents that work together to analyze resumes,
      search for jobs, and provide improvements.
      
    - **Resume Parsing**: Advanced natural language processing to extract and understand the
      components of your resume.
      
    - **Web Search Tools**: Integration with search APIs to find relevant job postings that
      match your skills and experience.
      
    - **Streamlit**: For building an intuitive and responsive user interface.
    """)
    
    # Privacy info
    st.markdown("### Privacy & Data")
    
    st.info("""
    We take your privacy seriously. Your resume data is used only for analysis and job matching
    within this application. We do not store your resume data permanently or share it with third parties.
    
    Your data is processed securely and is not used for training AI models.
    """)
    
    # Contact
    st.markdown("### Contact")
    
    st.markdown(f"""
    If you have any questions or feedback, please contact us:
    
    - Email: contact@{APP_NAME.lower().replace(' ', '')}.com
    - Twitter: @{APP_NAME.lower().replace(' ', '')}
    """)