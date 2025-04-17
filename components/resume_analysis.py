import streamlit as st
import json
from config.config import THEME_COLOR

def render_resume_analysis():
    """Render the resume analysis component."""
    if "resume_data" not in st.session_state or not st.session_state.resume_data:
        st.warning("Please upload and analyze your resume first!")
        return
    
    resume_data = st.session_state.resume_data
    
    # Try to parse the resume data if it's a string
    if isinstance(resume_data, str):
        try:
            resume_data = json.loads(resume_data)
        except:
            # If not valid JSON, just use as is
            pass
    
    # Display basic info
    st.markdown("### Resume Analysis")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Skills", "Experience", "Education"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            if isinstance(resume_data, dict) and 'personal_info' in resume_data:
                personal_info = resume_data.get('personal_info', {})
                st.markdown(f"#### {personal_info.get('name', 'Name not found')}")
                st.markdown(f"📧 {personal_info.get('email', 'Email not found')}")
                st.markdown(f"📱 {personal_info.get('phone', 'Phone not found')}")
                st.markdown(f"📍 {personal_info.get('location', 'Location not found')}")
            else:
                st.markdown("#### Personal Information")
                st.markdown("Unable to extract personal information from resume")
        
        with col2:
            if isinstance(resume_data, dict) and 'summary' in resume_data:
                st.markdown("#### Summary")
                st.markdown(resume_data.get('summary', 'No summary found'))
            else:
                st.markdown("#### Summary")
                st.markdown("Unable to extract summary from resume")
    
    with tab2:
        if isinstance(resume_data, dict) and 'skills' in resume_data:
            skills = resume_data.get('skills', [])
            
            if isinstance(skills, list) and skills:
                st.markdown("#### Key Skills")
                
                # Display skills as tags
                skills_html = ""
                for skill in skills:
                    skills_html += f"""
                    <span style="background-color: {THEME_COLOR}20; 
                                 color: {THEME_COLOR}; 
                                 padding: 3px 10px; 
                                 border-radius: 15px; 
                                 margin: 5px 5px 5px 0px;
                                 display: inline-block;
                                 font-size: 0.9em;">
                        {skill}
                    </span>
                    """
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.info("No skills found in your resume.")
        else:
            st.markdown("#### Skills")
            st.markdown("Unable to extract skills from resume")
    
    with tab3:
        if isinstance(resume_data, dict) and 'experience' in resume_data:
            experiences = resume_data.get('experience', [])
            
            if isinstance(experiences, list) and experiences:
                st.markdown("#### Work Experience")
                
                for exp in experiences:
                    with st.expander(f"{exp.get('title', 'Position')} at {exp.get('company', 'Company')}"):
                        st.markdown(f"**Duration:** {exp.get('duration', 'Not specified')}")
                        st.markdown(f"**Location:** {exp.get('location', 'Not specified')}")
                        st.markdown("**Responsibilities:**")
                        st.markdown(exp.get('description', 'No description available'))
            else:
                st.info("No work experience found in your resume.")
        else:
            st.markdown("#### Experience")
            st.markdown("Unable to extract experience from resume")
    
    with tab4:
        if isinstance(resume_data, dict) and 'education' in resume_data:
            education = resume_data.get('education', [])
            
            if isinstance(education, list) and education:
                st.markdown("#### Education")
                
                for edu in education:
                    st.markdown(f"**{edu.get('degree', 'Degree')}** - {edu.get('institution', 'Institution')}")
                    st.markdown(f"*{edu.get('duration', 'Duration not specified')}*")
                    if 'description' in edu and edu['description']:
                        st.markdown(edu['description'])
                    st.divider()
            else:
                st.info("No education information found in your resume.")
        else:
            st.markdown("#### Education")
            st.markdown("Unable to extract education from resume")