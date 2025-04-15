# resume_parser.py
import os
import json
import PyPDF2
from docx import Document
from crewai import Tool
from pydantic import BaseModel, Field

class ResumeParseInput(BaseModel):
    resume_path: str = Field(description="Path to the resume file")

class ResumeParseTool(Tool):
    def __init__(self):
        super().__init__(
            name="ResumeParseTool",
            description="Extracts structured information from resume documents",
            input_schema=ResumeParseInput
        )
    
    def _run(self, resume_path: str) -> dict:
        """Extract information from a resume file."""
        try:
            # Extract content based on file extension
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
            
            # Process the content to extract structured information
            parsed_data = self._extract_information(content)
            return parsed_data
        except Exception as e:
            return {"error": str(e)}
    
    def _parse_pdf(self, path):
        """Extract text from PDF."""
        text = ""
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def _parse_docx(self, path):
        """Extract text from DOCX."""
        doc = Document(path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    
    def _parse_txt(self, path):
        """Extract text from TXT."""
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    
    def _parse_json(self, path):
        """Extract data from JSON."""
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def _extract_information(self, content):
        """Extract structured information from text content."""
        # Basic extraction logic - in production this would use NLP/ML
        lines = content.strip().split('\n')
        data = {
            "raw_text": content,
            "contact_info": {},
            "education": [],
            "experience": [],
            "skills": []
        }
        
        # Simple extraction - would be replaced with more sophisticated parsing
        sections = {'contact': [], 'education': [], 'experience': [], 'skills': []}
        current_section = 'contact'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            lower_line = line.lower()
            if 'education' in lower_line and len(line) < 30:
                current_section = 'education'
                continue
            elif any(x in lower_line for x in ['experience', 'employment', 'work']):
                if len(line) < 30:
                    current_section = 'experience'
                    continue
            elif any(x in lower_line for x in ['skills', 'technologies', 'competencies']):
                if len(line) < 30:
                    current_section = 'skills'
                    continue
                    
            sections[current_section].append(line)
        
        # Extract email and phone
        for line in sections['contact']:
            if '@' in line:
                data['contact_info']['email'] = line
            elif any(c.isdigit() for c in line) and len(line) < 20:
                data['contact_info']['phone'] = line
                
        # Process sections
        data['education'] = sections['education']
        data['experience'] = sections['experience']
        data['skills'] = sections['skills']
        
        return data

