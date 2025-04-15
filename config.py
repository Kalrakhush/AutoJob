import os
from pathlib import Path

# API Keys
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "your-gemini-api-key")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key")
SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY", "your-serpapi-api-key")

# File paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "user_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Web search settings
JOB_SEARCH_SITES = [
    "linkedin.com/jobs",
    "indeed.com",
    "glassdoor.com"
]

# Application settings
MAX_JOBS_TO_SEARCH = 10
RESUME_SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score to consider a job match