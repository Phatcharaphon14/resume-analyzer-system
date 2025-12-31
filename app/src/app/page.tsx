'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import ResumeUpload from '@/components/resume-upload';
import AnalysisResult from '@/components/analysis-result';
import { analyzeResume } from '@/api/resume-api';
import { Upload, BarChart3, Target } from 'lucide-react';

interface AnalysisData {
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

export default function Home() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    setIsAnalyzing(true);
    setError(null);

    try {
      const result = await analyzeResume(file);
      if (result.success && result.data) {
        setAnalysisData(result.data);
      } else {
        setError(result.error || 'เกิดข้อผิดพลาดในการวิเคราะห์');
      }
    } catch (err) {
      setError('เกิดข้อผิดพลาดในการอัปโหลดไฟล์');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            ระบบวิเคราะห์ Resume
          </h1>
          <p className="text-gray-600">
            วิเคราะห์ความเหมาะสมของ Resume กับตำแหน่ง AI & Data Solution Intern
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Upload & Requirements */}
          <div className="lg:col-span-2 space-y-6">
            {/* Upload Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="h-5 w-5" />
                  อัปโหลด Resume
                </CardTitle>
                <CardDescription>
                  อัปโหลดไฟล์ PDF ของคุณเพื่อวิเคราะห์ความเหมาะสมกับตำแหน่งงาน
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ResumeUpload
                  onFileSelect={handleFileUpload}
                  isLoading={isAnalyzing}
                />
                {error && (
                  <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
                    <p className="text-red-600 text-sm">{error}</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Analysis Results */}
            {analysisData && (
              <AnalysisResult data={analysisData} />
            )}
          </div>

          {/* Right Column - Job Description & Stats */}
          <div className="space-y-6">
            {/* Job Description Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5" />
                  ตำแหน่งงานที่ต้องการ
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold text-lg text-blue-600">
                      AI & Data Solution Intern
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      นักศึกษาฝึกงานด้าน AI และ Data Solution
                    </p>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">
                      คุณสมบัติที่ต้องการ
                    </h4>
                    <ul className="space-y-2 text-sm">
                      <li className="flex items-start gap-2">
                        <div className="h-1.5 w-1.5 bg-blue-500 rounded-full mt-1.5" />
                        <span>Computer Science / Data Science / AI</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-1.5 w-1.5 bg-blue-500 rounded-full mt-1.5" />
                        <span>Python Programming</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-1.5 w-1.5 bg-blue-500 rounded-full mt-1.5" />
                        <span>Machine Learning Fundamentals</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <div className="h-1.5 w-1.5 bg-blue-500 rounded-full mt-1.5" />
                        <span>Data Analysis Skills</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Overall Match Score */}
            {analysisData && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    คะแนนรวม
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-5xl font-bold text-gray-900 mb-2">
                      {analysisData.match_percentage}%
                    </div>
                    <p className="text-gray-600 mb-4">
                      ความเหมาะสมกับตำแหน่งงาน
                    </p>
                    <Progress value={analysisData.match_percentage} className="h-2" />
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}