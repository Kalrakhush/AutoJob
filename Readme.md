# CareerBoost AI - Job Application Assistant

CareerBoost AI is an advanced job application assistant that uses artificial intelligence to help job seekers optimize their resumes and find relevant job opportunities. The application leverages CrewAI to orchestrate multiple specialized AI agents that work together to provide comprehensive assistance in the job application process.

## Features

- **Resume Analysis**: Upload your resume and get a detailed analysis of your skills, experience, and qualifications.
- **Job Search**: Find job openings that match your profile based on your resume analysis.
- **Resume Improvement**: Get personalized suggestions to improve your resume based on the target job positions.
- **Modern UI**: User-friendly interface built with Streamlit for a seamless experience.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/careerboost-ai.git
cd careerboost-ai
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL displayed in the terminal (usually http://localhost:8501).

3. Follow the app's interface to:
   - Upload your resume
   - Get a detailed analysis
   - Search for matching jobs
   - Receive personalized improvement suggestions

## Project Structure

```
job_application_assistant/
├── app.py                    # Main entry point for the Streamlit application
├── config/                   # Configuration settings
├── assets/                   # Static assets (CSS, images, JS)
├── components/               # Reusable UI components
├── pages/                    # Application pages
├── utils/                    # Utility functions
├── services/                 # Business logic services
├── agents/                   # CrewAI agents and configurations
└── tools/                    # Tools used by the agents
```

## Technologies Used

- **Streamlit**: For building the user interface
- **CrewAI**: For orchestrating AI agents
- **Google Gemini**: For natural language processing
- **Several search APIs**: For finding job opportunities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.