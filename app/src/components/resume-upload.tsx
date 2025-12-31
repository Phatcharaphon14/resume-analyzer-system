'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from '@/components/ui/button';
import { Upload, FileText, X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ResumeUploadProps {
    onFileSelect: (file: File) => void;
    isLoading: boolean;
}

export default function ResumeUpload({ onFileSelect, isLoading }: ResumeUploadProps) {
    const [file, setFile] = useState<File | null>(null);
    const [dragOver, setDragOver] = useState(false);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        const selectedFile = acceptedFiles[0];
        if (selectedFile && selectedFile.type === 'application/pdf') {
            setFile(selectedFile);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf']
        },
        multiple: false,
        onDragEnter: () => setDragOver(true),
        onDragLeave: () => setDragOver(false)
    });

    const handleUpload = () => {
        if (file) {
            onFileSelect(file);
        }
    };

    const handleRemove = () => {
        setFile(null);
    };

    return (
        <div className="space-y-4">
            <div
                {...getRootProps()}
                className={cn(
                    "border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors",
                    dragOver || isDragActive
                        ? "border-blue-500 bg-blue-50"
                        : "border-gray-300 hover:border-gray-400",
                    file && "border-green-500 bg-green-50"
                )}
            >
                <input {...getInputProps()} />

                {file ? (
                    <div className="flex flex-col items-center">
                        <FileText className="h-12 w-12 text-green-500 mb-3" />
                        <p className="font-medium text-gray-900">{file.name}</p>
                        <p className="text-sm text-gray-500 mt-1">
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={(e) => {
                                e.stopPropagation();
                                handleRemove();
                            }}
                            className="mt-3"
                        >
                            <X className="h-4 w-4 mr-2" />
                            ลบไฟล์
                        </Button>
                    </div>
                ) : (
                    <div className="flex flex-col items-center">
                        <Upload className="h-12 w-12 text-gray-400 mb-3" />
                        <p className="font-medium text-gray-900 mb-1">
                            ลากไฟล์มาวางที่นี่ หรือคลิกเพื่อเลือกไฟล์
                        </p>
                        <p className="text-sm text-gray-500">
                            รองรับเฉพาะไฟล์ PDF เท่านั้น
                        </p>
                    </div>
                )}
            </div>

            <Button
                onClick={handleUpload}
                disabled={!file || isLoading}
                className="w-full"
                size="lg"
            >
                {isLoading ? (
                    <>
                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent mr-2" />
                        กำลังวิเคราะห์...
                    </>
                ) : (
                    <>
                        <Upload className="h-4 w-4 mr-2" />
                        วิเคราะห์ Resume
                    </>
                )}
            </Button>
        </div>
    );
}