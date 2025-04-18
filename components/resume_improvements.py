import streamlit as st
import json
from services.crew_service import execute_resume_improvement

def render_resume_improvement():
    """Render the resume improvement component."""
    st.markdown("### Improve Your Resume")
    
    # Check if resume data exists
    if "resume_data" not in st.session_state or not st.session_state.resume_data:
        st.warning("Please upload and analyze your resume first!")
        return
    
    # Check if job search results exist
    if "job_search_results" not in st.session_state or not st.session_state.job_search_results:
        st.warning("Please search for jobs first to get targeted resume improvements!")
        improve_button_disabled = True
    else:
        improve_button_disabled = False
    
    if st.button("Generate Resume Improvements", 
                 disabled=improve_button_disabled,
                 type="primary"):
        with st.spinner("Analyzing your resume and generating improvements..."):
            # Call the resume improvement function from crew service
            improvements = execute_resume_improvement(
                resume_data=st.session_state.resume_data,
                job_results=st.session_state.get("job_search_results", None),
                job_title=st.session_state.get("job_title", ""),
                location=st.session_state.get("location", "")
            )
            
            # Store improvements in session state
            st.session_state.improved_resume = improvements
            
            # Success message
            st.success("Resume improvements generated!")
            
            # Force a rerun to update the UI
            st.rerun()

def render_improvement_results():
    """Render the resume improvement results."""
    if "improved_resume" not in st.session_state or not st.session_state.improved_resume:
        return

    improvements = st.session_state.improved_resume
    print(f"[DEBUG] improvements type: {type(improvements)}")

    # ✅ Always unwrap CrewOutput if present
    if hasattr(improvements, 'output'):
        improvements = improvements.output

    st.markdown("### Resume Improvement Suggestions")

    # ✅ Try to parse if it's a JSON string
    if isinstance(improvements, str):
        try:
            improvements = json.loads(improvements)
        except json.JSONDecodeError:
            tab1, tab2 = st.tabs(["Suggestions", "Raw Output"])
            with tab1:
                st.markdown(improvements)
            with tab2:
                st.code(improvements)
            return

    # ✅ Structured display
    if isinstance(improvements, dict):
        tab1, tab2, tab3 = st.tabs(["Summary", "Detailed Suggestions", "Improved Content"])

        with tab1:
            st.markdown("#### Summary of Improvements")
            st.markdown(improvements.get('summary', 'No summary available'))
            if 'improvement_areas' in improvements:
                st.markdown("#### Key Improvement Areas")
                for area in improvements['improvement_areas']:
                    st.markdown(f"- {area}")

        with tab2:
            st.markdown("#### Detailed Suggestions")
            sections = ['summary', 'skills', 'experience', 'education', 'formatting']
            for section in sections:
                section_key = f'{section}_suggestions'
                if section_key in improvements:
                    with st.expander(f"{section.capitalize()} Suggestions"):
                        if isinstance(improvements[section_key], list):
                            for suggestion in improvements[section_key]:
                                st.markdown(f"- {suggestion}")
                        else:
                            st.markdown(improvements[section_key])

        with tab3:
            st.markdown("#### Improved Content")
            sections = ['improved_summary', 'improved_skills', 'improved_experience', 'improved_education']
            for section in sections:
                if section in improvements:
                    with st.expander(f"{section.replace('improved_', '').capitalize()}"):
                        st.markdown(improvements[section])

            if 'improved_resume_full' in improvements:
                st.download_button(
                    label="Download Improved Resume",
                    data=improvements['improved_resume_full'],
                    file_name="improved_resume.md",
                    mime="text/markdown"
                )

        # ✅ Optional Markdown download of all dict content
        def dict_to_markdown(data, level=2):
            md = ""
            for key, value in data.items():
                header = f"{'#' * level} {key.replace('_', ' ').capitalize()}\n\n"
                if isinstance(value, dict):
                    md += header + dict_to_markdown(value, level + 1)
                elif isinstance(value, list):
                    md += header + "\n".join([f"- {str(item)}" for item in value]) + "\n\n"
                else:
                    md += header + f"{value}\n\n"
            return md

        markdown_output = dict_to_markdown(improvements)
        st.download_button(
            label="Download All as Markdown",
            data=markdown_output,
            file_name="resume_improvements_full.md",
            mime="text/markdown"
        )

    # else:
    #     st.markdown(str(improvements))
