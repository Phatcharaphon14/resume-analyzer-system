from typing import Dict, Any, Tuple
import time
from .ocr_service import OCRService
from .gemini_service import GeminiService
from app.models import JD_AI_DATA_INTERN, ResumeAnalysis
import uuid
import logging

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self):
        self.ocr_service = OCRService()
        self.gemini_service = GeminiService()
        
    async def analyze_resume(self, file_content: bytes, filename: str) -> ResumeAnalysis:
        """
        Main analysis pipeline
        """
        start_time = time.time()
        
        try:
            # Step 1: Extract text from PDF
            logger.info("Extracting text from PDF...")
            extracted_text = self.ocr_service.extract_text_from_pdf(file_content)
            
            if not extracted_text:
                raise ValueError("Could not extract text from PDF")
            
            # Step 2: Analyze with Gemini
            logger.info("Analyzing resume with Gemini...")
            analysis_result = self.gemini_service.analyze_resume(
                extracted_text, 
                JD_AI_DATA_INTERN
            )
            
            # Step 3: Calculate overall match percentage
            scores = analysis_result["scores"]
            match_percentage = (
                scores["education"] * 0.25 +
                scores["skills"] * 0.30 +
                scores["experience"] * 0.25 +
                scores["tools"] * 0.20
            )
            
            # Step 4: Create response
            processing_time = time.time() - start_time
            
            resume_analysis = ResumeAnalysis(
                resume_id=str(uuid.uuid4()),
                filename=filename,
                extracted_text=extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text,
                scores=scores,
                analysis_details=analysis_result["analysis_details"],
                recommendations=analysis_result["recommendations"],
                match_percentage=round(match_percentage, 2),
                processing_time=round(processing_time, 2)
            )
            
            return resume_analysis
            
        except Exception as e:
            logger.error(f"Error in analysis pipeline: {e}")
            raise