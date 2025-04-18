import streamlit as st
import json
from config.config import THEME_COLOR

def render_resume_analysis():
    """Render the resume analysis component."""
    if "resume_data" not in st.session_state or not st.session_state.resume_data:
        st.warning("Please upload and analyze your resume first!")
        return

    try:
        resume_data = json.loads(st.session_state.resume_data) if isinstance(st.session_state.resume_data, str) else st.session_state.resume_data
    except:
        st.error("Failed to parse resume data.")
        return

    st.markdown("### 📄 Resume Analysis")


    # Tabs
    tabs = st.tabs(["Overview", "Sections", "Raw JSON"])
    
    with tabs[0]:  # 
        if "ats_score" in resume_data:
            st.markdown("#### 📈 ATS Score")
            st.progress(resume_data["ats_score"] / 100)
            st.success(f"ATS Score: {resume_data['ats_score']} / 100")

        if "match_recommendations" in resume_data:
            st.markdown("**Recommendations to Improve ATS Match:**")
            for tip in resume_data["match_recommendations"]:
                st.markdown(f"- {tip}")

        # Normalize keys for reliable access
        normalized_resume = {k.lower().replace(" ", "_"): v for k, v in resume_data.items()}
        
        # Fetch personal information (normalize key name)
        personal_info_raw = (
            resume_data.get("personal_info")
            or resume_data.get("personal_information")
            or resume_data.get("Personal Information")
        )

        st.markdown("#### 👤 Personal Information")

        if isinstance(personal_info_raw, dict):
            st.markdown(f"**Name:** {personal_info_raw.get('name', 'N/A')}")
            st.markdown(f"**Email:** {personal_info_raw.get('email', 'N/A')}")
            st.markdown(f"**Phone:** {personal_info_raw.get('phone', 'N/A')}")
            st.markdown(f"**Location:** {personal_info_raw.get('location', 'N/A')}")
            if "linkedin" in personal_info_raw:
                st.markdown(f"**LinkedIn:** {personal_info_raw.get('linkedin')}")
            if "github" in personal_info_raw:
                st.markdown(f"**GitHub:** {personal_info_raw.get('github')}")
        elif isinstance(personal_info_raw, str):
            st.markdown(personal_info_raw)
        else:
            st.markdown("No personal info found.")


        # Summary
        summary = resume_data.get("summary") or resume_data.get("Summary")
        if summary:
            st.markdown("#### 📝 Summary")
            st.markdown(summary)


    with tabs[1]:  # Sections
        for section, content in resume_data.items():
            if section in ["personal_info", "summary", "ats_score", "match_recommendations"]:
                continue

            st.markdown(f"### 📌 {section.replace('_', ' ').title()}")

            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if isinstance(value, list):
                                st.markdown(f"**{key.replace('_', ' ').title()}:**")
                                for val in value:
                                    st.markdown(f"- {val}")
                            else:
                                st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
                        st.markdown("---")  # Divider between items
                    elif isinstance(item, str):
                        st.markdown(f"- {item}")
                    else:
                        st.markdown(str(item))

            elif isinstance(content, dict):
                for k, v in content.items():
                    st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")

            elif isinstance(content, str):
                st.markdown(content)

            else:
                st.write(content)

    with tabs[2]:  # Raw JSON
        st.json(resume_data)
