from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.analysis_service import AnalysisService
from app.schemas import AnalysisResponse
import logging

router = APIRouter()
analysis_service = AnalysisService()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze uploaded resume PDF
    """
    try:
        # Check file type
        if not file.filename.lower().endswith('.pdf'):
            return AnalysisResponse(
                success=False,
                error="Only PDF files are allowed"
            )
        
        # Read file content
        file_content = await file.read()
        
        if len(file_content) == 0:
            return AnalysisResponse(
                success=False,
                error="Uploaded file is empty"
            )
        
        # Analyze resume
        analysis_result = await analysis_service.analyze_resume(
            file_content, 
            file.filename
        )
        
        return AnalysisResponse(
            success=True,
            data=analysis_result
        )
        
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        return AnalysisResponse(
            success=False,
            error=str(e)
        )

@router.get("/job-description")
async def get_job_description():
    """
    Get target job description
    """
    from app.models import JD_AI_DATA_INTERN
    return JD_AI_DATA_INTERN