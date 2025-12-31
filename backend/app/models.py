# backend/app/models.py
from pydantic import BaseModel
from typing import Dict, List, Any, Optional


# Job Description for AI & Data Solution Intern position
JD_AI_DATA_INTERN = {
    "position": "AI & Data Solution Intern",
    "required_education": [
        "Computer Science",
        "Data Science", 
        "Artificial Intelligence",
        "Computer Engineering",
        "Information Technology"
    ],
    "required_skills": [
        "Python",
        "Machine Learning",
        "Data Analysis",
        "Statistics",
        "Problem Solving"
    ],
    "preferred_skills": [
        "Deep Learning",
        "Natural Language Processing",
        "Computer Vision",
        "Big Data",
        "Cloud Computing"
    ],
    "required_tools": [
        "Python",
        "Pandas",
        "NumPy",
        "Jupyter Notebook",
        "Git"
    ],
    "preferred_tools": [
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "Docker",
        "SQL"
    ],
    "responsibilities": [
        "Develop and implement AI/ML models",
        "Analyze and process large datasets",
        "Create data visualizations and reports",
        "Collaborate with development team",
        "Research new AI technologies"
    ]
}


class Scores(BaseModel):
    education: float = 0
    skills: float = 0
    experience: float = 0
    tools: float = 0
    overall: float = 0


class AnalysisDetails(BaseModel):
    education_match: List[str] = []
    skills_match: List[str] = []
    skills_missing: List[str] = []
    tools_match: List[str] = []
    tools_missing: List[str] = []
    experience_relevance: str = ""
    strengths: List[str] = []
    weaknesses: List[str] = []


class ResumeAnalysis(BaseModel):
    resume_id: str
    filename: str
    extracted_text: str
    scores: Dict[str, float]
    analysis_details: Dict[str, Any]
    recommendations: List[str]
    match_percentage: float
    processing_time: float
