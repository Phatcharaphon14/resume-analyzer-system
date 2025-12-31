import google.generativeai as genai
import os
from typing import Dict, Any, List
import json
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def analyze_resume(self, resume_text: str, jd: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze resume against job description using Gemini
        """
        try:
            prompt = self._create_analysis_prompt(resume_text, jd)
            
            response = self.model.generate_content(prompt)
            
            # Parse the response
            analysis_result = self._parse_gemini_response(response.text)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing resume with Gemini: {e}")
            return self._get_default_analysis()
    
    def _create_analysis_prompt(self, resume_text: str, jd: Dict[str, Any]) -> str:
        """
        Create prompt for Gemini analysis
        """
        prompt = f"""
        วิเคราะห์ Resume ต่อไปนี้สำหรับตำแหน่ง {jd['position']}:
        
        **ตำแหน่งงานที่ต้องการ:** {jd['position']}
        
        **คุณสมบัติที่ต้องการ:**
        - การศึกษา: {', '.join(jd['required_education'])}
        - ทักษะที่ต้องมี: {', '.join(jd['required_skills'])}
        - ทักษะที่ต้องการเพิ่ม: {', '.join(jd['preferred_skills'])}
        - เครื่องมือที่ต้องใช้: {', '.join(jd['required_tools'])}
        - เครื่องมือที่ต้องการเพิ่ม: {', '.join(jd['preferred_tools'])}
        
        **Resume Text:**
        {resume_text[:3000]}  # Limit text length
        
        **กรุณาวิเคราะห์และให้ผลลัพธ์ในรูปแบบ JSON ต่อไปนี้:**
        {{
            "scores": {{
                "education": 0-100,
                "skills": 0-100,
                "experience": 0-100,
                "tools": 0-100,
                "overall": 0-100
            }},
            "analysis_details": {{
                "education_match": ["list of matched education fields"],
                "skills_match": ["list of matched skills"],
                "skills_missing": ["list of missing required skills"],
                "tools_match": ["list of matched tools"],
                "tools_missing": ["list of missing required tools"],
                "experience_relevance": "คำอธิบายความเกี่ยวข้องของประสบการณ์",
                "strengths": ["จุดแข็งของผู้สมัคร"],
                "weaknesses": ["จุดอ่อนที่ควรพัฒนา"]
            }},
            "recommendations": ["คำแนะนำสำหรับการปรับปรุง Resume"],
            "reasoning": "คำอธิบายการให้คะแนนโดยละเอียด"
        }}
        
        **ข้อกำหนด:**
        1. ให้คะแนนแต่ละด้านตามความเหมาะสมกับตำแหน่งงาน
        2. ระบุสิ่งที่ตรงและไม่ตรงกับคุณสมบัติที่ต้องการ
        3. ให้คำแนะนำที่เป็นประโยชน์
        4. ใช้ภาษาไทยในการตอบ
        """
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse Gemini response to structured format
        """
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
            else:
                result = self._get_default_analysis()
                
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing Gemini response: {e}")
            return self._get_default_analysis()
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """
        Return default analysis structure
        """
        return {
            "scores": {
                "education": 0,
                "skills": 0,
                "experience": 0,
                "tools": 0,
                "overall": 0
            },
            "analysis_details": {
                "education_match": [],
                "skills_match": [],
                "skills_missing": [],
                "tools_match": [],
                "tools_missing": [],
                "experience_relevance": "",
                "strengths": [],
                "weaknesses": []
            },
            "recommendations": ["ไม่สามารถวิเคราะห์ Resume ได้ กรุณาตรวจสอบรูปแบบไฟล์"],
            "reasoning": "เกิดข้อผิดพลาดในการวิเคราะห์"
        }