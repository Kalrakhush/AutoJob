import streamlit as st
from config.config import APP_NAME, THEME_COLOR

def render_sidebar():
    """Render the sidebar navigation and return the selected page."""
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center;'>
            <h2 style='color: {THEME_COLOR};'>{APP_NAME}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.divider()
        
        # Navigation
        selected = st.radio(
            "Navigate",
            options=["Home", "Analyze Resume", "Search Jobs", "Improve Resume", "About"],
            index=0,
            key="sidebar_navigation"
        )
        
        st.sidebar.divider()
        
        # User guide
        with st.sidebar.expander("How to use"):
            st.markdown("""
            1. **Upload your resume** on the Analyze Resume page
            2. **View the analysis** of your skills and experience
            3. **Search for jobs** matching your profile
            4. **Get suggestions** to improve your resume
            """)
        
        # Display current status if resume is uploaded
        if "resume_path" in st.session_state and st.session_state.resume_path:
            with st.sidebar.container():
                st.success("✅ Resume uploaded")
                filename = st.session_state.resume_path.split("/")[-1]
                st.caption(f"Current file: {filename}")
                
                if st.button("Clear resume", key="clear_resume"):
                    st.session_state.resume_path = None
                    st.session_state.resume_data = None
                    st.session_state.resume_analysis = None
                    st.session_state.job_search_results = None
                    st.session_state.improved_resume = None
                    st.rerun()
    
    return selected