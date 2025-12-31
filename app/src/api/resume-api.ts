// Frontend API client for resume analysis

export interface AnalysisResult {
    match_percentage: number;
    scores: {
        education: number;
        skills: number;
        experience: number;
        tools: number;
        overall: number;
    };
    analysis: {
        education_match: string[];
        skills_match: string[];
        skills_missing: string[];
        tools_match: string[];
        tools_missing: string[];
        strengths: string[];
        weaknesses: string[];
    };
    recommendations: string[];
}

export interface ApiResponse {
    success: boolean;
    data?: AnalysisResult;
    error?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function analyzeResume(file: File): Promise<ApiResponse> {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        if (!response.ok) {
            return {
                success: false,
                error: result.error || 'เกิดข้อผิดพลาดในการวิเคราะห์',
            };
        }

        // Transform backend response to match frontend expected format
        if (result.success && result.data) {
            const analysis = result.data.analysis;

            return {
                success: true,
                data: {
                    match_percentage: analysis?.match_percentage || 0,
                    scores: {
                        education: analysis?.scores?.education || 0,
                        skills: analysis?.scores?.skills || 0,
                        experience: analysis?.scores?.experience || 0,
                        tools: analysis?.scores?.tools || 0,
                        overall: analysis?.match_percentage || 0,
                    },
                    analysis: {
                        education_match: [],
                        skills_match: analysis?.matched_skills || [],
                        skills_missing: analysis?.missing_skills || [],
                        tools_match: [],
                        tools_missing: [],
                        strengths: analysis?.strengths || [],
                        weaknesses: analysis?.weaknesses || [],
                    },
                    recommendations: analysis?.recommendations || [],
                },
            };
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        return {
            success: false,
            error: 'ไม่สามารถเชื่อมต่อกับ API ได้',
        };
    }
}
