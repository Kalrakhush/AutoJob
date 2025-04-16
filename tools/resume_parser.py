#tools/resume_parser.py
import os
import re
import json
import PyPDF2
from docx import Document
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from services.llm_service import LLMService

class ResumeParseInput(BaseModel):
    resume_path: str = Field(description="Path to the resume file")

class ResumeParseTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="ResumeParseTool",
            description="Extracts all information available from resume documents using an LLM without preset fields",
            input_schema=ResumeParseInput
        )
        

    def _run(self, resume_path: str) -> dict:
        """Extract information from a resume file using LLM."""
        try:
            if resume_path.endswith('.pdf'):
                content = self._parse_pdf(resume_path)
            elif resume_path.endswith('.docx'):
                content = self._parse_docx(resume_path)
            elif resume_path.endswith('.txt'):
                content = self._parse_txt(resume_path)
            elif resume_path.endswith('.json'):
                content = self._parse_json(resume_path)
            else:
                return {"error": "Unsupported file format"}
            
            parsed_data = self._extract_information(content)
            return parsed_data
        except Exception as e:
            return {"error": str(e)}

    def _parse_pdf(self, path):
        text = ""
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def _parse_docx(self, path):
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])

    def _parse_txt(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def _parse_json(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _extract_information(self, content):
        try:
            prompt = (
                "Analyze the following resume text and extract every piece of information that is present. "
                "Do not assume specific sections or hardcode keys—simply output everything you find in the text as a JSON object. "
                "Your output should only be valid JSON. If certain details are repeated, structure them appropriately. "
                "Resume Text:\n\n"
                f"{content}\n\n"
                "Return the extracted information as a JSON object."
            )
            llm = LLMService()
            llm_response = llm.generate_response(prompt)

            # Clean the LLM response
            cleaned_response = re.sub(r"^```(?:json)?\s*|\s*```$", "", llm_response.strip(), flags=re.DOTALL)

            # Parse cleaned JSON response
            response_data = json.loads(cleaned_response)

            return {
            "resume_data": response_data  # Corrected this line
            }


        except json.JSONDecodeError as e:
            return {
                "error": "LLM response was not valid JSON",
                "raw_response": llm_response
            }
        except Exception as e:
            return {"error": str(e)}


# Example usage:
tool = ResumeParseTool()
result = tool.run(resume_path=r"C:\Users\15038\Documents\Khushpreet's Resume.pdf")
print(result)
