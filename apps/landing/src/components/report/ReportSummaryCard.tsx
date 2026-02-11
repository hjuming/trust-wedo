import React from 'react';

interface ReportSummaryCardProps {
    score: number;
    grade: string;
    worstDimension: { name: string; score: number; max: number };
}

export function ReportSummaryCard({ score, grade, worstDimension }: ReportSummaryCardProps) {
    const gradeColor =
        grade === 'A' ? 'bg-green-500' :
            grade === 'B' ? 'bg-blue-500' :
                grade === 'C' ? 'bg-yellow-500' :
                    'bg-red-500';

    // 翻譯維度名稱
    const translateDimension = (key: string) => {
        const map: Record<string, string> = {
            'discoverability': 'AI 可發現性',
            'identity': '身分可信度',
            'structure': '內容結構化',
            'social': '社群信任',
            'technical': '技術基礎'
        };
        return map[key] || key;
    };

    const dimensionName = translateDimension(worstDimension.name);
    const dimensionPercentage = Math.round((worstDimension.score / worstDimension.max) * 100);

    return (
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 rounded-xl shadow-sm overflow-hidden mb-8">
            <div className="p-6 md:p-8">
                <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                    <div className="space-y-2 text-center md:text-left">
                        <div className="flex items-baseline justify-center md:justify-start space-x-4">
                            <h1 className="text-6xl font-bold text-gray-900 tracking-tight">{score}<span className="text-2xl text-gray-400 font-medium">/100</span></h1>
                            <span className={`${gradeColor} text-white px-4 py-1.5 rounded-full text-lg font-bold shadow-sm`}>等級 {grade}</span>
                        </div>
                        <p className="text-gray-500 font-medium text-lg">AI 信任度總體評分</p>
                    </div>

                    <div className="flex flex-col items-center md:items-end space-y-2 bg-white/60 p-4 rounded-lg border border-blue-100/50 backdrop-blur-sm shadow-sm md:min-w-[280px]">
                        <p className="text-gray-500 text-xs font-bold uppercase tracking-wider flex items-center gap-2">
                            <span className="flex h-2 w-2 relative">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                            </span>
                            最需優先改善
                        </p>
                        <div className="flex items-center justify-end w-full">
                            <p className="text-2xl font-bold text-gray-800 truncate">
                                {dimensionName}
                            </p>
                        </div>
                        <div className="flex items-center gap-2 w-full justify-end">
                            <span className="text-red-600 font-bold text-lg">{worstDimension.score}/{worstDimension.max}</span>
                            <span className="text-gray-400 text-sm font-medium">({dimensionPercentage}%)</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                            <div className="bg-red-500 h-1.5 rounded-full" style={{ width: `${dimensionPercentage}%` }}></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
