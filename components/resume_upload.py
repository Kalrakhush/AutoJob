import streamlit as st
import os
import tempfile
from config.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from utils.file_handlers import save_uploaded_file
from tools.resume_parser import ResumeParseTool

def render_resume_upload():
    """Render the resume upload component."""
    st.markdown("### Upload Your Resume")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF, DOCX, or TXT)",
            type=ALLOWED_EXTENSIONS,
            key="resume_uploader"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if uploaded_file is not None:
            if uploaded_file.size > MAX_FILE_SIZE:
                st.error(f"File size exceeds the maximum limit of {MAX_FILE_SIZE/1024/1024}MB")
            else:
                # Save the file
                file_path = save_uploaded_file(uploaded_file)
                
                # Parse the resume
                if st.button("Analyze Resume", type="primary"):
                    with st.spinner("Analyzing your resume..."):
                        resume_parser = ResumeParseTool()
                        result = resume_parser._run({"resume_path": file_path})
                        
                        # Store in session state
                        st.session_state.resume_path = file_path
                        st.session_state.resume_data = result
                        
                        # Success message
                        st.success("Resume analyzed successfully!")
                        
                        # Force a rerun to update the UI
                        st.rerun()