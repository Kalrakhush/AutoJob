import streamlit as st
from config.config import DEFAULT_LOCATION, SESSION_LOCATION, SESSION_JOB_TITLE
from services.crew_service import execute_job_search
import json
import pandas as pd


def render_job_search():
    """Render the job search component."""
    st.markdown("### Find Matching Jobs")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        job_title = st.text_input(
            "Job Title/Keywords",
            value=st.session_state.get(SESSION_JOB_TITLE, ""),
            key="job_title_input"
        )
    with col2:
        location = st.text_input(
            "Location",
            value=st.session_state.get(SESSION_LOCATION, DEFAULT_LOCATION),
            key="location_input"
        )
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.button("Search Jobs", type="primary", use_container_width=True)
    
    # Store inputs in session state
    st.session_state[SESSION_JOB_TITLE] = job_title
    st.session_state[SESSION_LOCATION] = location

    if search_button:
        if not st.session_state.get("resume_data"):
            st.warning("Please upload and analyze your resume first!")
            return

        # Parse resume_data if it's a JSON string
        raw = st.session_state.resume_data
        try:
            resume_payload = json.loads(raw) if isinstance(raw, str) else raw
        except json.JSONDecodeError:
            st.error("Failed to parse your resume data. Please re-upload or re-analyze.")
            return

        with st.spinner("Searching for jobs..."):
            # Pass the parsed JSON to your job search function
            job_results = execute_job_search(
                resume_data=resume_payload,
                job_title=job_title,
                location=location
            )

        # Store and display results
        st.session_state.job_search_results = job_results
        st.success("Job search completed!")
        st.rerun()




def render_job_results():
    """Render job search results dynamically without hardcoding any fields."""
    if "job_search_results" not in st.session_state or not st.session_state.job_search_results:
        return

    raw_results = st.session_state.job_search_results

    
    # Parse string if needed
    if isinstance(raw_results, str):
        try:
            job_results = json.loads(raw_results)
        except json.JSONDecodeError:
            st.warning("Invalid JSON format. Displaying raw text.")
            st.markdown(raw_results)
            return
    else:
        job_results = raw_results
        

    # Ensure it's a list of dicts
    if not isinstance(job_results, list):
        st.warning("Expected a list of job objects.")
        st.json(job_results)
        return

    st.markdown("### 💼 Job Recommendations")

    table_data = []
    for job in job_results:
        row = {}
        for key, value in job.items():
            # Format URLs as clickable links
            if key.lower() == "url" and isinstance(value, str):
                row["Apply Link"] = f'<a href="{value}" target="_blank">Apply Now</a>'
            elif key.lower() == "match_score" and isinstance(value, (int, float)):
                row["Match Score"] = f"{value * 100:.0f}%"
            elif isinstance(value, str):
                row[key.title()] = value.strip()
            else:
                row[key.title()] = value
        table_data.append(row)

    # Create and display table
    df = pd.DataFrame(table_data)

    # Only include preferred columns that exist
    preferred_columns = ["Title", "Company", "Match Score", "Apply Link"]
    available_columns = [col for col in preferred_columns if col in df.columns]
    other_columns = [col for col in df.columns if col not in available_columns]
    df = df[available_columns + other_columns]



    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Expanders for full snippets/descriptions
    with st.expander("📄 View Full Descriptions"):
        for idx, job in enumerate(job_results, 1):
            title = job.get("title", "Job Title")
            company = job.get("company", "Company")
            snippet = job.get("snippet", "No description available")
            match = job.get("match_score", None)
            url = job.get("url", "#")

            st.markdown(f"**{idx}. {title} @ {company}**")
            if match is not None:
                st.markdown(f"**Match Score:** {match * 100:.0f}%")
            st.markdown(f"[Apply Now]({url})")
            st.markdown(f"**Snippet:** {snippet}")
            st.markdown("---")
