# app.py
import streamlit as st
from page._home import render_home
from page._analyze_resume import render_analyze_resume
from page._search_jobs import render_search_jobs
from page._improve_resume import render_improve_resume
from config.config import THEME_COLOR, APP_NAME

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if "navigation" not in st.session_state:
        st.session_state.navigation = "Home"
    
    # Other session state initializations if needed
    if "resume_data" not in st.session_state:
        st.session_state.resume_data = None
    if "job_results" not in st.session_state:
        st.session_state.job_results = []

def navigation_sidebar():
    """Create the navigation sidebar."""
    with st.sidebar:
        st.title(APP_NAME)
        st.markdown(f"<hr style='border: 2px solid {THEME_COLOR};'>", unsafe_allow_html=True)
        
        # Navigation options
        pages = {
            "Home": "🏠",
            "Analyze Resume": "📄",
            "Search Jobs": "🔍",
            "Improve Resume": "⭐",
            "Settings": "⚙️"
        }
        
        selected_page = None
        
        # Create navigation buttons
        for page, icon in pages.items():
            if st.sidebar.button(
                f"{icon} {page}", 
                key=f"nav_{page}", 
                use_container_width=True,
                type="primary" if st.session_state.navigation == page else "secondary"
            ):
                selected_page = page
        
        # If a navigation button was clicked, update the state
        if selected_page:
            st.session_state.navigation = selected_page
            st.rerun()

def navigate_to(page):
    """Update navigation state and trigger rerun."""
    st.session_state.navigation = page
    st.rerun()

def main():
    """Main function to run the Streamlit app."""
    # Page config
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state variables
    initialize_session_state()
    
    # Show sidebar navigation
    navigation_sidebar()
    
    # Render the selected page
    if st.session_state.navigation == "Home":
        render_home(navigate_to)
    elif st.session_state.navigation == "Analyze Resume":
        render_analyze_resume()
    elif st.session_state.navigation == "Search Jobs":
        render_search_jobs()
    elif st.session_state.navigation == "Improve Resume":
        render_improve_resume()
    elif st.session_state.navigation == "Settings":
        render_settings()

def render_settings():
    """Render the settings page."""
    st.title("Settings")
    st.write("Configure your application settings here.")
    # Add settings options as needed

if __name__ == "__main__":
    main()