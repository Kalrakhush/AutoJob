import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application settings
APP_NAME = "CareerBoost AI"
VERSION = "1.0.0"
THEME_COLOR = "#4F8BF9"

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# File upload settings
ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Session state keys
SESSION_RESUME_DATA = "resume_data"
SESSION_RESUME_PATH = "resume_path"
SESSION_RESUME_ANALYSIS = "resume_analysis"
SESSION_JOB_SEARCH = "job_search_results"
SESSION_IMPROVED_RESUME = "improved_resume"
SESSION_LOCATION = "location"
SESSION_JOB_TITLE = "job_title"

# Default values
DEFAULT_LOCATION = "Remote"