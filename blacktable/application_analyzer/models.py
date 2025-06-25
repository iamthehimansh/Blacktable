"""
Pydantic models for Application Analysis
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from ..resume_parser.models import Resume


class CandidateProfile(BaseModel):
    """Comprehensive candidate profile extracted from application"""
    experience: List[str] = Field(description="List of work experiences")
    about: str = Field(description="Summary about the candidate")
    skills: List[str] = Field(description="List of technical and soft skills")
    previous_jobs: List[str] = Field(description="List of previous job titles and companies")
    college: List[str] = Field(description="List of educational institutions and degrees")
    other_details: Dict[str, Any] = Field(description="Additional details from application")


class JobApplication(BaseModel):
    """Job application form data"""
    # Personal Information (extracted/inferred from form)
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    
    # Resume Data - Complete structured resume information
    resume: Optional[Resume] = Field(
        None, 
        description="Complete resume data including About, WorkExperience, Projects, Education, etc."
    )
    
    # Job Information
    current_ctc: Optional[str] = None
    expected_ctc: Optional[str] = None
    notice_period: Optional[str] = None
    
    # Pre-screening questionnaire responses
    prescreening_responses: Dict[str, str] = Field(
        description="Dictionary of pre-screening questions and candidate answers"
    )
    
    # Additional application fields
    additional_fields: Dict[str, Any] = Field(
        default_factory=dict,
        description="Any other fields filled by the candidate"
    )


class JobRequirements(BaseModel):
    """Job posting requirements"""
    job_title: str
    job_description: str
    salary_range: Optional[str] = None
    prescreening_questions: List[str] = Field(
        description="List of pre-screening questions"
    )
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    experience_requirements: List[str] = Field(default_factory=list)
    education_requirements: Optional[str] = None


class WhyMatch(BaseModel):
    """Reasons why the candidate matches the job"""
    skill_matches: List[str] = Field(description="Skills that match job requirements")
    experience_matches: List[str] = Field(description="Relevant experience for the role")
    cultural_fit: List[str] = Field(description="Indicators of cultural fit")
    growth_potential: List[str] = Field(description="Evidence of growth potential")
    other_positives: List[str] = Field(description="Other positive indicators")


class WhyNotMatch(BaseModel):
    """Reasons why the candidate might not match the job"""
    skill_gaps: List[str] = Field(description="Missing or weak skills")
    experience_gaps: List[str] = Field(description="Lack of relevant experience")
    overqualification: List[str] = Field(description="Areas where candidate might be overqualified")
    salary_mismatch: List[str] = Field(description="Potential salary expectation issues")
    other_concerns: List[str] = Field(description="Other potential concerns")


class ApplicationAnalysisResult(BaseModel):
    """Complete application analysis result"""
    # Core Analysis
    ai_score: float = Field(ge=0.0, le=100.0, description="AI-generated fit score")
    why_match: WhyMatch = Field(description="Reasons for positive match")
    why_not_match: WhyNotMatch = Field(description="Reasons for concerns")
    
    # Candidate Profile
    candidate_profile: CandidateProfile = Field(description="Extracted candidate profile")
    
    # Overall Assessment
    overall_recommendation: str = Field(
        description="Overall hiring recommendation: strongly_recommend, recommend, consider, not_recommend"
    )
    confidence_level: str = Field(
        description="Confidence in analysis: high, medium, low"
    )
    
    # Summary
    executive_summary: str = Field(description="Brief executive summary for hiring managers")
    key_highlights: List[str] = Field(description="Top 3-5 key highlights")
    
    # Action Items
    next_steps: List[str] = Field(description="Recommended next steps in hiring process")
    interview_focus_areas: List[str] = Field(description="Areas to focus on during interviews")
