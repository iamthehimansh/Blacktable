"""
BlackTable - AI-Powered Recruitment Module
"""

try:
    from .resume_parser import ResumeParser
    from .question_generator import QuestionGenerator
    from .fit_score import FITScoreMatcher
except ImportError as e:
    # Handle import errors gracefully during development
    print(f"Warning: Some components could not be imported: {e}")
    ResumeParser = None
    QuestionGenerator = None
    FITScoreMatcher = None

__version__ = "1.0.0"
__author__ = "Himansh Raj"

__all__ = [
    "ResumeParser",
    "QuestionGenerator", 
    "FITScoreMatcher"
]
