"""
Pydantic models for Resume Parser
"""
from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location model"""
    City: Optional[str] = None
    Country: Optional[str] = None


class Timeline(BaseModel):
    """Timeline model"""
    Start: Optional[str] = None
    End: Optional[str] = None


class About(BaseModel):
    """About section model"""
    Name: Optional[str] = None
    Mobile: Optional[str] = None
    Email: Optional[str] = None
    Linkedin: Optional[str] = None
    About: Optional[str] = None
    TotalWorkExperience: Optional[int] = None

LocationInfo=Location
TimelineInfo=Timeline
class WorkExperience(BaseModel):
    """Work experience model"""
    ID: Optional[int] = None
    Title: Optional[str] = None
    Company: Optional[str] = None
    Location: Optional[LocationInfo] = None
    Experience: Optional[str] = None
    Skills: Optional[List[str]] = Field(default_factory=list)
    Type: Optional[str] = None
    Timeline: Optional[TimelineInfo] = None
    Description: Optional[List[str]] = Field(default_factory=list)


class Project(BaseModel):
    """Project model"""
    ID: Optional[int] = None
    Title: Optional[str] = None
    Client: Optional[str] = None
    Company: Optional[str] = None
    Role: Optional[str] = None
    Location: Optional[str] = None
    Duration: Optional[str] = None
    Skills: Optional[List[str]] = Field(default_factory=list)
    Timeline: Optional[TimelineInfo] = None
    Description: Optional[List[str]] = Field(default_factory=list)


class Education(BaseModel):
    """Education model"""
    ID: Optional[int] = None
    College: Optional[str] = None
    Degree: Optional[str] = None
    Course: Optional[str] = None
    Timeline: Optional[TimelineInfo] = None
    Duration: Optional[int] = None
    CGPA: Optional[float] = None


class CandidateOverall(BaseModel):
    """Candidate overall information model"""
    Skills: Optional[List[str]] = Field(default_factory=list)
    LookingFor: Optional[str] = None
    Hobbies: Optional[str] = None
    Extracurriculars: Optional[str] = None
    Awards: Optional[str] = None
    Achievements: Optional[List[str]] = Field(default_factory=list)
    Certificates: Optional[str] = None


class Weblink(BaseModel):
    """Weblink model"""
    Platform: Optional[str] = None
    Link: Optional[str] = None

AboutInfo=About
WorkExperienceInfo=WorkExperience
EducationInfo=Education
CandidateOverallInfo=CandidateOverall
class Resume(BaseModel):
    """Main resume model"""
    About: Optional[AboutInfo] = None
    WorkExperience: Optional[List[WorkExperienceInfo]] = Field(default_factory=list)
    Projects: Optional[List[Project]] = Field(default_factory=list)
    Publications: Optional[List[str]] = Field(default_factory=list)
    Education: Optional[List[EducationInfo]] = Field(default_factory=list)
    CandidateOverall: Optional[CandidateOverallInfo] = None
    Weblinks: Optional[List[Weblink]] = Field(default_factory=list)


class ResumeData(BaseModel):
    """Root resume data model"""
    resume: Optional[Resume] = None
