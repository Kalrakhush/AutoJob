import os
import tempfile
import streamlit as st
import uuid

def save_uploaded_file(uploaded_file):
    """
    Save an uploaded file to a temporary directory and return the path.
    
    Args:
        uploaded_file (UploadedFile): The uploaded file from Streamlit
        
    Returns:
        str: Path to the saved file
    """
    # Create a temporary directory if it doesn't exist
    temp_dir = os.path.join(tempfile.gettempdir(), "resume_uploads")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Generate a unique filename
    file_extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(temp_dir, unique_filename)
    
    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def get_file_content(file_path):
    """
    Read and return the content of a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Content of the file
    """
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    return content