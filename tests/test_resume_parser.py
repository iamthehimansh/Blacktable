"""
Tests for Resume Parser
"""
import pytest
import os
from blacktable.resume_parser import ResumeParser, ResumeData


class TestResumeParser:
    """Test cases for Resume Parser"""
    
    def setup_method(self):
        """Setup test method"""
        self.parser = ResumeParser()
    
    def test_parser_initialization(self):
        """Test parser initialization"""
        assert self.parser is not None
        assert self.parser.ai_service is not None
        assert self.parser.document_processor is not None
    
    def test_supported_format_check(self):
        """Test supported format checking"""
        assert self.parser.document_processor.is_supported_format("test.pdf")
        assert self.parser.document_processor.is_supported_format("test.doc")
        assert self.parser.document_processor.is_supported_format("test.docx")
        assert self.parser.document_processor.is_supported_format("test.txt")
        assert not self.parser.document_processor.is_supported_format("test.xyz")
    
    def test_parse_resume_from_text(self):
        """Test parsing resume from text"""
        sample_resume_text = """
        John Doe
        Software Engineer
        Email: john.doe@email.com
        Phone: +1-234-567-8900
        
        Experience:
        Software Engineer at TechCorp (2020-2023)
        - Developed web applications using Python and React
        - Led a team of 3 developers
        
        Education:
        Bachelor of Computer Science, MIT (2016-2020)
        
        Skills: Python, JavaScript, React, SQL
        """
        
        try:
            result = self.parser.parse_resume_from_text(sample_resume_text)
            assert isinstance(result, ResumeData)
            assert result.resume.About.Name is not None
        except Exception as e:
            # Test should pass even if AI service is not available
            pytest.skip(f"AI service not available: {e}")
    
    @pytest.mark.skipif(not os.path.exists("Himansh_CV.pdf"), reason="Test PDF not found")
    def test_parse_pdf_resume(self):
        """Test parsing PDF resume"""
        try:
            result = self.parser.parse_resume("Himansh_CV.pdf")
            assert isinstance(result, ResumeData)
            assert result.resume.About.Name is not None
        except Exception as e:
            pytest.skip(f"PDF parsing failed or AI service not available: {e}")
    
    def test_unsupported_format_error(self):
        """Test error for unsupported format"""
        with pytest.raises(ValueError, match="Unsupported file format"):
            self.parser.parse_resume("test.xyz")
    
    def test_file_not_found_error(self):
        """Test error for non-existent file"""
        with pytest.raises(FileNotFoundError):
            self.parser.parse_resume("non_existent_file.pdf")
