"""
FIT_Score analyzer for detailed analysis
"""
from typing import List, Dict, Any
from ..resume_parser.models import ResumeData
from .models import (
    JobRequirements, FITScoreResult, DetailedAnalysis,
    SkillMatch, ExperienceMatch, EducationMatch, 
    Strength, Gap, Recommendation
)


class FITScoreAnalyzer:
    """Detailed analyzer for FIT Score components"""
    
    def __init__(self):
        pass
    
    def analyze_skill_matches(
        self, 
        candidate_skills: List[str], 
        required_skills: List[str], 
        preferred_skills: List[str]
    ) -> List[SkillMatch]:
        """Analyze skill matches between candidate and job requirements"""
        skill_matches = []
        all_job_skills = set(required_skills + preferred_skills)
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        
        for job_skill in all_job_skills:
            is_required = job_skill in required_skills
            candidate_has = any(job_skill.lower() in cs.lower() or cs.lower() in job_skill.lower() 
                             for cs in candidate_skills_lower)
            
            # Simple confidence calculation
            confidence = 0.9 if candidate_has else 0.1
            
            skill_matches.append(SkillMatch(
                skill=job_skill,
                required=is_required,
                candidate_has=candidate_has,
                match_confidence=confidence
            ))
        
        return skill_matches
    
    def analyze_experience_matches(
        self, 
        resume_data: ResumeData, 
        experience_requirements: List[str]
    ) -> List[ExperienceMatch]:
        """Analyze experience matches"""
        experience_matches = []
        candidate_experience = resume_data.resume.WorkExperience
        
        for req in experience_requirements:
            # Simple matching logic - can be enhanced
            best_match_score = 0.0
            best_match_exp = "No relevant experience found"
            
            for exp in candidate_experience:
                # Check if requirement keywords appear in experience
                req_keywords = req.lower().split()
                exp_text = f"{exp.Title} {exp.Company} {' '.join(exp.Description)}".lower()
                
                matches = sum(1 for keyword in req_keywords if keyword in exp_text)
                score = matches / len(req_keywords) if req_keywords else 0
                
                if score > best_match_score:
                    best_match_score = score
                    best_match_exp = f"{exp.Title} at {exp.Company}"
            
            relevance = "high" if best_match_score > 0.7 else "medium" if best_match_score > 0.3 else "low"
            
            experience_matches.append(ExperienceMatch(
                required_experience=req,
                candidate_experience=best_match_exp,
                match_score=best_match_score,
                relevance=relevance
            ))
        
        return experience_matches
    
    def analyze_education_match(
        self, 
        resume_data: ResumeData, 
        education_requirements: str = None
    ) -> EducationMatch:
        """Analyze education match"""
        candidate_education = "No education information"
        match_score = 0.5  # Default neutral score
        is_sufficient = True  # Default to true if no requirements
        
        if resume_data.resume.Education:
            edu = resume_data.resume.Education[0]  # Take highest/first education
            candidate_education = f"{edu.Degree} in {edu.Course} from {edu.College}"
            
            if education_requirements:
                # Simple keyword matching
                req_lower = education_requirements.lower()
                edu_lower = candidate_education.lower()
                
                # Check for degree level matches
                if any(level in req_lower for level in ["bachelor", "master", "phd", "doctorate"]):
                    if any(level in edu_lower for level in ["bachelor", "master", "phd", "doctorate"]):
                        match_score = 0.8
                    else:
                        match_score = 0.4
                        is_sufficient = False
                
                # Check for field matches
                if any(field in edu_lower for field in ["computer", "engineering", "science", "technology"]):
                    match_score = min(1.0, match_score + 0.2)
        
        return EducationMatch(
            required_education=education_requirements,
            candidate_education=candidate_education,
            match_score=match_score,
            is_sufficient=is_sufficient
        )
    
    def identify_strengths(
        self, 
        resume_data: ResumeData, 
        skill_matches: List[SkillMatch]
    ) -> List[Strength]:
        """Identify candidate strengths"""
        strengths = []
        
        # Skill-based strengths
        matched_skills = [sm for sm in skill_matches if sm.candidate_has and sm.match_confidence > 0.7]
        if matched_skills:
            skill_names = [sm.skill for sm in matched_skills]
            strengths.append(Strength(
                category="skills",
                description=f"Strong technical skills in {', '.join(skill_names[:5])}",
                evidence=[f"Demonstrated experience with {skill}" for skill in skill_names[:3]],
                relevance_score=0.9
            ))
        
        # Experience-based strengths
        total_experience = resume_data.resume.About.TotalWorkExperience
        if total_experience >= 3:
            strengths.append(Strength(
                category="experience",
                description=f"Solid professional experience ({total_experience} years)",
                evidence=[f"Total work experience: {total_experience} years"],
                relevance_score=0.8
            ))
        
        # Project-based strengths
        if resume_data.resume.Projects:
            project_count = len(resume_data.resume.Projects)
            strengths.append(Strength(
                category="projects",
                description=f"Diverse project portfolio ({project_count} projects)",
                evidence=[f"Project: {proj.Title}" for proj in resume_data.resume.Projects[:3]],
                relevance_score=0.7
            ))
        
        return strengths
    
    def identify_gaps(
        self, 
        skill_matches: List[SkillMatch], 
        experience_matches: List[ExperienceMatch]
    ) -> List[Gap]:
        """Identify candidate gaps"""
        gaps = []
        
        # Missing required skills
        missing_required_skills = [
            sm for sm in skill_matches 
            if sm.required and not sm.candidate_has
        ]
        
        if missing_required_skills:
            skill_names = [sm.skill for sm in missing_required_skills]
            gaps.append(Gap(
                category="skills",
                description=f"Missing required skills: {', '.join(skill_names)}",
                severity="critical" if len(skill_names) > 3 else "important",
                mitigation_suggestions=[
                    "Consider training programs or certifications",
                    "Look for transferable skills from related technologies",
                    "Assess learning potential and adaptability"
                ]
            ))
        
        # Low experience matches
        low_exp_matches = [
            em for em in experience_matches 
            if em.match_score < 0.5
        ]
        
        if low_exp_matches:
            gaps.append(Gap(
                category="experience",
                description="Limited relevant experience in some required areas",
                severity="important",
                mitigation_suggestions=[
                    "Evaluate transferable experience",
                    "Consider mentoring and on-the-job training",
                    "Assess growth potential and learning ability"
                ]
            ))
        
        return gaps
    
    def calculate_component_scores(
        self, 
        skill_matches: List[SkillMatch],
        experience_matches: List[ExperienceMatch],
        education_match: EducationMatch
    ) -> Dict[str, float]:
        """Calculate component scores"""
        
        # Skill score
        if skill_matches:
            required_skills = [sm for sm in skill_matches if sm.required]
            if required_skills:
                skill_score = sum(sm.match_confidence for sm in required_skills if sm.candidate_has) / len(required_skills) * 100
            else:
                skill_score = 70.0  # Default if no required skills
        else:
            skill_score = 50.0
        
        # Experience score
        if experience_matches:
            exp_score = sum(em.match_score for em in experience_matches) / len(experience_matches) * 100
        else:
            exp_score = 60.0
        
        # Education score
        edu_score = education_match.match_score * 100
        
        return {
            "skill_score": skill_score,
            "experience_score": exp_score,
            "education_score": edu_score
        }
