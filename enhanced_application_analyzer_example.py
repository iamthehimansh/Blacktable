"""
Enhanced example usage of ApplicationAnalyzer with Resume data integration
"""

from blacktable import ApplicationAnalyzer
from blacktable.resume_parser.models import (
    Resume, About, WorkExperience, Education, Project, 
    CandidateOverall, Location, Timeline
)
import json


def create_sample_resume():
    """Create a sample resume object for demonstration"""
    
    # Create About section
    about = About(
        Name="John Doe",
        Mobile="+1-555-0123",
        Email="john.doe@email.com",
        Linkedin="https://linkedin.com/in/johndoe",
        About="Senior Python Developer with 6 years of experience in web development, API design, and cloud technologies.",
        TotalWorkExperience=6
    )
    
    # Create Work Experience
    work_exp1 = WorkExperience(
        ID=1,
        Title="Senior Python Developer",
        Company="TechCorp Inc.",
        Location=Location(City="San Francisco", Country="USA"),
        Experience="3 years",
        Skills=["Python", "Django", "PostgreSQL", "AWS", "Docker"],
        Type="Full-time",
        Timeline=Timeline(Start="2022-01", End="Present"),
        Description=[
            "Led development of high-traffic e-commerce platform serving 10,000+ concurrent users",
            "Implemented microservices architecture using Django and Docker",
            "Optimized database queries resulting in 40% performance improvement",
            "Mentored team of 3 junior developers"
        ]
    )
    
    work_exp2 = WorkExperience(
        ID=2,
        Title="Python Developer",
        Company="StartupXYZ",
        Location=Location(City="San Francisco", Country="USA"),
        Experience="3 years",
        Skills=["Python", "Flask", "MongoDB", "Redis", "API Development"],
        Type="Full-time",
        Timeline=Timeline(Start="2019-06", End="2021-12"),
        Description=[
            "Developed REST APIs using Flask for mobile and web applications",
            "Implemented caching strategies with Redis for improved performance",
            "Built automated testing frameworks with pytest",
            "Collaborated with front-end team on API integration"
        ]
    )
    
    # Create Education
    education = Education(
        ID=1,
        College="University of California, Berkeley",
        Degree="Bachelor's",
        Course="Computer Science",
        Timeline=Timeline(Start="2015-08", End="2019-05"),
        Duration=4,
        CGPA=3.7
    )
    
    # Create Projects
    project1 = Project(
        ID=1,
        Title="E-commerce Analytics Dashboard",
        Company="TechCorp Inc.",
        Role="Lead Developer",
        Duration="6 months",
        Skills=["Python", "Django", "React", "PostgreSQL", "Chart.js"],
        Description=[
            "Built comprehensive analytics dashboard for e-commerce platform",
            "Implemented real-time data visualization using Chart.js",
            "Designed efficient database schema for analytics data storage"
        ]
    )
    
    project2 = Project(
        ID=2,
        Title="Microservices Migration",
        Company="TechCorp Inc.",
        Role="Senior Developer",
        Duration="8 months",
        Skills=["Python", "Docker", "Kubernetes", "AWS", "MongoDB"],
        Description=[
            "Migrated monolithic application to microservices architecture",
            "Implemented container orchestration with Kubernetes",
            "Set up CI/CD pipelines for automated deployment"
        ]
    )
    
    # Create Candidate Overall
    candidate_overall = CandidateOverall(
        Skills=["Python", "Django", "Flask", "PostgreSQL", "MongoDB", "AWS", "Docker", "Kubernetes", "API Development", "Microservices"],
        LookingFor="Senior leadership roles in Python development with focus on scalable systems",
        Achievements=["AWS Certified Developer", "Led successful microservices migration", "Mentored 5+ junior developers"],
        Certificates="AWS Certified Developer, Python Institute Certified Associate Programmer"
    )
    
    # Create complete Resume
    resume = Resume(
        About=about,
        WorkExperience=[work_exp1, work_exp2],
        Projects=[project1, project2],
        Education=[education],
        CandidateOverall=candidate_overall,
        Publications=[],
        Weblinks=[]
    )
    
    return resume


