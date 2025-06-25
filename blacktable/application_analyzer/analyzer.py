"""
Application Analyzer - AI-powered comprehensive job application analysis
"""
import json
from typing import Dict, Any, List
from ..core.ai_service import AIService
# from ..core.config import AIConfig
from ..fit_score.matcher import FITScoreMatcher
from ..fit_score.models import FITScoreResult
from ..resume_parser.models import ResumeData
from .models import (
    JobApplication, JobRequirements, ApplicationAnalysisResult,
    CandidateProfile, WhyMatch, WhyNotMatch
)


class ApplicationAnalyzer:
    """
    Comprehensive application analyzer that evaluates job applications 
    against job requirements using AI
    """
    
    def __init__(self, ai_provider: str = "openai"):
        """
        Initialize the application analyzer
        
        Args:
            ai_provider: AI provider to use ("openai" or "anthropic")
        """
        self.ai_service = AIService(provider=ai_provider)
        self.fit_score_matcher = FITScoreMatcher(ai_provider=ai_provider)
        # self.config = AIConfig()
    
    def analyze_application(
        self,
        job_title: str,
        job_description: str,
        salary_range: str = None,
        prescreening_questions: List[str] = None,
        prescreening_responses: Dict[str, str] = None,
        current_ctc: str = None,
        expected_ctc: str = None,
        notice_period: str = None,
        additional_fields: Dict[str, Any] = None,
        resume: Any = None
    ) -> ApplicationAnalysisResult:
        """
        Analyze a job application comprehensively
        
        Args:
            job_title: Title of the job position
            job_description: Detailed job description
            salary_range: Salary range for the position (optional)
            prescreening_questions: List of pre-screening questions (optional)
            prescreening_responses: Dict of question:answer pairs from candidate
            current_ctc: Candidate's current CTC
            expected_ctc: Candidate's expected CTC
            notice_period: Candidate's notice period
            additional_fields: Any other fields filled by candidate
            resume: Complete Resume object with structured resume data (optional)
            
        Returns:
            ApplicationAnalysisResult with comprehensive analysis
        """
        
        # Create job requirements and application objects
        job_requirements = JobRequirements(
            job_title=job_title,
            job_description=job_description,
            salary_range=salary_range,
            prescreening_questions=prescreening_questions or []
        )
        
        job_application = JobApplication(
            resume=resume,
            current_ctc=current_ctc,
            expected_ctc=expected_ctc,
            notice_period=notice_period,
            prescreening_responses=prescreening_responses or {},
            additional_fields=additional_fields or {}
        )
        
        # Calculate FIT Score if resume is available
        fit_score_result = None
        if resume:
            try:
                # Create ResumeData object for FIT Score analysis
                resume_data = ResumeData(resume=resume)
                fit_score_result = self.fit_score_matcher.calculate_fit_score(
                    resume_data=resume_data,
                    job_description=job_description
                )
            except Exception as e:
                # Log the error but continue with analysis
                print(f"Warning: FIT Score calculation failed: {e}")
                fit_score_result = None
        
        # Generate comprehensive analysis using AI (including FIT Score data)
        return self._generate_ai_analysis(job_requirements, job_application, fit_score_result)
    
    def _generate_ai_analysis(
        self, 
        job_requirements: JobRequirements, 
        job_application: JobApplication,
        fit_score_result: FITScoreResult = None
    ) -> ApplicationAnalysisResult:
        """
        Generate AI-powered analysis of the application
        
        Args:
            job_requirements: Job requirements object
            job_application: Job application object
            fit_score_result: FIT Score analysis result (optional)
            
        Returns:
            ApplicationAnalysisResult with AI-generated analysis
        """
        
        # Create comprehensive prompt for AI analysis
        analysis_prompt = self._create_analysis_prompt(job_requirements, job_application, fit_score_result)
        
        # System prompt for AI
        system_prompt = """
You are an expert AI recruitment analyst with deep expertise in talent assessment, 
job matching, and candidate evaluation. Your role is to provide comprehensive, 
objective, and actionable analysis of job applications.

You will receive job application data along with detailed FIT Score analysis that provides 
technical skill matching, experience relevance, and detailed gap analysis. Use this 
FIT Score data to enhance your assessment and provide more accurate analysis.

Analyze the provided job application data against the job requirements and provide:
1. A precise AI fit score (0-100) - consider and incorporate the FIT Score analysis
2. Detailed reasons why the candidate matches
3. Detailed reasons for concerns or gaps
4. Extracted candidate profile information
5. Strategic hiring recommendations

Be thorough, objective, and provide actionable insights for hiring managers.
Focus on both hard skills and soft skills, cultural fit, growth potential, and overall suitability.
Use the FIT Score analysis to inform your technical assessment while adding your own insights 
on communication, cultural fit, and overall potential.
"""
        
        # Generate structured response using AI
        try:
            result = self.ai_service.generate_structured_response(
                prompt=analysis_prompt,
                response_model=ApplicationAnalysisResult,
                system_prompt=system_prompt
            )
            return result
        except Exception as e:
            # Fallback analysis if AI fails
            print(f"Warning: AI analysis failed, performing fallback analysis: {e}")
            # throw e  # Optionally re-raise the exception for further handling
            raise ValueError("AI analysis failed, fallback analysis not implemented")

    def _create_analysis_prompt(
        self, 
        job_requirements: JobRequirements, 
        job_application: JobApplication,
        fit_score_result: FITScoreResult = None
    ) -> str:
        """
        Create a comprehensive prompt for AI analysis
        
        Args:
            job_requirements: Job requirements object
            job_application: Job application object
            fit_score_result: FIT Score analysis result (optional)
            
        Returns:
            Formatted prompt string
        """
        
        prompt = f"""
Analyze this job application comprehensively:

JOB REQUIREMENTS:
=================
Job Title: {job_requirements.job_title}
Job Description: {job_requirements.job_description}
"""
        
        if job_requirements.salary_range:
            prompt += f"Salary Range: {job_requirements.salary_range}\n"
        
        if job_requirements.prescreening_questions:
            prompt += f"Pre-screening Questions: {', '.join(job_requirements.prescreening_questions)}\n"
        
        prompt += f"""

CANDIDATE APPLICATION:
=====================
"""
        
        if job_application.current_ctc:
            prompt += f"Current CTC: {job_application.current_ctc}\n"
        
        if job_application.expected_ctc:
            prompt += f"Expected CTC: {job_application.expected_ctc}\n"
        
        if job_application.notice_period:
            prompt += f"Notice Period: {job_application.notice_period}\n"
        
        if job_application.prescreening_responses:
            prompt += "\nPre-screening Responses:\n"
            for question, answer in job_application.prescreening_responses.items():
                prompt += f"Q: {question}\nA: {answer}\n\n"
        
        if job_application.additional_fields:
            prompt += "\nAdditional Information:\n"
            for field, value in job_application.additional_fields.items():
                prompt += f"{field}: {value}\n"
        
        # Add resume data if available
        if job_application.resume:
            prompt += "\nRESUME DATA:\n"
            prompt += "============\n"
            resume = job_application.resume
            
            # About section
            if resume.About:
                prompt += f"Candidate Name: {resume.About.Name or 'Not provided'}\n"
                prompt += f"Email: {resume.About.Email or 'Not provided'}\n"
                prompt += f"Mobile: {resume.About.Mobile or 'Not provided'}\n"
                prompt += f"LinkedIn: {resume.About.Linkedin or 'Not provided'}\n"
                prompt += f"About: {resume.About.About or 'Not provided'}\n"
                prompt += f"Total Work Experience: {resume.About.TotalWorkExperience or 0} years\n\n"
            
            # Work Experience
            if resume.WorkExperience:
                prompt += "Work Experience:\n"
                for exp in resume.WorkExperience:
                    prompt += f"- {exp.Title or 'Unknown Title'} at {exp.Company or 'Unknown Company'}\n"
                    if exp.Timeline:
                        prompt += f"  Duration: {exp.Timeline.Start or 'N/A'} to {exp.Timeline.End or 'N/A'}\n"
                    if exp.Skills:
                        prompt += f"  Skills: {', '.join(exp.Skills)}\n"
                    if exp.Description:
                        prompt += f"  Description: {' '.join(exp.Description[:2])}\n"  # First 2 description points
                prompt += "\n"
            
            # Education
            if resume.Education:
                prompt += "Education:\n"
                for edu in resume.Education:
                    prompt += f"- {edu.Degree or 'Unknown Degree'} in {edu.Course or 'Unknown Course'}\n"
                    prompt += f"  Institution: {edu.College or 'Unknown College'}\n"
                    if edu.Timeline:
                        prompt += f"  Duration: {edu.Timeline.Start or 'N/A'} to {edu.Timeline.End or 'N/A'}\n"
                    if edu.CGPA:
                        prompt += f"  CGPA: {edu.CGPA}\n"
                prompt += "\n"
            
            # Projects
            if resume.Projects:
                prompt += "Projects:\n"
                for proj in resume.Projects[:3]:  # Limit to top 3 projects
                    prompt += f"- {proj.Title or 'Unknown Project'}\n"
                    if proj.Skills:
                        prompt += f"  Technologies: {', '.join(proj.Skills)}\n"
                    if proj.Description:
                        prompt += f"  Description: {' '.join(proj.Description[:1])}\n"  # First description point
                prompt += "\n"
            
            # Skills from CandidateOverall
            if resume.CandidateOverall and resume.CandidateOverall.Skills:
                prompt += f"Overall Skills: {', '.join(resume.CandidateOverall.Skills)}\n"
            
            # Achievements
            if resume.CandidateOverall and resume.CandidateOverall.Achievements:
                prompt += f"Achievements: {', '.join(resume.CandidateOverall.Achievements)}\n"
            
            prompt += "\n"
        
        # Add FIT Score analysis if available
        if fit_score_result:
            prompt += f"""
FIT SCORE ANALYSIS:
==================
Technical FIT Score: {fit_score_result.score:.1f}/100 ({fit_score_result.category})
Confidence Level: {fit_score_result.confidence:.2f}

Component Scores:
- Skills Match: {fit_score_result.skill_score:.1f}/100
- Experience Match: {fit_score_result.experience_score:.1f}/100  
- Education Match: {fit_score_result.education_score:.1f}/100
- Growth Potential: {fit_score_result.overall_potential_score:.1f}/100

Strengths Identified:
{chr(10).join(f"- {strength}" for strength in fit_score_result.strengths)}

Gaps Identified:
{chr(10).join(f"- {gap}" for gap in fit_score_result.gaps)}

FIT Score Recommendations:
{chr(10).join(f"- {rec}" for rec in fit_score_result.recommendations)}

FIT Score Summary: {fit_score_result.summary}
FIT Score Hiring Recommendation: {fit_score_result.hiring_recommendation}

Detailed Technical Analysis:
- Total Skills Analyzed: {len(fit_score_result.detailed_analysis.skill_matches)}
- Skills Matched: {len([sm for sm in fit_score_result.detailed_analysis.skill_matches if sm.candidate_has])}
- Experience Areas Evaluated: {len(fit_score_result.detailed_analysis.experience_matches)}
- Education Assessment: {fit_score_result.detailed_analysis.education_match.candidate_education}

"""
        
        prompt += """

ANALYSIS REQUIREMENTS:
=====================
Please provide a comprehensive analysis including:

1. AI Score (0-100): Calculate based on overall fit considering:
   - Technical skills match (use FIT Score analysis as primary reference)
   - Experience relevance  
   - Cultural fit indicators
   - Growth potential
   - Salary expectations alignment
   - Communication quality in responses
   - Overall FIT Score assessment and recommendations

2. Why Match: Identify specific reasons why this candidate is a good fit:
   - Skill matches with job requirements (reference FIT Score detailed analysis)
   - Relevant experience indicators (use FIT Score experience matches)
   - Cultural fit signals
   - Growth potential evidence (consider FIT Score potential score)
   - Communication quality from responses
   - Other positive indicators from FIT Score strengths

3. Why Not Match: Identify potential concerns or gaps:
   - Missing or weak skills (reference FIT Score gaps analysis)
   - Experience gaps (use FIT Score experience analysis)
   - Overqualification risks
   - Salary mismatch concerns
   - Communication or response quality issues
   - Other concerns from FIT Score analysis

4. Candidate Profile: Extract and infer:
   - Experience list (work history indicators)
   - About summary (professional summary)
   - Skills list (technical and soft skills)
   - Previous jobs (job titles and companies)
   - College information (education background)
   - Other relevant details

5. Recommendations: Provide strategic hiring advice including:
   - Overall recommendation level (consider FIT Score hiring recommendation)
   - Confidence in assessment (factor in FIT Score confidence)
   - Executive summary (incorporate FIT Score insights)
   - Key highlights (include both technical and soft skill assessments)
   - Next steps (consider FIT Score recommendations)
   - Interview focus areas (target both technical gaps and cultural fit)

Be thorough, objective, and provide actionable insights for hiring decisions.
When FIT Score analysis is available, use it as the foundation for technical assessment 
while adding your insights on communication skills, cultural fit, and overall candidate potential.
If FIT Score analysis is not available, perform your own technical assessment.
"""
        
        return prompt
    

