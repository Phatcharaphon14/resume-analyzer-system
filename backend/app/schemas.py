# backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional, Dict, List, Any


class AnalysisData(BaseModel):
    """Analysis data model for response"""
    analysis_id: Optional[str] = None
    filename: Optional[str] = None
    file_size: Optional[int] = None
    extracted_text_length: Optional[int] = None
    analysis: Optional[Dict[str, Any]] = None
    processing_time: Optional[str] = None
    job_description: Optional[Dict[str, Any]] = None


class AnalysisResponse(BaseModel):
    """Response model for resume analysis"""
    success: bool
    data: Optional[AnalysisData] = None
    error: Optional[str] = None