def main():
    """Demonstrate ApplicationAnalyzer with resume data"""
    
    print("🚀 Enhanced BlackTable Application Analyzer Demo with Resume Data")
    print("=" * 70)
    
    # Initialize the analyzer
    analyzer = ApplicationAnalyzer(ai_provider="openai")
    
    # Create sample resume
    sample_resume = create_sample_resume()
    
    # Job requirements
    job_title = "Senior Python Developer"
    job_description = """
    We are seeking a Senior Python Developer to join our growing engineering team.
    
    Key Responsibilities:
    - Design and develop scalable web applications using Python
    - Lead API development and microservices architecture
    - Mentor junior developers and contribute to technical decisions
    - Optimize application performance and database queries
    - Collaborate with DevOps team on deployment strategies
    
    Required Skills:
    - 5+ years of Python development experience
    - Strong experience with Django or Flask
    - Database experience with PostgreSQL or MongoDB
    - Cloud platform experience (AWS preferred)
    - API development and microservices architecture
    - Leadership and mentoring experience
    
    Preferred Skills:
    - Docker and Kubernetes experience
    - Experience with high-traffic applications
    - AWS certifications
    - Agile development methodologies
    """
    
    salary_range = "$90,000 - $130,000"
    
    # Pre-screening questions and responses
    prescreening_questions = [
        "How many years of Python development experience do you have?",
        "Describe your experience with microservices architecture",
        "Have you led or mentored other developers?",
        "What's your experience with cloud platforms?",
        "Why are you interested in this senior role?"
    ]
    
    prescreening_responses = {
        "How many years of Python development experience do you have?": 
            "I have 6 years of professional Python development experience, working with both Django and Flask frameworks.",
        
        "Describe your experience with microservices architecture": 
            "I led a major microservices migration project at my current company, moving from a monolithic Django application to a containerized microservices architecture using Docker and Kubernetes.",
        
        "Have you led or mentored other developers?": 
            "Yes, I currently mentor a team of 3 junior developers and have mentored 5+ developers throughout my career. I enjoy teaching and helping others grow.",
        
        "What's your experience with cloud platforms?": 
            "I'm AWS Certified Developer with extensive experience deploying applications on AWS. I've worked with EC2, RDS, S3, Lambda, and container services.",
        
        "Why are you interested in this senior role?": 
            "I'm looking for opportunities to take on more technical leadership responsibilities and work on challenging scalability problems. Your company's focus on innovation aligns with my career goals."
    }
    
    # Application details
    current_ctc = "$85,000"
    expected_ctc = "$110,000"
    notice_period = "1 month"
    
    additional_fields = {
        "years_of_experience": "6",
        "current_location": "San Francisco, CA",
        "willing_to_relocate": "Yes",
        "preferred_work_mode": "Hybrid",
        "github_profile": "https://github.com/johndoe",
        "portfolio_website": "https://johndoe.dev",
        "technical_certifications": "AWS Certified Developer, Python Institute Certified",
        "availability_for_interview": "Available weekdays after 5 PM PST"
    }
    
    print("🔍 Analyzing comprehensive job application with resume data...")
    print("=" * 70)
    
    try:
        # Perform comprehensive analysis with resume data
        result = analyzer.analyze_application(
            job_title=job_title,
            job_description=job_description,
            salary_range=salary_range,
            prescreening_questions=prescreening_questions,
            prescreening_responses=prescreening_responses,
            current_ctc=current_ctc,
            expected_ctc=expected_ctc,
            notice_period=notice_period,
            additional_fields=additional_fields,
            resume=sample_resume  # Enhanced with resume data
        )
        
        # Display comprehensive results
        print(f"📊 AI SCORE: {result.ai_score}/100")
        print(f"🎯 RECOMMENDATION: {result.overall_recommendation.upper()}")
        print(f"🔬 CONFIDENCE: {result.confidence_level.upper()}")
        print()
        
        print("✅ WHY CANDIDATE MATCHES:")
        print("-" * 40)
        for category, items in [
            ("Skills", result.why_match.skill_matches),
            ("Experience", result.why_match.experience_matches),
            ("Cultural Fit", result.why_match.cultural_fit),
            ("Growth Potential", result.why_match.growth_potential)
        ]:
            if items:
                print(f"{category}: {', '.join(items[:3])}")  # Show first 3 items
        print()
        
        print("⚠️  POTENTIAL CONCERNS:")
        print("-" * 40)
        for category, items in [
            ("Skill Gaps", result.why_not_match.skill_gaps),
            ("Experience Gaps", result.why_not_match.experience_gaps),
            ("Salary Concerns", result.why_not_match.salary_mismatch),
            ("Other Concerns", result.why_not_match.other_concerns)
        ]:
            if items:
                print(f"{category}: {', '.join(items[:2])}")  # Show first 2 items
        print()
        
        print("👤 EXTRACTED CANDIDATE PROFILE:")
        print("-" * 40)
        print(f"About: {result.candidate_profile.about}")
        print(f"Skills: {', '.join(result.candidate_profile.skills[:8])}")  # First 8 skills
        print(f"Experience: {', '.join(result.candidate_profile.experience[:3])}")  # First 3 experiences
        print(f"Previous Jobs: {', '.join(result.candidate_profile.previous_jobs)}")
        print(f"Education: {', '.join(result.candidate_profile.college)}")
        print()
        
        print("📋 EXECUTIVE SUMMARY:")
        print("-" * 40)
        print(result.executive_summary)
        print()
        
        print("🎯 KEY HIGHLIGHTS:")
        print("-" * 40)
        for i, highlight in enumerate(result.key_highlights, 1):
            print(f"{i}. {highlight}")
        print()
        
        print("📝 NEXT STEPS:")
        print("-" * 40)
        for i, step in enumerate(result.next_steps, 1):
            print(f"{i}. {step}")
        print()
        
        print("🎤 INTERVIEW FOCUS AREAS:")
        print("-" * 40)
        for i, area in enumerate(result.interview_focus_areas, 1):
            print(f"{i}. {area}")
        print()
        
        # Save detailed results
        output_data = {
            "job_title": job_title,
            "candidate_name": sample_resume.About.Name if sample_resume.About else "Unknown",
            "analysis_result": result.model_dump(),
            "resume_included": True,
            "timestamp": "2025-06-25"
        }
        
        with open("enhanced_application_analysis.json", "w") as f:
            json.dump(output_data, f, indent=2, default=str)
        
        print("💾 Enhanced analysis saved to 'enhanced_application_analysis.json'")
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        print("Please check your AI service configuration and try again.")




if __name__ == "__main__":
    # Run enhanced demo with resume data
    main()
    

    
    print("\n✨ Enhanced demo completed! Resume data integration successful.")
