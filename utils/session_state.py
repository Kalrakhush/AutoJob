import streamlit as st
from config.config import (
    SESSION_RESUME_DATA,
    SESSION_RESUME_PATH,
    SESSION_RESUME_ANALYSIS,
    SESSION_JOB_SEARCH,
    SESSION_IMPROVED_RESUME,
    SESSION_LOCATION,
    SESSION_JOB_TITLE,
    DEFAULT_LOCATION
)

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if SESSION_RESUME_DATA not in st.session_state:
        st.session_state[SESSION_RESUME_DATA] = None
    
    if SESSION_RESUME_PATH not in st.session_state:
        st.session_state[SESSION_RESUME_PATH] = None
    
    if SESSION_RESUME_ANALYSIS not in st.session_state:
        st.session_state[SESSION_RESUME_ANALYSIS] = None
    
    if SESSION_JOB_SEARCH not in st.session_state:
        st.session_state[SESSION_JOB_SEARCH] = None
    
    if SESSION_IMPROVED_RESUME not in st.session_state:
        st.session_state[SESSION_IMPROVED_RESUME] = None
    
    if SESSION_LOCATION not in st.session_state:
        st.session_state[SESSION_LOCATION] = DEFAULT_LOCATION
    
    if SESSION_JOB_TITLE not in st.session_state:
        st.session_state[SESSION_JOB_TITLE] = ""