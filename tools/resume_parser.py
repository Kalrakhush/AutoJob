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
            description="Extracts structured information from a resume file using LLM",
            input_schema=ResumeParseInput
        )

    def _run(self, tool_input: dict) -> dict:
        resume_path = tool_input.get("resume_path")
        if not resume_path or not os.path.exists(resume_path):
            return {"error": f"Invalid or missing file: {resume_path}"}
        return self._extract_from_resume(resume_path)

    def _extract_from_resume(self, resume_path: str) -> dict:
        try:
            content = self._read_resume_file(resume_path)
            return self._extract_information(content)
        except Exception as e:
            return {"error": str(e)}
    
    def _read_resume_file(self, path):
        ext = path.lower().split('.')[-1]
        if ext == 'pdf':
            return self._parse_pdf(path)
        elif ext == 'docx':
            return self._parse_docx(path)
        elif ext == 'txt':
            return self._parse_txt(path)
        elif ext == 'json':
            return self._parse_json(path)
        else:
            raise ValueError("Unsupported file type")

    def _parse_pdf(self, path):
        import PyPDF2
        text = ""
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def _parse_docx(self, path):
        from docx import Document
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])

    def _parse_txt(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    def _parse_json(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            return json.dumps(json.load(file), indent=2)

    def _extract_information(self, content):
        from services.llm_service import LLMService
        prompt = (
            "Analyze the following resume and extract all possible details as proper string eith proper line breaks. "
            "understand the text first of resume , as it can be of any format. Then give proper headers as are in resume and proper details.\n\n"
            f"{content}\n\n"
            
        )
        llm = LLMService()
        response = llm.generate_response(prompt)
        return response
