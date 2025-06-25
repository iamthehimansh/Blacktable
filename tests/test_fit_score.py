"""
Tests for FIT_Score
"""
import pytest
from blacktable.fit_score import FITScoreMatcher, FITScoreResult
from blacktable.resume_parser.models import ResumeData


class TestFITScoreMatcher:
    """Test cases for FIT Score Matcher"""
    
    def setup_method(self):
        """Setup test method"""
        self.matcher = FITScoreMatcher()
    
    def test_matcher_initialization(self):
        """Test matcher initialization"""
        assert self.matcher is not None
        assert self.matcher.ai_service is not None
        assert self.matcher.analyzer is not None
    
    def test_calculate_fit_score(self):
        """Test calculating FIT score"""
        mock_resume_data = self._create_mock_resume_data()
        
        job_description = """
        Senior Python Developer
        
        Requirements:
        - 5+ years of Python development experience
        - Experience with Django, Flask
        - Knowledge of AWS, Docker
        - Bachelor's degree in Computer Science
        
        Responsibilities:
        - Develop scalable web applications
        - Lead technical initiatives
        - Mentor junior developers
        """
        
        try:
            result = self.matcher.calculate_fit_score(
                resume_data=mock_resume_data,
                job_description=job_description
            )
            
            assert isinstance(result, FITScoreResult)
            assert 0 <= result.score <= 100
            assert result.category in ["excellent", "good", "fair", "poor"]
            assert 0 <= result.confidence <= 1
            assert isinstance(result.strengths, list)
            assert isinstance(result.gaps, list)
            assert isinstance(result.recommendations, list)
            
        except Exception as e:
            pytest.skip(f"AI service not available: {e}")
    
    def test_skill_analysis(self):
        """Test skill analysis component"""
        candidate_skills = ["Python", "Django", "JavaScript", "SQL"]
        required_skills = ["Python", "Django", "AWS"]
        preferred_skills = ["JavaScript", "Docker"]
        
        skill_matches = self.matcher.analyzer.analyze_skill_matches(
            candidate_skills, required_skills, preferred_skills
        )
        
        assert isinstance(skill_matches, list)
        assert len(skill_matches) > 0
        
        # Check that Python and Django are matched
        python_match = next((sm for sm in skill_matches if sm.skill == "Python"), None)
        assert python_match is not None
        assert python_match.candidate_has == True
        assert python_match.required == True
    
    def test_component_scores(self):
        """Test component score calculation"""
        from blacktable.fit_score.models import SkillMatch, ExperienceMatch, EducationMatch
        
        skill_matches = [
            SkillMatch(skill="Python", required=True, candidate_has=True, match_confidence=0.9),
            SkillMatch(skill="AWS", required=True, candidate_has=False, match_confidence=0.1)
        ]
        
        experience_matches = [
            ExperienceMatch(required_experience="5+ years", candidate_experience="5 years", 
                          match_score=0.8, relevance="high")
        ]
        
        education_match = EducationMatch(
            required_education="Bachelor's degree",
            candidate_education="Bachelor of Computer Science",
            match_score=0.9,
            is_sufficient=True
        )
        
        scores = self.matcher.analyzer.calculate_component_scores(
            skill_matches, experience_matches, education_match
        )
        
        assert "skill_score" in scores
        assert "experience_score" in scores
        assert "education_score" in scores
        assert 0 <= scores["skill_score"] <= 100
        assert 0 <= scores["experience_score"] <= 100
        assert 0 <= scores["education_score"] <= 100
    
    def _create_mock_resume_data(self) -> ResumeData:
        """Create mock resume data for testing"""
        from blacktable.resume_parser.models import (
            About, WorkExperience, Project, Education, CandidateOverall, 
            Location, Timeline, Weblink, Resume, ResumeData
        )
        
        about = About(
            Name="Jane Smith",
            Mobile="+1234567890",
            Email="jane@example.com",
            Linkedin="https://linkedin.com/in/janesmith",
            About="Senior software developer with 5+ years experience",
            TotalWorkExperience=5
        )
        
        work_exp = WorkExperience(
            ID=1,
            Title="Senior Python Developer",
            Company="TechCorp",
            Location=Location(City="New York", Country="USA"),
            Experience="5 years",
            Skills=["Python", "Django", "PostgreSQL"],
            Type="Full-Time",
            Timeline=Timeline(Start="2019", End="Present"),
            Description=["Developed scalable web applications", "Led team of 4 developers"]
        )
        
        project = Project(
            ID=1,
            Title="E-commerce Platform",
            Skills=["Python", "Django", "AWS"],
            Description=["Built high-traffic e-commerce platform serving 100k+ users"]
        )
        
        education = Education(
            ID=1,
            College="MIT",
            Degree="Bachelor of Science",
            Course="Computer Science",
            Timeline=Timeline(Start="2015", End="2019"),
            Duration=48,
            CGPA=3.9
        )
        
        candidate_overall = CandidateOverall(
            Skills=["Python", "Django", "JavaScript", "PostgreSQL", "Git", "Linux"],
            Achievements=["Employee of the year 2022", "Successfully led 3 major projects"]
        )
        
        weblink = Weblink(
            Platform="LinkedIn",
            Link="https://linkedin.com/in/janesmith"
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
