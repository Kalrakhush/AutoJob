# Job Application Agent

A CrewAI-powered automated job application system that analyzes resumes, searches for matching jobs, improves resumes for specific positions, and handles job applications.

## Features

- **Resume Analysis**: Parse and extract structured information from resume documents
- **Job Search**: Find relevant job postings based on skills and preferences
- **Resume Tailoring**: Optimize resumes for specific job descriptions
- **Application Submission**: Automate the job application process
- **User-Friendly UI**: Streamlit-based interface for easy interaction

## Project Structure

```
job_application_agent/
│
├── main.py                # Entry point for the application
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
│
├── agents/
│   ├── __init__.py
│   ├── definitions/       # YAML definitions for agents
│   │   ├── resume_analyzer.yaml
│   │   ├── job_searcher.yaml
│   │   ├── resume_improver.yaml
│   │   └── job_applicator.yaml
│   ├── resume_analyzer.py # Agent implementation
│   ├── job_searcher.py    # Agent implementation
│   ├── resume_improver.py # Agent implementation
│   └── job_applicator.py  # Agent implementation
│
├── tools/
│   ├── __init__.py
│   ├── definitions/       # YAML definitions for tools
│   │   ├── resume_parser.yaml
│   │   ├── web_search.yaml
│   │   ├── resume_formatter.yaml
│   │   └── job_submission.yaml
│   ├── resume_parser.py   # Tool implementation
│   ├── web_search.py      # Tool implementation
│   ├── resume_formatter.py # Tool implementation
│   └── job_submission.py  # Tool implementation
│
├── ui/
│   ├── __init__.py
│   ├── app.py             # Streamlit application
│   └── components/
│       ├── __init__.py
│       ├── resume_upload.py
│       ├── job_selector.py
│       └── confirmation.py
│
└── data/
    └── user_data/         # Directory to store user resumes and job info
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/job-application-agent.git
cd job-application-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Run the application from the command line:

```bash
python main.py --resume path/to/resume.pdf --keywords "python developer" --location "San Francisco" --experience senior --user-info path/to/user_info.json
```

Arguments:
- `--resume`: Path to your resume file (required)
- `--keywords`: Job keywords to search for
- `--location`: Job location preference
- `--experience`: Experience level (entry, mid, senior)
- `--user-info`: Path to JSON file with user information

Example user_info.json:
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "location": "San Francisco, CA",
    "linkedin": "https://linkedin.com/in/johndoe"
}
```

### Web Interface

Start the Streamlit web interface:

```bash
streamlit run ui/app.py
```

Then follow the steps in the web interface:
1. Upload your resume
2. Search for jobs
3. Improve your resume for selected jobs
4. Submit applications

## How It Works

The application uses CrewAI to orchestrate a team of agents:

1. **Resume Analyzer Agent**: Parses your resume to extract skills, experiences, and qualifications.
2. **Job Searcher Agent**: Finds job postings that match your skills and preferences.
3. **Resume Improver Agent**: Tailors your resume to better match each job description.
4. **Job Applicator Agent**: Submits applications to the selected jobs.

Each agent uses specialized tools to perform its tasks, and the agents work together in a sequential process to complete the job application workflow.

## Configuration

You can customize the application behavior by modifying the YAML definition files for agents and tools:

- Agent definitions: `agents/definitions/*.yaml`
- Tool definitions: `tools/definitions/*.yaml`

## Extension Points

To extend the system with additional functionality:

1. Add new tools in the `tools/` directory
2. Create YAML definitions for new tools in `tools/definitions/`
3. Implement new agents in the `agents/` directory
4. Create YAML definitions for new agents in `agents/definitions/`
5. Update the main application to incorporate the new components

## Dependencies

- crewai: Agent orchestration framework
- streamlit: Web interface
- PyPDF2: PDF parsing
- python-docx: DOCX parsing
- requests: HTTP requests for job searching and applications
- pydantic: Data validation and schema definitions

## License

MIT