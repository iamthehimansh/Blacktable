"""
BlackTable - AI-Powered Recruitment Module
Main testing script for all components
"""

import os
import sys
from pathlib import Path

# Add the blacktable module to the path
sys.path.insert(0, str(Path(__file__).parent))

from blacktable.resume_parser import ResumeParser
from blacktable.question_generator import QuestionGenerator
from blacktable.fit_score import FITScoreMatcher


def test_resume_parser():
    """Test Resume Parser component"""
    print("🔍 Testing Resume Parser...")
    
    try:
        parser = ResumeParser()
        
        # Test with existing PDF if available
        pdf_path = "Himansh_CV.pdf"
        if os.path.exists(pdf_path):
            print(f"  📄 Parsing PDF: {pdf_path}")
            test_resume = parser.parse_resume(pdf_path)
            print(f"  ✅ Resume Parser Test - Name: {test_resume.resume.About.Name}")
            print(f"  📊 Experience: {test_resume.resume.About.TotalWorkExperience} years")
            print(f"  🎯 Skills: {', '.join(test_resume.resume.CandidateOverall.Skills[:5])}")
            return test_resume
        else:
            # Test with sample text
            print("  📝 Testing with sample text resume...")
            sample_resume = """
            John Doe
            Senior Software Engineer
            Email: john.doe@example.com
            Phone: +1-234-567-8900
            LinkedIn: https://linkedin.com/in/johndoe
            
            EXPERIENCE:
            Senior Software Engineer at TechCorp (2020-Present)
            - Led development of microservices architecture using Python and Django
            - Implemented CI/CD pipelines reducing deployment time by 60%
            - Mentored 3 junior developers and conducted code reviews
            Skills: Python, Django, AWS, Docker, Kubernetes
            
            Software Engineer at StartupXYZ (2018-2020)
            - Developed REST APIs serving 1M+ daily requests
            - Optimized database queries improving performance by 40%
            Skills: Python, Flask, PostgreSQL, Redis
            
            PROJECTS:
            E-commerce Platform (2021)
            - Built scalable e-commerce platform handling 10k+ concurrent users
            - Technologies: Python, Django, PostgreSQL, AWS, Docker
            
            EDUCATION:
            Bachelor of Computer Science
            Massachusetts Institute of Technology (2014-2018)
            CGPA: 3.8/4.0
            
            SKILLS:
            Python, Django, Flask, JavaScript, AWS, Docker, Kubernetes, PostgreSQL, Redis, Git
            
            ACHIEVEMENTS:
            - AWS Certified Developer Associate
            - Led team that won company hackathon 2021
            - Speaker at PyCon 2022
            """
            
            test_resume = parser.parse_resume_from_text(sample_resume)
            print(f"  ✅ Resume Parser Test - Name: {test_resume.resume.About.Name}")
            print(f"  📊 Experience: {test_resume.resume.About.TotalWorkExperience} years")
            print(f"  🎯 Skills: {', '.join(test_resume.resume.CandidateOverall.Skills[:5])}")
            return test_resume
            
    except Exception as e:
        print(f"  ❌ Resume Parser Test Failed: {e}")
        return None


def test_question_generator(resume_data=None):
    """Test Question Generator component"""
    print("\n❓ Testing Question Generator...")
    
    try:
        generator = QuestionGenerator()
        
        job_description = """
        Senior Python Developer Position
        
        We are looking for an experienced Python developer to join our backend team.
        
        Requirements:
        - 5+ years of Python development experience
        - Strong experience with Django or Flask frameworks
        - Experience with AWS cloud services
        - Knowledge of Docker and containerization
        - Experience with PostgreSQL or similar databases
        - Understanding of microservices architecture
        - Experience with CI/CD pipelines
        
        Responsibilities:
        - Design and develop scalable backend services
        - Collaborate with frontend team on API design
        - Optimize application performance and scalability
        - Mentor junior developers
        - Participate in code reviews and technical discussions
        
        Nice to have:
        - Experience with Kubernetes
        - Knowledge of Redis or other caching solutions
        - Experience with message queues (RabbitMQ, Celery)
        - DevOps experience
        """
        
        # Test standard questions
        print("  📋 Generating standard questions...")
        test_questions = generator.generate_standard_questions(
            job_description=job_description,
            interview_round="technical",
            focus_area="backend development",
            question_count=5
        )
        print(f"  ✅ Standard Questions Generated: {len(test_questions)}")
        if test_questions:
            print(f"  📝 Sample Question: {test_questions[0].text[:100]}...")
        
        # Test personalized questions if resume data is available
        if resume_data:
            print("  🎯 Generating personalized questions...")
            personalized_questions = generator.generate_personalized_questions(
                resume_data=resume_data,
                job_description=job_description,
                interview_round="technical",
                question_count=3
            )
            print(f"  ✅ Personalized Questions Generated: {len(personalized_questions)}")
            if personalized_questions:
                print(f"  📝 Sample Personalized Question: {personalized_questions[0].text[:100]}...")
            
            # Test mixed question set
            print("  🔀 Generating mixed question set...")
            mixed_set = generator.generate_mixed_question_set(
                resume_data=resume_data,
                job_description=job_description,
                interview_round="technical",
                focus_area="backend development",
                total_questions=10,
                personalized_ratio=0.3
            )
            print(f"  ✅ Mixed Question Set: {mixed_set.total_questions} total")
            print(f"     - Standard: {mixed_set.standard_questions_count}")
            print(f"     - Personalized: {mixed_set.personalized_questions_count}")
            
            return len(test_questions) + len(personalized_questions)
        else:
            return len(test_questions)
            
    except Exception as e:
        print(f"  ❌ Question Generator Test Failed: {e}")
        return 0


