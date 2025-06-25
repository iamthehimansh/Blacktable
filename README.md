# BlackTable

## AI-Powered Recruitment Toolkit

BlackTable is an advanced recruitment toolkit that leverages AI to automate and enhance various aspects of the hiring process. It helps recruiters and hiring managers make data-driven decisions by providing detailed analysis of resumes, generating tailored interview questions, calculating fit scores, and analyzing job applications.

![BlackTable Logo](./blacktable.png)

## Features

### Resume Parser
- Extract structured data from resumes in PDF, DOCX, DOC, and TXT formats
- Parse personal information, work experience, education, skills, projects, and more
- Generate standardized resume data for consistent evaluation

### Question Generator
- Generate standard interview questions based on job descriptions
- Create personalized questions tailored to a candidate's resume
- Support for different interview rounds (screening, technical, behavioral, final, HR)
- Customize focus areas and difficulty levels

### FIT Score Matcher
- Calculate candidate-job fit score (0-100)
- Identify candidate strengths and gaps
- Generate detailed analysis of skill matches, experience, and education
- Provide recommendations for hiring decisions

### Application Analyzer
- Comprehensive analysis of complete job applications
- Process pre-screening question responses
- Generate AI-powered recommendations with confidence levels
- Highlight key aspects for interviewers to focus on

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone the repository:
```bash
git clone https://github.com/iamthehimansh/Blacktable.git
cd Blacktable
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# For OpenAI API
export OPENAI_API_KEY="your-openai-api-key"

# For Anthropic API (optional)
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

## Usage

### Starting the API Server
Run the following command to start the API server:
```bash
python start_api.py
```

This will start the server at http://0.0.0.0:8000 with the interactive GUI accessible at the root URL.

### Using the Python Modules

#### Resume Parsing
```python
from blacktable.resume_parser import ResumeParser

# Initialize the parser
parser = ResumeParser()

# Parse a resume file
resume_data = parser.parse_resume("path/to/resume.pdf")

# Or parse from text
text_resume = """John Doe
Software Engineer
Email: john.doe@email.com
"""
resume_data = parser.parse_resume_from_text(text_resume)
```

#### Question Generation
```python
from blacktable.question_generator import QuestionGenerator

# Initialize the generator
generator = QuestionGenerator()

# Generate standard questions
questions = generator.generate_standard_questions(
    job_description="We are looking for a Python developer...",
    interview_round="technical",
    focus_area="backend development",
    question_count=5
)

# Generate personalized questions (requires resume_data)
personalized_questions = generator.generate_personalized_questions(
    resume_data=resume_data,
    job_description="We are looking for a Python developer...",
    interview_round="technical",
    question_count=3
)
```

#### FIT Score Calculation
```python
from blacktable.fit_score import FITScoreMatcher

# Initialize the matcher
matcher = FITScoreMatcher()

# Calculate fit score
fit_result = matcher.calculate_fit_score(
    resume_data=resume_data,
    job_description="Senior Python Developer with 5+ years..."
)

# Access results
print(f"FIT Score: {fit_result.score}/100")
print(f"Category: {fit_result.category}")
print(f"Strengths: {fit_result.strengths}")
print(f"Gaps: {fit_result.gaps}")
```

#### Application Analysis
```python
from blacktable.application_analyzer import ApplicationAnalyzer

# Initialize the analyzer
analyzer = ApplicationAnalyzer()

# Analyze application
result = analyzer.analyze_application(
    job_title="Senior Python Developer",
    job_description="We are looking for an experienced...",
    salary_range="$120,000 - $150,000",
    prescreening_questions=["How many years of Python experience do you have?"],
    prescreening_responses={"How many years...": "I have 7 years of experience"},
    current_ctc="$110,000",
    expected_ctc="$130,000",
    notice_period="2 weeks",
    resume=resume_data.resume
)

# Access results
print(f"AI Score: {result.ai_score}")
print(f"Recommendation: {result.overall_recommendation}")
print(f"Key Highlights: {result.key_highlights}")
```

## API Reference

The BlackTable API provides endpoints for all core features. An interactive GUI is available at the root URL.

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/parse-resume` | POST | Parse a resume file |
| `/api/generate-questions` | POST | Generate standard interview questions |
| `/api/generate-personalized-questions` | POST | Generate personalized interview questions |
| `/api/calculate-fit-score` | POST | Calculate FIT score between resume and job |
| `/api/analyze-application` | POST | Analyze complete job application |

For full API documentation, visit http://localhost:8000/docs after starting the server.

## Testing

BlackTable includes comprehensive tests for all modules. Run the tests using pytest:

```bash
pytest tests/
```

### Test Files
- `test_resume_parser.py` - Tests for the Resume Parser module
- `test_question_generator.py` - Tests for the Question Generator module
- `test_fit_score.py` - Tests for the FIT Score module
- `test_application_analyzer.py` - Tests for the Application Analyzer module

## Project Structure

```
BlackTable/
├── api/                    # FastAPI API implementation
│   ├── main.py            # Main API routes
│   └── static/            # Static files for GUI
├── blacktable/             # Core modules
│   ├── resume_parser/     # Resume parsing functionality
│   ├── question_generator/ # Question generation functionality
│   ├── fit_score/         # FIT score calculation
│   ├── application_analyzer/ # Application analysis
│   └── core/              # Shared core functionality
├── tests/                  # Test files
└── start_api.py            # Server startup script
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- OpenAI API for powering the AI functionality
- FastAPI for the web framework
- Docling for document processing capabilities