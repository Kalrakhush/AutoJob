import streamlit as st
from config.config import APP_NAME, THEME_COLOR

def render_header():
    """Render the application header."""
    col1, col2 = st.columns([1, 4])
    
    with col1:
        st.image("assets/images/logo.png", width=100)
    
    with col2:
        st.markdown(f"""
        <h1 style='color: {THEME_COLOR};'>{APP_NAME}</h1>
        <p>Your AI-powered job application assistant</p>
        """, unsafe_allow_html=True)
    
    st.divider()