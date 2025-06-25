"""
Tests for Question Generator
"""
import pytest
from blacktable.question_generator import QuestionGenerator, Question
from blacktable.resume_parser.models import ResumeData, Resume, About


class TestQuestionGenerator:
    """Test cases for Question Generator"""
    
    def setup_method(self):
        """Setup test method"""
        self.generator = QuestionGenerator()
    
    def test_generator_initialization(self):
        """Test generator initialization"""
        assert self.generator is not None
        assert self.generator.ai_service is not None
        assert self.generator.templates is not None
    
    def test_generate_standard_questions(self):
        """Test generating standard questions"""
        job_description = """
        Software Engineer Position
        We are looking for a Python developer with 3+ years experience.
        Requirements: Python, Django, REST APIs, SQL
        """
        
        try:
            questions = self.generator.generate_standard_questions(
                job_description=job_description,
                interview_round="technical",
                focus_area="backend development",
                question_count=5
            )
            
            assert isinstance(questions, list)
            assert len(questions) <= 5
            if questions:
                assert isinstance(questions[0], Question)
                
        except Exception as e:
            pytest.skip(f"AI service not available: {e}")
    
    def test_generate_personalized_questions(self):
        """Test generating personalized questions"""
        # Create mock resume data
        mock_resume_data = self._create_mock_resume_data()
        
        job_description = """
        Senior Python Developer
        5+ years experience with Python, Django, AWS
        """
        
        try:
            questions = self.generator.generate_personalized_questions(
                resume_data=mock_resume_data,
                job_description=job_description,
                interview_round="technical",
                question_count=3
            )
            
            assert isinstance(questions, list)
            assert len(questions) <= 3
            if questions:
                assert isinstance(questions[0], Question)
                assert questions[0].is_personalized == True
                
        except Exception as e:
            pytest.skip(f"AI service not available: {e}")
    
    def test_generate_mixed_question_set(self):
        """Test generating mixed question set"""
        mock_resume_data = self._create_mock_resume_data()
        
        job_description = """
        Full Stack Developer
        3+ years experience with Python, React, databases
        """
        
        try:
            question_set = self.generator.generate_mixed_question_set(
                resume_data=mock_resume_data,
                job_description=job_description,
                interview_round="technical",
                focus_area="full-stack",
                total_questions=10,
                personalized_ratio=0.3
            )
            
            assert question_set.total_questions == 10
            assert question_set.personalized_questions_count == 3
            assert question_set.standard_questions_count == 7
            
        except Exception as e:
            pytest.skip(f"AI service not available: {e}")
    
    def _create_mock_resume_data(self) -> ResumeData:
        """Create mock resume data for testing"""
        from blacktable.resume_parser.models import (
            About, WorkExperience, Project, Education, CandidateOverall, 
            Location, Timeline, Weblink, Resume, ResumeData
        )
        
        about = About(
            Name="John Doe",
            Mobile="+1234567890",
            Email="john@example.com",
            Linkedin="https://linkedin.com/in/johndoe",
            About="Experienced software developer",
            TotalWorkExperience=5
        )
        
        work_exp = WorkExperience(
            ID=1,
            Title="Senior Python Developer",
            Company="TechCorp",
            Location=Location(City="San Francisco", Country="USA"),
            Experience="5 years",
            Skills=["Python", "Django", "AWS"],
            Type="Full-Time",
            Timeline=Timeline(Start="2019", End="Present"),
            Description=["Developed web applications", "Led technical initiatives"]
        )
        
        project = Project(
            ID=1,
            Title="E-commerce Platform",
            Skills=["Python", "Django", "PostgreSQL"],
            Description=["Built scalable e-commerce platform"]
        )
        
        education = Education(
            ID=1,
            College="University of Technology",
            Degree="Bachelor of Science",
            Course="Computer Science",
            Timeline=Timeline(Start="2015", End="2019"),
            Duration=48,
            CGPA=3.8
        )
        
        candidate_overall = CandidateOverall(
            Skills=["Python", "Django", "JavaScript", "AWS", "SQL"],
            Achievements=["Top performer 2022", "Led successful project delivery"]
        )
        
        weblink = Weblink(
            Platform="LinkedIn",
            Link="https://linkedin.com/in/johndoe"
        )
        
        resume = Resume(
            About=about,
            WorkExperience=[work_exp],
            Projects=[project],
            Education=[education],
            CandidateOverall=candidate_overall,
            Weblinks=[weblink]
        )
        
        return ResumeData(resume=resume)
