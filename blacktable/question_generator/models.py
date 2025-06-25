"""
Pydantic models for Question Generator
"""
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class QuestionType(str, Enum):
    """Question type enumeration"""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    EXPERIENCE = "experience"
    PROJECT = "project"
    SITUATIONAL = "situational"


class QuestionDifficulty(str, Enum):
    """Question difficulty enumeration"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class InterviewRound(str, Enum):
    """Interview round enumeration"""
    SCREENING = "screening"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    FINAL = "final"
    HR = "hr"


class Question(BaseModel):
    """Individual question model"""
    id: int
    text: str
    type: QuestionType
    difficulty: QuestionDifficulty
    focus_area: str
    expected_answer_points: List[str]
    follow_up_questions: Optional[List[str]] = None
    is_personalized: bool = False
    source_context: Optional[str] = None  # Context from resume if personalized


class QuestionSet(BaseModel):
    """Set of questions for an interview"""
    job_title: str
    interview_round: InterviewRound
    focus_area: str
    questions: List[Question]
    total_questions: int
    standard_questions_count: int
    personalized_questions_count: int


class StandardQuestionRequest(BaseModel):
    """Request model for generating standard questions"""
    job_description: str
    interview_round: InterviewRound
    focus_area: str
    difficulty_levels: List[QuestionDifficulty] = [QuestionDifficulty.MEDIUM]
    question_count: int = 10


class PersonalizedQuestionRequest(BaseModel):
    """Request model for generating personalized questions"""
    job_description: str
    interview_round: InterviewRound
    focus_area: str
    candidate_experience: List[dict]  # Work experience from resume
    candidate_projects: List[dict]    # Projects from resume
    candidate_skills: List[str]       # Skills from resume
    question_count: int = 5