def test_fit_score(resume_data=None):
    """Test FIT_Score component"""
    print("\n🎯 Testing FIT_Score Matcher...")
    
    try:
        matcher = FITScoreMatcher()
        
        job_description = """
        Senior Python Developer Position
        
        We are seeking a seasoned Python developer with expertise in backend development.
        
        Required Qualifications:
        - 5+ years of professional Python development experience
        - Strong experience with Django framework
        - Proficiency in PostgreSQL database design and optimization
        - Experience with AWS cloud services (EC2, S3, RDS)
        - Knowledge of Docker containerization
        - Understanding of RESTful API design principles
        - Experience with Git version control
        - Bachelor's degree in Computer Science or related field
        
        Preferred Qualifications:
        - Experience with Kubernetes orchestration
        - Knowledge of Redis caching
        - Experience with CI/CD pipelines
        - Leadership and mentoring experience
        - Open source contributions
        
        About the Role:
        You will be responsible for designing and implementing scalable backend services,
        optimizing application performance, and mentoring junior team members.
        """
        
        if resume_data:
            print("  🔍 Calculating FIT score...")
            test_score = matcher.calculate_fit_score(
                resume_data=resume_data,
                job_description=job_description
            )
            
            print(f"  ✅ FIT Score Calculated: {test_score.score:.1f}/100")
            print(f"  📊 Category: {test_score.category.title()}")
            print(f"  🎯 Confidence: {test_score.confidence:.2f}")
            print(f"  💪 Key Strengths: {len(test_score.strengths)}")
            if test_score.strengths:
                print(f"     - {test_score.strengths[0]}")
            print(f"  🔍 Identified Gaps: {len(test_score.gaps)}")
            if test_score.gaps:
                print(f"     - {test_score.gaps[0]}")
            print(f"  💡 Recommendations: {len(test_score.recommendations)}")
            if test_score.recommendations:
                print(f"     - {test_score.recommendations[0]}")
            
            print(f"\n  📈 Component Scores:")
            print(f"     - Skills: {test_score.skill_score:.1f}/100")
            print(f"     - Experience: {test_score.experience_score:.1f}/100")
            print(f"     - Education: {test_score.education_score:.1f}/100")
            print(f"     - Potential: {test_score.overall_potential_score:.1f}/100")
            
            print(f"\n  🤝 Hiring Recommendation: {test_score.hiring_recommendation.replace('_', ' ').title()}")
            
            return test_score.score
        else:
            print("  ⚠️  No resume data available for FIT score calculation")
            return 0
            
    except Exception as e:
        print(f"  ❌ FIT Score Test Failed: {e}")
        return 0


def main():
    """Main testing function"""
    print("🚀 BlackTable AI-Powered Recruitment Module - Testing Suite")
    print("=" * 60)
    
    # Test Resume Parser
    resume_data = test_resume_parser()
    
    # Test Question Generator
    question_count = test_question_generator(resume_data)
    
    # Test FIT Score
    fit_score = test_fit_score(resume_data)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TESTING SUMMARY")
    print("=" * 60)
    
    if resume_data:
        print(f"✅ Resume Parser: Successfully parsed resume for {resume_data.resume.About.Name}")
    else:
        print("❌ Resume Parser: Failed to parse resume")
    
    if question_count > 0:
        print(f"✅ Question Generator: Generated {question_count} questions")
    else:
        print("❌ Question Generator: Failed to generate questions")
    
    if fit_score > 0:
        print(f"✅ FIT Score: Calculated score of {fit_score:.1f}/100")
    else:
        print("❌ FIT Score: Failed to calculate score")
    
    print("\n🎉 Testing completed!")
    
    if all([resume_data, question_count > 0, fit_score > 0]):
        print("🌟 All components working successfully!")
    else:
        print("⚠️  Some components may need attention. Check your API keys and dependencies.")


if __name__ == "__main__":
    main()
