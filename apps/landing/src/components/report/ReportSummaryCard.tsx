import React from 'react';
import { DifficultSiteWarning } from './DifficultSiteWarning';

interface ReportSummaryCardProps {
    score: number;
    grade: string;
    worstDimension: { name: string; score: number; max: number };
    isDifficultSite?: boolean;
    difficultSiteInfo?: {
        name: string;
        name_zh: string;
        reason: string;
        estimated_score: number;
        estimated_grade: string;
        note: string;
    };
    estimatedScore?: number;
    estimatedGrade?: string;
    estimatedDimensions?: {
        discoverability: number;
        structure: number;
        technical: number;
        social: number;
    };
    detectionMessage?: string;
}

export function ReportSummaryCard({
    score,
    grade,
    worstDimension,
    isDifficultSite = false,
    difficultSiteInfo,
    estimatedScore,
    estimatedGrade,
    estimatedDimensions,
    detectionMessage
}: ReportSummaryCardProps) {
    // 決定要顯示的分數和等級
    const displayScore = isDifficultSite && estimatedScore ? estimatedScore : score;
    const displayGrade = isDifficultSite && estimatedGrade ? estimatedGrade : grade;

    const gradeColor =
        displayGrade === 'A' ? 'bg-green-500' :
            displayGrade === 'B' ? 'bg-blue-500' :
                displayGrade === 'C' ? 'bg-yellow-500' :
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
        <div className="space-y-6">
            {/* 特殊網站警告 */}
            {isDifficultSite && difficultSiteInfo && (
                <DifficultSiteWarning
                    siteInfo={difficultSiteInfo}
                    estimatedDimensions={estimatedDimensions}
                    detectionMessage={detectionMessage}
                />
            )}

            {/* 分數卡片 */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-100 rounded-xl shadow-sm overflow-hidden">
                <div className="p-6 md:p-8">
                    <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                        <div className="space-y-2 text-center md:text-left">
                            <div className="flex items-baseline justify-center md:justify-start space-x-4">
                                <h1 className="text-6xl font-bold text-gray-900 tracking-tight">
                                    {displayScore}
                                    <span className="text-2xl text-gray-400 font-medium">/100</span>
                                </h1>
                                <span className={`${gradeColor} text-white px-4 py-1.5 rounded-full text-lg font-bold shadow-sm`}>
                                    等級 {displayGrade}
                                </span>
                            </div>

                            {/* 如果是特殊網站,顯示實際檢測分數 */}
                            {isDifficultSite && score !== displayScore && (
                                <div className="flex items-center gap-2 text-sm mt-2">
                                    <svg className="w-4 h-4 text-red-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <span className="text-gray-600 dark:text-gray-400">
                                        實際檢測分數: {score}/100
                                    </span>
                                    <span className="px-2 py-0.5 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 text-xs rounded font-medium">
                                        檢測失敗
                                    </span>
                                </div>
                            )}

                            <p className="text-gray-500 font-medium text-lg">
                                {isDifficultSite ? 'AI 信任度預估評分' : 'AI 信任度總體評分'}
                            </p>
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
                                {worstDimension.score === 0 && isDifficultSite ? (
                                    <span className="text-gray-400 text-sm">無法檢測</span>
                                ) : (
                                    <>
                                        <span className="text-red-600 font-bold text-lg">
                                            {worstDimension.score}/{worstDimension.max}
                                        </span>
                                        <span className="text-gray-400 text-sm font-medium">
                                            ({dimensionPercentage}%)
                                        </span>
                                    </>
                                )}
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                                <div
                                    className={`h-1.5 rounded-full ${isDifficultSite ? 'bg-amber-500' : 'bg-red-500'}`}
                                    style={{ width: `${dimensionPercentage}%` }}
                                ></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
