import { useState } from 'react';

interface QuickWin {
    title: string;
    impact: string;
    effort: string;
    dimension: string;
    instructions: string;
    code_snippet?: string;
    priority: number;
}

interface QuickWinsProps {
    quickWins: QuickWin[];
}

export function QuickWins({ quickWins }: QuickWinsProps) {
    const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

    const handleCopy = async (code: string, index: number) => {
        try {
            await navigator.clipboard.writeText(code);
            setCopiedIndex(index);
            setTimeout(() => setCopiedIndex(null), 2000);
        } catch (err) {
            console.error('複製失敗:', err);
        }
    };

    if (!quickWins || quickWins.length === 0) {
        return null;
    }

    return (
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-500 rounded-lg p-6">
            {/* 標題 */}
            <div className="flex items-start gap-3 mb-4">
                <span className="text-2xl">💡</span>
                <div>
                    <h3 className="text-lg font-bold text-green-800">
                        🚀 快速提升分數 - 3 分鐘見效
                    </h3>
                    <p className="text-sm text-green-700 mt-1">
                        以下是最容易改善的項目,立即實施即可看到分數提升
                    </p>
                </div>
            </div>

            {/* 建議列表 */}
            <div className="space-y-4">
                {quickWins.map((win, idx) => (
                    <div key={idx} className="bg-white rounded-lg p-4 shadow-sm border border-green-200">
                        <div className="flex items-start justify-between mb-2">
                            <div className="flex-1">
                                <h4 className="font-semibold text-gray-900 flex items-center gap-2">
                                    <span className="text-green-600">✅</span>
                                    {win.title}
                                </h4>
                                <div className="flex gap-4 mt-1 text-xs text-gray-600">
                                    <span className="flex items-center gap-1">
                                        ⚡ {win.effort}
                                    </span>
                                    <span className="flex items-center gap-1">
                                        📈 {win.impact}
                                    </span>
                                    <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded">
                                        {getDimensionName(win.dimension)}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <p className="text-sm text-gray-700 mt-2">{win.instructions}</p>

                        {/* 程式碼範例 */}
                        {win.code_snippet && (
                            <div className="mt-3">
                                <div className="relative bg-gray-900 rounded-md p-3">
                                    <pre className="text-xs text-green-400 overflow-x-auto">
                                        <code>{win.code_snippet}</code>
                                    </pre>
                                    <button
                                        onClick={() => handleCopy(win.code_snippet!, idx)}
                                        className="absolute top-2 right-2 px-2 py-1 bg-gray-700 hover:bg-gray-600 text-white text-xs rounded transition-colors"
                                    >
                                        {copiedIndex === idx ? '✓ 已複製' : '📋 複製'}
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

function getDimensionName(dimension: string): string {
    const nameMap: Record<string, string> = {
        'discoverability': 'AI可發現性',
        'identity': '身份識別',
        'structure': '內容結構化',
        'trust': '信任訊號',
        'technical': '技術體質'
    };

    return nameMap[dimension] || dimension;
}
