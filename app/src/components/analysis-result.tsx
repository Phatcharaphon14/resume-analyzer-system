'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { CheckCircle, XCircle, AlertCircle, TrendingUp } from 'lucide-react';

interface AnalysisResultProps {
    data: {
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
    };
}

export default function AnalysisResult({ data }: AnalysisResultProps) {
    const scoreCategories = [
        { key: 'education', label: 'การศึกษา', value: data.scores.education },
        { key: 'skills', label: 'ทักษะ', value: data.scores.skills },
        { key: 'experience', label: 'ประสบการณ์', value: data.scores.experience },
        { key: 'tools', label: 'เครื่องมือ', value: data.scores.tools },
    ];

    return (
        <div className="space-y-6">
            {/* Score Breakdown */}
            <Card>
                <CardHeader>
                    <CardTitle>ผลการวิเคราะห์รายด้าน</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {scoreCategories.map((category) => (
                            <div key={category.key} className="space-y-2">
                                <div className="flex justify-between items-center">
                                    <span className="font-medium text-gray-700">{category.label}</span>
                                    <span className="font-bold text-gray-900">{category.value}%</span>
                                </div>
                                <Progress value={category.value} className="h-2" />
                                <div className="flex justify-between text-sm text-gray-500">
                                    <span>ต่ำ</span>
                                    <span>สูง</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Skills & Tools Analysis */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Skills Card */}
                <Card>
                    <CardHeader>
                        <CardTitle className="text-lg">ทักษะ</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {/* Matched Skills */}
                        {data.analysis.skills_match.length > 0 && (
                            <div>
                                <h4 className="font-medium text-green-600 mb-2 flex items-center gap-1">
                                    <CheckCircle className="h-4 w-4" />
                                    ทักษะที่มีตรงตามต้องการ
                                </h4>
                                <ul className="space-y-1">
                                    {data.analysis.skills_match.map((skill, index) => (
                                        <li key={index} className="text-sm text-gray-700">
                                            • {skill}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Missing Skills */}
                        {data.analysis.skills_missing.length > 0 && (
                            <div>
                                <h4 className="font-medium text-red-600 mb-2 flex items-center gap-1">
                                    <XCircle className="h-4 w-4" />
                                    ทักษะที่ควรพัฒนาเพิ่ม
                                </h4>
                                <ul className="space-y-1">
                                    {data.analysis.skills_missing.map((skill, index) => (
                                        <li key={index} className="text-sm text-gray-700">
                                            • {skill}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Tools Card */}
                <Card>
                    <CardHeader>
                        <CardTitle className="text-lg">เครื่องมือ</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {/* Matched Tools */}
                        {data.analysis.tools_match.length > 0 && (
                            <div>
                                <h4 className="font-medium text-green-600 mb-2 flex items-center gap-1">
                                    <CheckCircle className="h-4 w-4" />
                                    เครื่องมือที่สามารถใช้งานได้
                                </h4>
                                <ul className="space-y-1">
                                    {data.analysis.tools_match.map((tool, index) => (
                                        <li key={index} className="text-sm text-gray-700">
                                            • {tool}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {/* Missing Tools */}
                        {data.analysis.tools_missing.length > 0 && (
                            <div>
                                <h4 className="font-medium text-red-600 mb-2 flex items-center gap-1">
                                    <XCircle className="h-4 w-4" />
                                    เครื่องมือที่ควรเรียนรู้เพิ่ม
                                </h4>
                                <ul className="space-y-1">
                                    {data.analysis.tools_missing.map((tool, index) => (
                                        <li key={index} className="text-sm text-gray-700">
                                            • {tool}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>

            {/* Recommendations */}
            {data.recommendations.length > 0 && (
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <TrendingUp className="h-5 w-5" />
                            คำแนะนำสำหรับการปรับปรุง
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <ul className="space-y-3">
                            {data.recommendations.map((rec, index) => (
                                <li key={index} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                                    <AlertCircle className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5" />
                                    <span className="text-gray-700">{rec}</span>
                                </li>
                            ))}
                        </ul>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}