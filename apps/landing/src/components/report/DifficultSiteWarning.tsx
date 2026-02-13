import React, { useState } from 'react';

interface DifficultSiteWarningProps {
    siteInfo: {
        name: string;
        name_zh: string;
        reason: string;
        estimated_score: number;
        estimated_grade: string;
        note: string;
    };
    estimatedDimensions?: {
        discoverability: number;
        structure: number;
        technical: number;
        social: number;
    };
    detectionMessage?: string;
}

export const DifficultSiteWarning: React.FC<DifficultSiteWarningProps> = ({
    siteInfo,
    estimatedDimensions,
    detectionMessage
}) => {
    const [showDimensions, setShowDimensions] = useState(false);

    // 維度名稱映射
    const dimensionNames: Record<string, string> = {
        discoverability: 'AI 可發現性',
        structure: '內容結構化',
        technical: '技術基礎',
        social: '社群信任',
    };

    // 維度最大值
    const dimensionMax: Record<string, number> = {
        discoverability: 25,
        structure: 25,
        technical: 20,
        social: 30,
    };

    return (
        <div className="mb-6 rounded-lg border-l-4 border-amber-500 bg-amber-50 dark:bg-amber-900/20">
            <div className="p-4">
                {/* Header */}
                <div className="flex items-start gap-3 mb-3">
                    <svg
                        className="w-6 h-6 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                        />
                    </svg>
                    <div className="flex-1">
                        <h4 className="font-bold text-amber-900 dark:text-amber-200 text-base mb-1">
                            ⚠️ 評分可能不準確
                        </h4>
                        <p className="text-sm text-amber-800 dark:text-amber-300 leading-relaxed break-words">
                            {detectionMessage || siteInfo.reason}
                        </p>
                    </div>
                </div>

                {/* Divider */}
                <div className="my-3 border-t border-amber-200 dark:border-amber-800" />

                {/* Estimated Score */}
                <div className="flex items-center gap-2 mb-3 p-3 bg-white/50 dark:bg-black/20 rounded-md">
                    <svg
                        className="w-5 h-5 text-amber-600 dark:text-amber-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                        />
                    </svg>
                    <div className="flex-1">
                        <div className="text-xs text-amber-700 dark:text-amber-400 mb-1">
                            預估分數 (基於網站類型)
                        </div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-bold text-amber-900 dark:text-amber-100">
                                {siteInfo.estimated_score}
                            </span>
                            <span className="text-lg text-amber-700 dark:text-amber-300">
                                / 100
                            </span>
                            <span className={`
                ml-2 px-2 py-0.5 rounded text-sm font-medium
                ${siteInfo.estimated_grade === 'A'
                                    ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300'
                                    : siteInfo.estimated_grade === 'B'
                                        ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300'
                                        : 'bg-gray-100 text-gray-800 dark:bg-gray-900/50 dark:text-gray-300'
                                }
              `}>
                                等級 {siteInfo.estimated_grade}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Estimated Dimensions (Collapsible) */}
                {estimatedDimensions && (
                    <div className="mb-3">
                        <button
                            onClick={() => setShowDimensions(!showDimensions)}
                            className="w-full flex items-center justify-between p-2 hover:bg-amber-100/50 dark:hover:bg-amber-900/10 rounded-md transition-colors"
                        >
                            <span className="text-xs font-medium text-amber-700 dark:text-amber-400">
                                預估維度分數
                            </span>
                            <svg
                                className={`w-4 h-4 text-amber-600 dark:text-amber-400 transition-transform ${showDimensions ? 'rotate-180' : ''
                                    }`}
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                            </svg>
                        </button>

                        {showDimensions && (
                            <div className="mt-2 p-3 bg-white/50 dark:bg-black/20 rounded-md space-y-2">
                                {Object.entries(estimatedDimensions).map(([key, value]) => (
                                    <div key={key} className="flex items-center justify-between text-sm">
                                        <span className="text-amber-800 dark:text-amber-300">
                                            {dimensionNames[key]}
                                        </span>
                                        <div className="flex items-center gap-2">
                                            <span className="font-medium text-amber-900 dark:text-amber-100">
                                                {value}/{dimensionMax[key]}
                                            </span>
                                            <div className="w-16 h-2 bg-amber-200 dark:bg-amber-800 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-amber-600 dark:bg-amber-400 rounded-full"
                                                    style={{ width: `${(value / dimensionMax[key]) * 100}%` }}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                )}

                {/* Note */}
                <div className="flex items-start gap-2 p-3 bg-amber-100/50 dark:bg-amber-900/10 rounded-md">
                    <svg
                        className="w-4 h-4 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                    </svg>
                    <p className="text-xs text-amber-800 dark:text-amber-300 leading-relaxed break-words">
                        💡 {siteInfo.note}
                    </p>
                </div>
            </div>
        </div>
    );
};
