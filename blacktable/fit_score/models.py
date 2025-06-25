"""
Pydantic models for FIT_Score
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SkillMatch(BaseModel):
    """Skill matching analysis"""
    skill: str
    required: bool
    candidate_has: bool
    proficiency_level: Optional[str] = None
    match_confidence: float = Field(ge=0.0, le=1.0)


class ExperienceMatch(BaseModel):
    """Experience matching analysis"""
    required_experience: str
    candidate_experience: str
    match_score: float = Field(ge=0.0, le=1.0)
    relevance: str  # "high", "medium", "low"


class EducationMatch(BaseModel):
    """Education matching analysis"""
    required_education: Optional[str] = None
    candidate_education: str
    match_score: float = Field(ge=0.0, le=1.0)
    is_sufficient: bool


class Strength(BaseModel):
    """Candidate strength"""
    category: str  # "skills", "experience", "education", "projects"
    description: str
    evidence: List[str]  # Supporting evidence from resume
    relevance_score: float = Field(ge=0.0, le=1.0)


class Gap(BaseModel):
    """Candidate gap/weakness"""
    category: str  # "skills", "experience", "education"
    description: str
    severity: str  # "critical", "important", "minor"
    mitigation_suggestions: List[str]


class Recommendation(BaseModel):
    """Hiring recommendation"""
    category: str  # "skill_development", "training", "experience_gain"
    description: str
    priority: str  # "high", "medium", "low"
    timeline: Optional[str] = None


class DetailedAnalysis(BaseModel):
    """Detailed FIT analysis"""
    skill_matches: List[SkillMatch]
    experience_matches: List[ExperienceMatch]
    education_match: EducationMatch
    strengths: List[Strength]
    gaps: List[Gap]
    overall_assessment: str


class FITScoreResult(BaseModel):
    """Complete FIT Score result"""
    score: float = Field(ge=0.0, le=100.0)
    category: str  # "excellent", "good", "fair", "poor"
    confidence: float = Field(ge=0.0, le=1.0)
    
    # High-level summaries
    strengths: List[str]
    gaps: List[str]
    recommendations: List[str]
    
    # Detailed analysis
    detailed_analysis: DetailedAnalysis
    
    # Breakdown scores
    skill_score: float = Field(ge=0.0, le=100.0)
    experience_score: float = Field(ge=0.0, le=100.0) 
    education_score: float = Field(ge=0.0, le=100.0)
    overall_potential_score: float = Field(ge=0.0, le=100.0)
    
    # Summary
    summary: str
    hiring_recommendation: str  # "strongly_recommend", "recommend", "consider", "not_recommend"


# this is created to maintain consistency with the existing codebase
class RandomVariable(BaseModel):
    """Placeholder for random variable"""
    name: str
    value: Any

class JobRequirements(BaseModel):
    """Parsed job requirements"""
    title: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_requirements: List[str]
    education_requirements: Optional[str] = None
    key_responsibilities: List[str]
    company_type: Optional[str] = None
    seniority_level: str  # "entry", "mid", "senior", "executive"
    random_variables: Optional[RandomVariable] = None
if __name__=="__main__":
    print(JobRequirements.model_json_schema())
    print(FITScoreResult.model_json_schema())