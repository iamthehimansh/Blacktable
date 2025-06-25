"""
Question Generator - Main generator class
"""
from typing import List, Dict, Any
from ..core.ai_service import AIService
from ..resume_parser.models import ResumeData
from .models import (
    Question, QuestionSet, StandardQuestionRequest, PersonalizedQuestionRequest,
    InterviewRound, QuestionType, QuestionDifficulty
)
from .templates import QuestionTemplates


class QuestionGenerator:
    """AI-powered interview question generator"""
    
    def __init__(self, ai_provider: str = "openai"):
        """
        Initialize Question Generator
        
        Args:
            ai_provider: AI service provider ("openai" or "anthropic")
        """
        self.ai_service = AIService(provider=ai_provider)
        self.templates = QuestionTemplates()
    
    def generate_standard_questions(
        self,
        job_description: str,
        interview_round: str,
        focus_area: str,
        question_count: int = 10,
        difficulty_levels: List[str] = None
    ) -> List[Question]:
        """
        Generate standard interview questions for a job position
        
        Args:
            job_description: Job description text
            interview_round: Type of interview round
            focus_area: Specific area of focus
            question_count: Number of questions to generate
            difficulty_levels: List of difficulty levels
            
        Returns:
            List of generated questions
        """
        if difficulty_levels is None:
            difficulty_levels = ["medium"]
        
        # Convert string to enum
        round_enum = InterviewRound(interview_round)
        
        # Get prompt template
        system_prompt = self.templates.get_standard_prompt_template(round_enum)
        
        generation_prompt = f"""
Generate {question_count} interview questions for the following job:

Job Description:
{job_description}

Requirements:
- Interview Round: {interview_round}
- Focus Area: {focus_area}
- Difficulty Levels: {', '.join(difficulty_levels)}
- Generate diverse question types appropriate for this round
- Include expected answer points for each question
- Suggest follow-up questions where relevant

Format the response as a JSON object with a "questions" array containing question objects.
"""
        
        try:
            # Create a temporary model for the response
            from pydantic import BaseModel
            
            class QuestionResponse(BaseModel):
                questions: List[Question]
            
            response = self.ai_service.generate_structured_response(
                prompt=generation_prompt,
                response_model=QuestionResponse,
                system_prompt=system_prompt
            )
            
            return response.questions
            
        except Exception as e:
            raise ValueError(f"Failed to generate standard questions: {e}")
    
    def generate_personalized_questions(
        self,
        resume_data: ResumeData,
        job_description: str,
        interview_round: str,
        question_count: int = 5
    ) -> List[Question]:
        """
        Generate personalized interview questions based on candidate's resume
        
        Args:
            resume_data: Parsed resume data
            job_description: Job description text
            interview_round: Type of interview round
            question_count: Number of questions to generate
            
        Returns:
            List of personalized questions
        """
        # Extract relevant information from resume
        candidate_info = self._extract_candidate_context(resume_data)
        
        system_prompt = f"""
You are an expert interviewer creating personalized questions based on the candidate's specific background.
Focus on their actual experience, projects, and skills to create targeted questions that reveal depth of knowledge and experience.

Interview Round: {interview_round}
"""
        
        generation_prompt = f"""
Generate {question_count} personalized interview questions based on the candidate's resume and the job requirements.

Job Description:
{job_description}

Candidate Background:
- Name: {candidate_info['name']}
- Total Experience: {candidate_info['total_experience']} years
- Current/Recent Role: {candidate_info['recent_role']}
- Key Skills: {', '.join(candidate_info['skills'][:10])}  # Top 10 skills
- Recent Projects: {candidate_info['recent_projects']}
- Education: {candidate_info['education']}

Create questions that:
1. Probe specific experiences mentioned in their resume
2. Assess depth of knowledge in their claimed skills
3. Explore their project work and technical decisions
4. Understand their growth and learning from past roles
5. Connect their background to the job requirements

Each question should reference specific elements from their resume and be tailored to their experience level.
"""
        
        try:
            from pydantic import BaseModel
            
            class PersonalizedQuestionResponse(BaseModel):
                questions: List[Question]
            
            response = self.ai_service.generate_structured_response(
                prompt=generation_prompt,
                response_model=PersonalizedQuestionResponse,
                system_prompt=system_prompt
            )
            
            # Mark questions as personalized
            for question in response.questions:
                question.is_personalized = True
            
            return response.questions
            
        except Exception as e:
            raise ValueError(f"Failed to generate personalized questions: {e}")
    
    def generate_mixed_question_set(
        self,
        resume_data: ResumeData,
        job_description: str,
        interview_round: str,
        focus_area: str,
        total_questions: int = 15,
        personalized_ratio: float = 0.3
    ) -> QuestionSet:
        """
        Generate a mixed set of standard and personalized questions
        
        Args:
            resume_data: Parsed resume data
            job_description: Job description text
            interview_round: Type of interview round
            focus_area: Specific area of focus
            total_questions: Total number of questions
            personalized_ratio: Ratio of personalized questions (0.0 to 1.0)
            
        Returns:
            QuestionSet with mixed questions
        """
        personalized_count = int(total_questions * personalized_ratio)
        standard_count = total_questions - personalized_count
        
        # Generate standard questions
        standard_questions = self.generate_standard_questions(
            job_description=job_description,
            interview_round=interview_round,
            focus_area=focus_area,
            question_count=standard_count
        )
        
        # Generate personalized questions
        personalized_questions = self.generate_personalized_questions(
            resume_data=resume_data,
            job_description=job_description,
            interview_round=interview_round,
            question_count=personalized_count
        )
        
        # Combine questions
        all_questions = standard_questions + personalized_questions
        
        # Re-number questions
        for i, question in enumerate(all_questions, 1):
            question.id = i
        
        return QuestionSet(
            job_title=self._extract_job_title(job_description),
            interview_round=InterviewRound(interview_round),
            focus_area=focus_area,
            questions=all_questions,
            total_questions=len(all_questions),
            standard_questions_count=len(standard_questions),
            personalized_questions_count=len(personalized_questions)
        )
    
    def _extract_candidate_context(self, resume_data: ResumeData) -> Dict[str, Any]:
        """Extract relevant context from resume for personalized questions"""
        resume = resume_data.resume
        
        # Get recent work experience
        recent_role = "Not specified"
        if resume.WorkExperience:
            recent_exp = resume.WorkExperience[0]  # Assuming first is most recent
            recent_role = f"{recent_exp.Title} at {recent_exp.Company}"
        
        # Get recent projects
        recent_projects = []
        for project in resume.Projects[:3]:  # Top 3 projects
            recent_projects.append(f"{project.Title} ({', '.join(project.Skills[:3])})")
        
        # Get education
        education = "Not specified"
        if resume.Education:
            edu = resume.Education[0]
            education = f"{edu.Degree} in {edu.Course} from {edu.College}"
        
        return {
            'name': resume.About.Name,
            'total_experience': resume.About.TotalWorkExperience,
            'recent_role': recent_role,
            'skills': resume.CandidateOverall.Skills,
            'recent_projects': recent_projects,
            'education': education
        }
    
    def _extract_job_title(self, job_description: str) -> str:
        """Extract job title from job description"""
        # Simple extraction - could be enhanced with NLP
        lines = job_description.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            if any(keyword in line.lower() for keyword in ['position', 'role', 'job title', 'we are looking for']):
                return line.strip()

        return "Unknown Position"  # Default fallback
