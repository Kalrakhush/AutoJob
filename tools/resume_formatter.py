import json
import re
from typing import Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from services.llm_service import LLMService

class ResumeFormatterInput(BaseModel):
    resume_data: Dict[str, Any] = Field(description="Parsed resume data")
    job_description: str = Field(description="Target job description")


class ResumeFormatterTool(BaseTool):
    """Reformats and tailors resumes to specific job descriptions using LLM intelligence."""
    def __init__(self):
        super().__init__(
            name="ResumeFormatterTool",
            description="Reformats and tailors resumes to specific job descriptions",
            input_schema=ResumeFormatterInput
        )

    def _run(self, resume_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """Use LLM to analyze and improve resume data based on the job description."""
        try:
            # Combine inputs into a single prompt
            prompt = (
                "You're a resume optimization assistant.\n"
                "Given the following parsed resume data and a target job description, do the following:\n"
                "1. Analyze the job description to identify key skills, experience, and qualifications.\n"
                "2. Tailor the resume by prioritizing matching skills, enhancing experience descriptions, "
                "and optionally generating a summary if missing.\n"
                "3. Return the improved resume in JSON format.\n"
                "4. Also include a summary of the improvements you made.\n\n"
                f"Job Description:\n{job_description}\n\n"
                f"Parsed Resume:\n{json.dumps(resume_data, indent=2)}\n\n"
                "Return JSON:\n{\n"
                "  \"improved_resume\": { ... },\n"
                "  \"matched_keywords\": [ ... ],\n"
                "  \"improvements\": [ ... ]\n"
                "}"
            )
            llm = LLMService()
            llm_response = llm.generate_response(prompt)

            # Clean the LLM response
            cleaned_response = re.sub(r"^```(?:json)?\s*|\s*```$", "", llm_response.strip(), flags=re.DOTALL)

            # Parse cleaned JSON response
            response_data = json.loads(cleaned_response)

            return {
                "original_resume": resume_data,
                **response_data
            }

        except json.JSONDecodeError as e:
            return {
                "error": "LLM response was not valid JSON",
                "raw_response": llm_response
            }
        except Exception as e:
            return {"error": str(e)}

# Example parsed resume input
# parsed_resume = {
#     "name": "John Doe",
#     "email": "john@example.com",
#     "skills": ["Java", "Spring Boot", "SQL", "Communication"],
#     "experience": [
#         {
#             "company": "Tech Mahindra",
#             "role": "Software Engineer",
#             "description": "Worked on Spring Boot microservices and database queries"
#         }
#     ],
#     "education": ["Bachelor of Technology in Computer Science"]
# }

# # Example job description
# job_description = """
# We are hiring a Java Developer with strong experience in Spring Boot, REST APIs, and SQL databases.
# Candidates must have excellent communication and problem-solving skills. Exposure to cloud platforms is a plus.
# """

# # Instantiate the tool
# formatter = ResumeFormatterTool()

# # Run the formatter tool
# result = formatter._run(resume_data=parsed_resume, job_description=job_description)

# print(result)
