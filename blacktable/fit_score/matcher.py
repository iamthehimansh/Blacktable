"""
FIT_Score Matcher - Main matching class
"""
from typing import List, Dict, Any
from ..core.ai_service import AIService
from ..resume_parser.models import ResumeData
from .models import FITScoreResult, JobRequirements, DetailedAnalysis
from .analyzer import FITScoreAnalyzer


class FITScoreMatcher:
    """AI-powered resume and job description matcher"""
    
    def __init__(self, ai_provider: str = "openai"):
        """
        Initialize FIT Score Matcher
        
        Args:
            ai_provider: AI service provider ("openai" or "anthropic")
        """
        self.ai_service = AIService(provider=ai_provider)
        self.analyzer = FITScoreAnalyzer()
    
    def calculate_fit_score(
        self, 
        resume_data: ResumeData, 
        job_description: str
    ) -> FITScoreResult:
        """
        Calculate FIT score between resume and job description
        
        Args:
            resume_data: Parsed resume data
            job_description: Job description text
            
        Returns:
            FITScoreResult: Complete FIT analysis
        """
        # Step 1: Parse job requirements using AI
        job_requirements = self._parse_job_requirements(job_description)
        
        # Step 2: Perform detailed analysis
        detailed_analysis = self._perform_detailed_analysis(resume_data, job_requirements)
        
        # Step 3: Calculate component scores
        component_scores = self.analyzer.calculate_component_scores(
            detailed_analysis.skill_matches,
            detailed_analysis.experience_matches,
            detailed_analysis.education_match
        )
        
        # Step 4: Calculate overall FIT score using AI
        overall_score = self._calculate_overall_score(
            resume_data, job_requirements, detailed_analysis, component_scores
        )
        
        # Step 5: Generate recommendations
        recommendations = self._generate_recommendations(detailed_analysis)
        
        # Step 6: Create final result
        return FITScoreResult(
            score=overall_score["score"],
            category=overall_score["category"],
            confidence=overall_score["confidence"],
            strengths=[s.description for s in detailed_analysis.strengths],
            gaps=[g.description for g in detailed_analysis.gaps],
            recommendations=recommendations,
            detailed_analysis=detailed_analysis,
            skill_score=component_scores["skill_score"],
            experience_score=component_scores["experience_score"],
            education_score=component_scores["education_score"],
            overall_potential_score=overall_score["potential_score"],
            summary=overall_score["summary"],
            hiring_recommendation=overall_score["hiring_recommendation"]
        )
    
    def _parse_job_requirements(self, job_description: str) -> JobRequirements:
        """Parse job description to extract structured requirements"""
        system_prompt = """
You are an expert at analyzing job descriptions and extracting structured requirements.
Extract all relevant information including required skills, preferred skills, experience requirements, 
education requirements, and other key details.
"""
        
        extraction_prompt = f"""
Analyze the following job description and extract structured requirements:

Job Description:
{job_description}

Extract:
1. Job title
2. Required technical and soft skills
3. Preferred/nice-to-have skills  
4. Experience requirements (years, type, specific domains)
5. Education requirements
6. Key responsibilities
7. Company type/industry if mentioned
8. Seniority level (entry/mid/senior/executive)

Be thorough and accurate in extraction.
"""
        
        try:
            job_requirements = self.ai_service.generate_structured_response(
                prompt=extraction_prompt,
                response_model=JobRequirements,
                system_prompt=system_prompt
            )
            return job_requirements
        except Exception as e:
            raise ValueError(f"Failed to parse job requirements: {e}")
    
    def _perform_detailed_analysis(
        self, 
        resume_data: ResumeData, 
        job_requirements: JobRequirements
    ) -> DetailedAnalysis:
        """Perform detailed analysis of resume vs job requirements"""
        
        # Analyze skill matches
        skill_matches = self.analyzer.analyze_skill_matches(
            candidate_skills=resume_data.resume.CandidateOverall.Skills,
            required_skills=job_requirements.required_skills,
            preferred_skills=job_requirements.preferred_skills
        )
        
        # Analyze experience matches
        experience_matches = self.analyzer.analyze_experience_matches(
            resume_data=resume_data,
            experience_requirements=job_requirements.experience_requirements
        )
        
        # Analyze education match
        education_match = self.analyzer.analyze_education_match(
            resume_data=resume_data,
            education_requirements=job_requirements.education_requirements
        )
        
        # Identify strengths
        strengths = self.analyzer.identify_strengths(resume_data, skill_matches)
        
        # Identify gaps
        gaps = self.analyzer.identify_gaps(skill_matches, experience_matches)
        
        # Generate overall assessment using AI
        overall_assessment = self._generate_overall_assessment(
            resume_data, job_requirements, skill_matches, experience_matches, education_match
        )
        
        return DetailedAnalysis(
            skill_matches=skill_matches,
            experience_matches=experience_matches,
            education_match=education_match,
            strengths=strengths,
            gaps=gaps,
            overall_assessment=overall_assessment
        )
    
    def _calculate_overall_score(
        self, 
        resume_data: ResumeData,
        job_requirements: JobRequirements,
        detailed_analysis: DetailedAnalysis,
        component_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """Calculate overall FIT score using AI analysis"""
        
        system_prompt = """
You are an expert recruiter calculating a comprehensive FIT score between a candidate and job position.
Consider all aspects: skills, experience, education, cultural fit, and growth potential.
Provide a score from 0-100 and detailed reasoning.
"""
        
        scoring_prompt = f"""
Calculate the overall FIT score for this candidate-job match:

Job: {job_requirements.title}
Candidate: {resume_data.resume.About.Name}

Component Scores:
- Skills: {component_scores['skill_score']:.1f}/100
- Experience: {component_scores['experience_score']:.1f}/100  
- Education: {component_scores['education_score']:.1f}/100

Detailed Analysis:
- Skill Matches: {len([sm for sm in detailed_analysis.skill_matches if sm.candidate_has])} matched out of {len(detailed_analysis.skill_matches)}
- Experience Relevance: {detailed_analysis.overall_assessment}
- Strengths: {len(detailed_analysis.strengths)} identified
- Gaps: {len(detailed_analysis.gaps)} identified

Provide:
1. Overall FIT score (0-100)
2. Score category (excellent: 85+, good: 70-84, fair: 50-69, poor: <50)
3. Confidence level (0.0-1.0)
4. Potential score (considering growth potential)
5. Brief summary
6. Hiring recommendation (strongly_recommend/recommend/consider/not_recommend)

Consider both current fit and future potential.
"""
        
        try:
            from pydantic import BaseModel
            
            class OverallScoreResponse(BaseModel):
                score: float
                category: str
                confidence: float
                potential_score: float
                summary: str
                hiring_recommendation: str
            
            response = self.ai_service.generate_structured_response(
                prompt=scoring_prompt,
                response_model=OverallScoreResponse,
                system_prompt=system_prompt
            )
            
            return {
                "score": response.score,
                "category": response.category,
                "confidence": response.confidence,
                "potential_score": response.potential_score,
                "summary": response.summary,
                "hiring_recommendation": response.hiring_recommendation
            }
            
        except Exception as e:
            # Fallback calculation
            weighted_score = (
                component_scores["skill_score"] * 0.4 +
                component_scores["experience_score"] * 0.4 +
                component_scores["education_score"] * 0.2
            )
            
            category = "excellent" if weighted_score >= 85 else "good" if weighted_score >= 70 else "fair" if weighted_score >= 50 else "poor"
            
            return {
                "score": weighted_score,
                "category": category,
                "confidence": 0.7,
                "potential_score": min(100, weighted_score + 10),
                "summary": f"Calculated FIT score of {weighted_score:.1f} based on component analysis",
                "hiring_recommendation": "recommend" if weighted_score >= 70 else "consider"
            }
    
    def _generate_overall_assessment(
        self,
        resume_data: ResumeData,
        job_requirements: JobRequirements,
        skill_matches: List,
        experience_matches: List,
        education_match
    ) -> str:
        """Generate overall assessment text using AI"""
        
        system_prompt = "You are an expert recruiter providing concise assessment of candidate fit."
        
        assessment_prompt = f"""
Provide a brief overall assessment of this candidate for the position:

Position: {job_requirements.title}
Candidate: {resume_data.resume.About.Name} ({resume_data.resume.About.TotalWorkExperience} years experience)

Key Points:
- Required skills coverage: {len([sm for sm in skill_matches if sm.required and sm.candidate_has])}/{len([sm for sm in skill_matches if sm.required])}
- Experience relevance: {sum(em.match_score for em in experience_matches)/len(experience_matches) if experience_matches else 0:.1f}
- Education fit: {education_match.match_score:.1f}

Provide a 2-3 sentence assessment focusing on key strengths and any notable concerns.
"""
        
        try:
            assessment = self.ai_service.generate_text_response(
                prompt=assessment_prompt,
                system_prompt=system_prompt
            )
            return assessment.strip()
        except Exception:
            return "Assessment could not be generated automatically."
    
    def _generate_recommendations(self, detailed_analysis: DetailedAnalysis) -> List[str]:
        """Generate hiring recommendations based on analysis"""
        recommendations = []
        
        # Skill-based recommendations
        missing_skills = [sm for sm in detailed_analysis.skill_matches if sm.required and not sm.candidate_has]
        if missing_skills:
            recommendations.append(f"Consider training for missing skills: {', '.join([sm.skill for sm in missing_skills[:3]])}")
        
        # Experience-based recommendations
        low_exp_matches = [em for em in detailed_analysis.experience_matches if em.match_score < 0.5]
        if low_exp_matches:
            recommendations.append("Provide mentoring for areas with limited experience")
        
        # Strength-based recommendations
        if detailed_analysis.strengths:
            top_strength = detailed_analysis.strengths[0]
            recommendations.append(f"Leverage candidate's strength in {top_strength.category}")
        
        # Gap mitigation
        for gap in detailed_analysis.gaps:
            if gap.mitigation_suggestions:
                recommendations.extend(gap.mitigation_suggestions[:1])  # Add first suggestion
        
        return recommendations[:5]  # Limit to 5 recommendations
