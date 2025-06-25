"""
Resume Parser - Main parser class
"""
from typing import Optional
from .models import ResumeData
from .utils import DocumentProcessor
from ..core.ai_service import AIService


class ResumeParser:
    """AI-powered resume parser"""
    
    def __init__(self, ai_provider: str = "openai"):
        """
        Initialize Resume Parser
        
        Args:
            ai_provider: AI service provider ("openai" or "anthropic")
        """
        self.document_processor = DocumentProcessor()
        self.ai_service = AIService(provider=ai_provider)
    
    def parse_resume(self, file_path: str) -> ResumeData:
        """
        Parse resume from file and extract structured data
        
        Args:
            file_path: Path to the resume file
            
        Returns:
            ResumeData: Structured resume data
        """
        # Validate file format
        if not self.document_processor.is_supported_format(file_path):
            raise ValueError(f"Unsupported file format: {file_path}")
        
        # Convert document to markdown
        markdown_content = self.document_processor.convert_to_markdown(file_path)
        
        # Create prompt for AI extraction
        system_prompt = """
You are an expert resume parser. Extract all relevant information from the resume and structure it according to the provided JSON schema. 

Guidelines:
- Extract all information accurately
- If information is not present, use null or empty arrays as appropriate
- For work experience, assign sequential IDs starting from 1
- For projects and education, also use sequential IDs
- Parse dates in a readable format (e.g., "October 2023", "June 2023")
- Extract skills from throughout the resume
- Calculate total work experience in years
- Be thorough in extracting descriptions and achievements
"""
        
        extraction_prompt = f"""
Please parse the following resume content and extract all information according to the JSON schema:

Resume Content:
{markdown_content}

Extract all personal information, work experience, projects, education, skills, achievements, and any other relevant details. Ensure all data is properly structured and accurate.
"""
        
        # Generate structured response using AI
        try:
            resume_data = self.ai_service.generate_structured_response(
                prompt=extraction_prompt,
                response_model=ResumeData,
                system_prompt=system_prompt
            )
            return resume_data
        except Exception as e:
            raise ValueError(f"Failed to parse resume: {e}")
    
    def parse_resume_from_text(self, text_content: str) -> ResumeData:
        """
        Parse resume from text content directly
        
        Args:
            text_content: Resume text content
            
        Returns:
            ResumeData: Structured resume data
        """
        system_prompt = """
You are an expert resume parser. Extract all relevant information from the resume and structure it according to the provided JSON schema. 

Guidelines:
- Extract all information accurately
- If information is not present, use null or empty arrays as appropriate
- For work experience, assign sequential IDs starting from 1
- For projects and education, also use sequential IDs
- Parse dates in a readable format (e.g., "October 2023", "June 2023")
- Extract skills from throughout the resume
- Calculate total work experience in years
- Be thorough in extracting descriptions and achievements
"""
        
        extraction_prompt = f"""
Please parse the following resume content and extract all information according to the JSON schema:

Resume Content:
{text_content}

Extract all personal information, work experience, projects, education, skills, achievements, and any other relevant details. Ensure all data is properly structured and accurate.
"""
        
        try:
            resume_data = self.ai_service.generate_structured_response(
                prompt=extraction_prompt,
                response_model=ResumeData,
                system_prompt=system_prompt
            )
            return resume_data
        except Exception as e:
            raise ValueError(f"Failed to parse resume text: {e}")
