"""
Tests for Application Analyzer
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blacktable.application_analyzer import ApplicationAnalyzer
from blacktable.application_analyzer.models import (
    ApplicationAnalysisResult, CandidateProfile, WhyMatch, WhyNotMatch
)


class TestApplicationAnalyzer:
    """Test cases for ApplicationAnalyzer"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = ApplicationAnalyzer(ai_provider="openai")
        
        self.sample_job_data = {
            "job_title": "Python Developer",
            "job_description": "Looking for a Python developer with Django experience",
            "salary_range": "$70,000 - $90,000",
            "prescreening_questions": [
                "How many years of Python experience do you have?",
                "Are you familiar with Django?"
            ]
        }
        
        self.sample_application_data = {
            "prescreening_responses": {
                "How many years of Python experience do you have?": "5 years",
                "Are you familiar with Django?": "Yes, very experienced"
            },
            "current_ctc": "$65,000",
            "expected_ctc": "$80,000",
            "notice_period": "2 months",
            "additional_fields": {
                "location": "Remote",
                "github": "https://github.com/testuser"
            }
        }
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        analyzer = ApplicationAnalyzer()
        assert analyzer is not None
        assert analyzer.ai_service is not None
    
    @patch('blacktable.core.ai_service.AIService.generate_structured_response')
    def test_analyze_application_success(self, mock_ai_response):
        """Test successful application analysis"""
        # Mock AI response
        mock_result = ApplicationAnalysisResult(
            ai_score=85.0,
            why_match=WhyMatch(
                skill_matches=["Python experience"],
                experience_matches=["5 years experience"],
                cultural_fit=["Good communication"],
                growth_potential=["Eager to learn"],
                other_positives=[]
            ),
            why_not_match=WhyNotMatch(
                skill_gaps=[],
                experience_gaps=[],
                overqualification=[],
                salary_mismatch=[],
                other_concerns=[]
            ),
            candidate_profile=CandidateProfile(
                experience=["5 years Python development"],
                about="Experienced Python developer",
                skills=["Python", "Django"],
                previous_jobs=["Software Developer"],
                college=["Computer Science Degree"],
                other_details={}
            ),
            overall_recommendation="recommend",
            confidence_level="high",
            executive_summary="Strong candidate with relevant experience",
            key_highlights=["5 years Python experience", "Django expertise"],
            next_steps=["Schedule technical interview"],
            interview_focus_areas=["Django projects", "Problem solving"]
        )
        
        mock_ai_response.return_value = mock_result
        
        # Test analysis
        result = self.analyzer.analyze_application(**self.sample_job_data, **self.sample_application_data)
        
        assert result is not None
        assert result.ai_score == 85.0
        assert result.overall_recommendation == "recommend"
        assert "Python experience" in result.why_match.skill_matches
    
    @patch('blacktable.core.ai_service.AIService.generate_structured_response')
    def test_analyze_application_ai_failure(self, mock_ai_response):
        """Test application analysis when AI service fails"""
        # Mock AI service failure
        mock_ai_response.side_effect = Exception("AI service unavailable")
        
        # Test fallback analysis
        result = self.analyzer.analyze_application(**self.sample_job_data, **self.sample_application_data)
        
        assert result is not None
        assert result.overall_recommendation == "consider"
        assert result.confidence_level == "low"
        assert "AI analysis failed" in result.why_not_match.skill_gaps[0]
    
    def test_create_analysis_prompt(self):
        """Test analysis prompt creation"""
        from blacktable.application_analyzer.models import JobRequirements, JobApplication
        
        job_req = JobRequirements(**self.sample_job_data)
        job_app = JobApplication(**self.sample_application_data)
        
        prompt = self.analyzer._create_analysis_prompt(job_req, job_app)
        
        assert "Python Developer" in prompt
        assert "5 years" in prompt
        assert "Django experience" in prompt
        assert "ANALYSIS REQUIREMENTS" in prompt
    
    
    
    def test_minimal_application_data(self):
        """Test analysis with minimal application data"""
        minimal_data = {
            "job_title": "Developer",
            "job_description": "Basic developer role",
            "prescreening_responses": {"Question": "Answer"}
        }
        
        # This should not raise an exception
        result = self.analyzer.analyze_application(**minimal_data)
        assert result is not None
        assert isinstance(result, ApplicationAnalysisResult)
    
    
    def test_resume_prompt_integration(self):
        """Test that resume data is properly integrated into analysis prompt"""
        from blacktable.application_analyzer.models import JobRequirements, JobApplication
        from blacktable.resume_parser.models import Resume, About
        
        # Create job requirements and application with resume
        job_req = JobRequirements(**self.sample_job_data)
        
        # Create simple resume
        resume = Resume(About=About(Name="Test User", Email="test@test.com"))
        
        job_app = JobApplication(
            **self.sample_application_data,
            resume=resume
        )
        
        # Test prompt creation
        prompt = self.analyzer._create_analysis_prompt(job_req, job_app)
        
        assert "RESUME DATA:" in prompt
        assert "Test User" in prompt
        assert "test@test.com" in prompt
    
    
if __name__ == "__main__":
    # Run basic tests
    test_analyzer = TestApplicationAnalyzer()
    test_analyzer.setup_method()
    
    print("🧪 Running Enhanced Application Analyzer Tests...")
    print("=" * 60)
    
    try:
        test_analyzer.test_analyzer_initialization()
        print("✅ Analyzer initialization test passed")
        
        test_analyzer.test_create_analysis_prompt()
        print("✅ Analysis prompt creation test passed")
        
        
        test_analyzer.test_minimal_application_data()
        print("✅ Minimal application data test passed")
        
        test_analyzer.test_analyze_application_with_resume()
        print("✅ Resume integration test passed")
        
        test_analyzer.test_resume_prompt_integration()
        print("✅ Resume prompt integration test passed")
        
        
        print("\n🎉 All enhanced tests passed!")
        print("💡 Note: AI-dependent tests require proper API configuration")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        
    print("\n📋 To run full tests with pytest:")
    print("pip install pytest")
    print("pytest tests/test_application_analyzer.py -v")
