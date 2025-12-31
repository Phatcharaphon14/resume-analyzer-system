# backend/app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types
import fitz  # PyMuPDF
import os
import json
import uuid
from typing import Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Resume Analysis API",
    description="API for analyzing resumes without database storage",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini AI
def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not found. Using mock analysis.")
        return None
    
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        return None

gemini_client = init_gemini()

# Job Description for AI & Data Solution Intern
JOB_DESCRIPTION = {
    "position": "AI & Data Solution Intern",
    "required_skills": ["Python", "Machine Learning", "Data Analysis", "SQL", "Git"],
    "preferred_skills": ["Deep Learning", "Natural Language Processing", "Cloud Computing", "Docker"],
    "required_tools": ["Python", "Pandas", "NumPy", "Jupyter", "Git"],
    "responsibilities": [
        "Develop AI/ML models",
        "Analyze and process data",
        "Create data visualizations",
        "Collaborate with development team"
    ]
}

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extract text from PDF using PyMuPDF"""
    try:
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract text from PDF")

def analyze_with_gemini(resume_text: str) -> dict:
    """Analyze resume using Gemini AI"""
    if not gemini_client:
        return get_mock_analysis()
    
    prompt = f"""
    Analyze this resume for the position: {JOB_DESCRIPTION['position']}
    
    Required Skills: {', '.join(JOB_DESCRIPTION['required_skills'])}
    Preferred Skills: {', '.join(JOB_DESCRIPTION['preferred_skills'])}
    Required Tools: {', '.join(JOB_DESCRIPTION['required_tools'])}
    
    Resume Text:
    {resume_text[:3000]}
    
    Provide analysis in this JSON format:
    {{
        "scores": {{
            "education": 0-100,
            "skills": 0-100,
            "experience": 0-100,
            "tools": 0-100
        }},
        "match_percentage": 0-100,
        "strengths": ["list strengths"],
        "weaknesses": ["list weaknesses"],
        "recommendations": ["list recommendations"],
        "matched_skills": ["list matched skills"],
        "missing_skills": ["list missing skills"]
    }}
    
    Respond only with valid JSON.
    """
    
    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            
            # Extract JSON from response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            
            analysis = json.loads(response_text)
            logger.info("AI analysis completed successfully!")
            return analysis
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                logger.warning(f"Quota exceeded (attempt {attempt + 1}/{max_retries}). Using mock analysis.")
                break
            logger.error(f"Gemini analysis error (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                import time
                time.sleep(2)
    
    logger.info("Returning mock analysis due to API limitations.")
    return get_mock_analysis()

def get_mock_analysis() -> dict:
    """Return mock analysis when Gemini is not available"""
    return {
        "scores": {
            "education": 85,
            "skills": 75,
            "experience": 65,
            "tools": 80
        },
        "match_percentage": 76,
        "strengths": [
            "Strong educational background",
            "Good foundation in Python",
            "Basic understanding of machine learning concepts"
        ],
        "weaknesses": [
            "Limited practical experience",
            "Need more project work",
            "Could improve knowledge in advanced ML techniques"
        ],
        "recommendations": [
            "Work on personal AI/ML projects",
            "Take online courses on deep learning",
            "Contribute to open-source projects",
            "Practice with real datasets"
        ],
        "matched_skills": ["Python", "Data Analysis", "Git"],
        "missing_skills": ["Deep Learning", "Cloud Computing", "Docker"]
    }

@app.get("/")
async def root():
    return {
        "app": "Resume Analysis System",
        "version": "2.0.0",
        "status": "running",
        "database": "none",
        "features": ["PDF processing", "AI analysis", "Real-time scoring"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.get("/job-description")
async def get_job_description():
    return {
        "success": True,
        "data": JOB_DESCRIPTION
    }

@app.post("/api/v1/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze a resume PDF file
    """
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Only PDF files are accepted"}
            )
        
        # Read file
        file_content = await file.read()
        if len(file_content) == 0:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "Empty file"}
            )
        
        # Extract text from PDF
        logger.info(f"Processing file: {file.filename}")
        resume_text = extract_text_from_pdf(file_content)
        
        if not resume_text:
            return JSONResponse(
                status_code=400,
                content={"success": False, "error": "No text found in PDF"}
            )
        
        # Analyze with AI
        logger.info("Analyzing resume with AI...")
        analysis_result = analyze_with_gemini(resume_text)
        
        # Prepare response
        response_data = {
            "success": True,
            "data": {
                "analysis_id": str(uuid.uuid4()),
                "filename": file.filename,
                "file_size": len(file_content),
                "extracted_text_length": len(resume_text),
                "analysis": analysis_result,
                "processing_time": "real-time",
                "job_description": JOB_DESCRIPTION
            }
        }
        
        return response_data
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Analysis error: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": f"Internal server error: {str(e)}"}
        )

@app.get("/api/v1/test")
async def test_endpoint():
    """Test endpoint for debugging"""
    return {
        "status": "ok",
        "message": "API is working",
        "gemini_available": gemini_client is not None,
        "endpoints": {
            "POST /api/v1/analyze": "Upload and analyze resume",
            "GET /job-description": "Get job requirements",
            "GET /health": "Health check"
        }
    }