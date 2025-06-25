"""
BlackTable API - FastAPI backend for all recruitment modules
"""
import os
import json
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import tempfile
import shutil

# Import BlackTable modules
from blacktable.resume_parser import ResumeParser
from blacktable.question_generator import QuestionGenerator
from blacktable.fit_score import FITScoreMatcher
from blacktable.application_analyzer import ApplicationAnalyzer

app = FastAPI(
    title="BlackTable API",
    description="AI-Powered Recruitment API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
resume_parser = ResumeParser()
question_generator = QuestionGenerator()
fit_score_matcher = FITScoreMatcher()
application_analyzer = ApplicationAnalyzer()

# Mount static files for GUI
app.mount("/static", StaticFiles(directory="api/static"), name="static")


# Pydantic models for request/response
class QuestionGenerationRequest(BaseModel):
    job_description: str
    interview_round: str = "screening"
    focus_area: str = ""
    question_count: int = 10
    difficulty_levels: List[str] = ["medium"]


class ApplicationAnalysisRequest(BaseModel):
    job_title: str
    job_description: str
    salary_range: Optional[str] = None
    prescreening_questions: Optional[List[str]] = None
    prescreening_responses: Optional[Dict[str, str]] = None
    current_ctc: Optional[str] = None
    expected_ctc: Optional[str] = None
    notice_period: Optional[str] = None
    additional_fields: Optional[Dict[str, Any]] = None


# Helper function to save uploaded file temporarily
def save_uploaded_file(uploaded_file: UploadFile) -> str:
    """Save uploaded file temporarily and return path"""
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, uploaded_file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    
    return file_path


@app.get("/", response_class=FileResponse)
async def root():
    """Serve the main GUI page"""
    return FileResponse("api/static/index.html")

# API Endpoints

@app.post("/api/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    """Parse resume and return structured data"""
    try:
        # Save uploaded file temporarily
        file_path = save_uploaded_file(file)
        
        # Parse resume
        resume_data = resume_parser.parse_resume(file_path)
        
        # Clean up temporary file
        os.remove(file_path)
        os.rmdir(os.path.dirname(file_path))
        
        return {"success": True, "data": resume_data.dict()}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Resume parsing failed: {str(e)}")


@app.post("/api/generate-questions")
async def generate_questions(request: QuestionGenerationRequest):
    """Generate standard interview questions"""
    try:
        questions = question_generator.generate_standard_questions(
            job_description=request.job_description,
            interview_round=request.interview_round,
            focus_area=request.focus_area,
            question_count=request.question_count,
            difficulty_levels=request.difficulty_levels
        )
        
        return {"success": True, "data": [q.dict() for q in questions]}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Question generation failed: {str(e)}")


@app.post("/api/generate-personalized-questions")
async def generate_personalized_questions(
    job_description: str = Form(...),
    interview_round: str = Form("screening"),
    question_count: int = Form(5),
    file: UploadFile = File(...)
):
    """Generate personalized interview questions based on resume"""
    try:
        # Save uploaded file temporarily
        file_path = save_uploaded_file(file)
        
        # Parse resume
        resume_data = resume_parser.parse_resume(file_path)
        
        # Generate personalized questions
        questions = question_generator.generate_personalized_questions(
            resume_data=resume_data,
            job_description=job_description,
            interview_round=interview_round,
            question_count=question_count
        )
        
        # Clean up temporary file
        os.remove(file_path)
        os.rmdir(os.path.dirname(file_path))
        
        return {"success": True, "data": [q.dict() for q in questions]}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Personalized question generation failed: {str(e)}")


@app.post("/api/calculate-fit-score")
async def calculate_fit_score(
    job_description: str = Form(...),
    file: UploadFile = File(...)
):
    """Calculate FIT score between resume and job description"""
    try:
        # Save uploaded file temporarily
        file_path = save_uploaded_file(file)
        
        # Parse resume
        resume_data = resume_parser.parse_resume(file_path)
        
        # Calculate FIT score
        fit_score_result = fit_score_matcher.calculate_fit_score(
            resume_data=resume_data,
            job_description=job_description
        )
        
        # Clean up temporary file
        os.remove(file_path)
        os.rmdir(os.path.dirname(file_path))
        
        return {"success": True, "data": fit_score_result.dict()}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"FIT score calculation failed: {str(e)}")


@app.post("/api/analyze-application")
async def analyze_application(
    job_title: str = Form(...),
    job_description: str = Form(...),
    salary_range: Optional[str] = Form(None),
    current_ctc: Optional[str] = Form(None),
    expected_ctc: Optional[str] = Form(None),
    notice_period: Optional[str] = Form(None),
    prescreening_questions: Optional[str] = Form(None),
    prescreening_responses: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    """Analyze complete job application"""
    try:
        # Save uploaded file temporarily
        file_path = save_uploaded_file(file)
        
        # Parse resume
        resume_data = resume_parser.parse_resume(file_path)
        
        # Parse pre-screening data
        parsed_prescreening_questions = None
        parsed_prescreening_responses = None
        
        if prescreening_questions:
            try:
                parsed_prescreening_questions = json.loads(prescreening_questions)
            except json.JSONDecodeError:
                parsed_prescreening_questions = None
        
        if prescreening_responses:
            try:
                parsed_prescreening_responses = json.loads(prescreening_responses)
            except json.JSONDecodeError:
                parsed_prescreening_responses = None
        
        # Analyze application
        analysis_result = application_analyzer.analyze_application(
            job_title=job_title,
            job_description=job_description,
            salary_range=salary_range,
            current_ctc=current_ctc,
            expected_ctc=expected_ctc,
            notice_period=notice_period,
            prescreening_questions=parsed_prescreening_questions,
            prescreening_responses=parsed_prescreening_responses,
            resume=resume_data.resume
        )
        
        # Clean up temporary file
        os.remove(file_path)
        os.rmdir(os.path.dirname(file_path))
        
        return {"success": True, "data": analysis_result.dict()}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Application analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
