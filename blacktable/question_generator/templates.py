"""
Question templates and prompts for Question Generator
"""
from typing import Dict, List
from .models import InterviewRound, QuestionType


class QuestionTemplates:
    """Templates for generating different types of questions"""
    
    STANDARD_QUESTION_PROMPTS = {
        InterviewRound.SCREENING: {
            "system_prompt": """
You are an expert interviewer creating screening questions for initial candidate evaluation. 
Focus on basic qualifications, cultural fit, and motivation.
""",
            "question_types": [QuestionType.BEHAVIORAL, QuestionType.EXPERIENCE],
            "sample_focuses": [
                "communication skills",
                "motivation and interest", 
                "basic technical understanding",
                "cultural fit",
                "career goals"
            ]
        },
        
        InterviewRound.TECHNICAL: {
            "system_prompt": """
You are a technical interviewer creating in-depth technical questions to assess candidate's 
programming skills, problem-solving abilities, and technical knowledge.
""",
            "question_types": [QuestionType.TECHNICAL, QuestionType.SITUATIONAL],
            "sample_focuses": [
                "coding and algorithms",
                "system design",
                "data structures",
                "debugging and troubleshooting",
                "best practices",
                "architecture decisions"
            ]
        },
        
        InterviewRound.BEHAVIORAL: {
            "system_prompt": """
You are a behavioral interviewer focusing on past experiences, leadership, teamwork, 
and soft skills assessment using STAR method principles.
""",
            "question_types": [QuestionType.BEHAVIORAL, QuestionType.SITUATIONAL],
            "sample_focuses": [
                "leadership and teamwork",
                "conflict resolution", 
                "adaptability and learning",
                "time management",
                "decision making",
                "communication"
            ]
        },
        
        InterviewRound.FINAL: {
            "system_prompt": """
You are conducting final round interviews focusing on strategic thinking, 
cultural alignment, and long-term potential.
""",
            "question_types": [QuestionType.BEHAVIORAL, QuestionType.SITUATIONAL],
            "sample_focuses": [
                "strategic thinking",
                "long-term vision",
                "cultural alignment",
                "growth potential",
                "industry knowledge"
            ]
        },
        
        InterviewRound.HR: {
            "system_prompt": """
You are an HR interviewer focusing on compensation, benefits, policies, 
and overall fit with company culture and values.
""",
            "question_types": [QuestionType.BEHAVIORAL],
            "sample_focuses": [
                "company culture fit",
                "work-life balance",
                "career development",
                "compensation expectations",
                "company policies"
            ]
        }
    }
    
    PERSONALIZED_QUESTION_PROMPTS = {
        "experience_based": """
Based on the candidate's work experience at {company} as {title}, create specific questions about:
- Challenges they faced in that role
- Specific technologies or methodologies they used
- Achievements and impact they made
- Lessons learned and growth
""",
        
        "project_based": """
Based on the candidate's project "{project_title}" involving {skills}, create questions about:
- Technical decisions and trade-offs made
- Implementation challenges and solutions
- Results and impact of the project
- What they would do differently
""",
        
        "skill_based": """
The candidate has experience with {skills}. Create questions that:
- Test practical application of these skills
- Explore depth of knowledge
- Assess how they've used these in real scenarios
- Understand their preferred approaches and methodologies
""",
        
        "gap_analysis": """
The job requires {required_skills} but candidate's resume shows {candidate_skills}.
Create questions to:
- Assess transferable skills
- Understand learning ability and adaptability
- Explore related experience that might be applicable
- Gauge willingness and ability to learn new technologies
"""
    }
    
    @classmethod
    def get_standard_prompt_template(cls, interview_round: InterviewRound) -> str:
        """Get standard question generation prompt template"""
        template = cls.STANDARD_QUESTION_PROMPTS.get(interview_round)
        if not template:
            raise ValueError(f"No template found for interview round: {interview_round}")
        
        return f"""
{template['system_prompt']}

Generate questions that are:
- Appropriate for {interview_round.value} round
- Focus on the specified area
- Include multiple difficulty levels
- Have clear evaluation criteria
- Include suggested follow-up questions

Question types to focus on: {', '.join([qt.value for qt in template['question_types']])}
"""
    
    @classmethod
    def get_personalized_prompt_template(cls, context_type: str) -> str:
        """Get personalized question generation prompt template"""
        template = cls.PERSONALIZED_QUESTION_PROMPTS.get(context_type)
        if not template:
            raise ValueError(f"No template found for context type: {context_type}")
        
        return template
