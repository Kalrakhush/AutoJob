import streamlit as st
from config.config import THEME_COLOR

def show_info_card(title, content, icon="ℹ️"):
    """
    Display an information card with a title and content.
    
    Args:
        title (str): Title of the card
        content (str): Content of the card
        icon (str): Emoji icon for the card
    """
    st.markdown(f"""
    <div style="
        border-left: 4px solid {THEME_COLOR};
        padding: 10px 15px;
        margin: 10px 0;
        background-color: {THEME_COLOR}10;
        border-radius: 5px;
    ">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def show_progress_steps(steps, current_step):
    """
    Display progress steps.
    
    Args:
        steps (list): List of step names
        current_step (int): Current step index (0-based)
    """
    total_steps = len(steps)
    
    # Calculate progress percentage
    progress_percentage = (current_step) / (total_steps - 1)
    
    # Create progress bar
    st.progress(progress_percentage)
    
    # Create columns for each step
    cols = st.columns(total_steps)
    
    for i, step in enumerate(steps):
        with cols[i]:
            if i < current_step:
                # Completed step
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="
                        background-color: {THEME_COLOR};
                        color: white;
                        width: 25px;
                        height: 25px;
                        border-radius: 50%;
                        line-height: 25px;
                        text-align: center;
                        margin: 0 auto;
                    ">✓</div>
                    <p style="font-size: 0.8em; margin-top: 5px; color: {THEME_COLOR};">{step}</p>
                </div>
                """, unsafe_allow_html=True)
            elif i == current_step:
                # Current step
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="
                        border: 2px solid {THEME_COLOR};
                        color: {THEME_COLOR};
                        width: 25px;
                        height: 25px;
                        border-radius: 50%;
                        line-height: 25px;
                        text-align: center;
                        margin: 0 auto;
                        font-weight: bold;
                    ">{i+1}</div>
                    <p style="font-size: 0.8em; margin-top: 5px; font-weight: bold;">{step}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Future step
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="
                        border: 1px solid #ccc;
                        color: #ccc;
                        width: 25px;
                        height: 25px;
                        border-radius: 50%;
                        line-height: 25px;
                        text-align: center;
                        margin: 0 auto;
                    ">{i+1}</div>
                    <p style="font-size: 0.8em; margin-top: 5px; color: #ccc;">{step}</p>
                </div>
                """, unsafe_allow_html=True)