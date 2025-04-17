import streamlit as st
from config.config import VERSION

def render_footer():
    """Render the application footer."""
    st.divider()
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown("""
        <div style='text-align: center;'>
            <p>Made with ❤️ using CrewAI and Streamlit</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='text-align: right;'>
            <p>v{VERSION}</p>
        </div>
        """, unsafe_allow_html=True)