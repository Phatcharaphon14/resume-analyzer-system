# backend/app/services/ocr_service.py
import io
import fitz  # PyMuPDF
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class OCRService:
    def __init__(self):
        pass
        
    def extract_text_from_pdf(self, pdf_content: bytes) -> Optional[str]:
        """
        Extract text from PDF using PyMuPDF
        """
        try:
            # Open PDF from bytes
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            
            extracted_text = ""
            
            # Process each page
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if text:
                    extracted_text += text + "\n"
            
            doc.close()
            
            return extracted_text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return None