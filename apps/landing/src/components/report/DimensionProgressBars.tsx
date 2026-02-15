interface DimensionItem {
    name: string;
    score: number;
    max: number;
    status: 'pass' | 'fail' | 'unknown' | 'partial';
    details?: string;
    suggestion?: string;
}

interface DimensionData {
    name: string;
    score: number;
    max: number;
    percentage: number;
    items: DimensionItem[];
}

interface DimensionProgressBarsProps {
    dimensions: Record<string, DimensionData>;
}

export function DimensionProgressBars({ dimensions }: DimensionProgressBarsProps) {
    const validDims = Object.entries(dimensions).filter(([_, dim]) => dim.max > 0);

    return (
        <div className="space-y-6">
            {validDims.map(([key, dim]) => (
                <div key={key} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    {/* 標題與分數 */}
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-900">{dim.name}</h3>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getBadgeColor(dim.percentage)}`}>
                            {dim.score}/{dim.max} ({dim.percentage}%)
                        </span>
                    </div>

                    {/* 進度條 */}
                    <div className="mb-4">
                        <div className="w-full bg-gray-200 rounded-full h-3">
                            <div
                                className={`h-3 rounded-full transition-all duration-500 ${getProgressColor(dim.percentage)}`}
                                style={{ width: `${dim.percentage}%` }}
                            />
                        </div>
                    </div>

                    {/* 明細項目 */}
                    <div className="space-y-3">
                        {dim.items.map((item, idx) => (
                            <div key={idx} className="flex items-start justify-between text-sm py-1 border-b border-gray-50 last:border-0 hover:bg-gray-50/50 rounded-lg px-2 -mx-2 transition-colors">
                                <div className="flex items-start gap-3 flex-1">
                                    <span className="text-lg leading-none mt-0.5" title={item.status}>
                                        {item.status === 'pass' ? '✅' : item.status === 'partial' ? '⚠️' : '❌'}
                                    </span>
                                    <div>
                                        <div className="text-gray-900 font-medium">{getItemDisplayName(item.name)}</div>
                                        {/* Show suggestion for fail/partial */}
                                        {(item.status === 'fail' || item.status === 'partial') && item.suggestion && (
                                            <div className="text-xs text-amber-600 mt-1 flex items-center gap-1">
                                                <span>💡</span>
                                                {item.suggestion}
                                            </div>
                                        )}
                                        {/* Show details for pass (or fail if available) */}
                                        {item.details && (
                                            <div className="text-xs text-gray-500 mt-0.5">
                                                {item.details}
                                            </div>
                                        )}
                                    </div>
                                </div>
                                <div className="text-right ml-4 shrink-0">
                                    <span className={`font-bold ${item.score > 0 ? 'text-green-600' : 'text-gray-400'}`}>
                                        {item.score > 0 ? `+${item.score}` : '0'}
                                    </span>
                                    <div className="text-[10px] text-gray-400 uppercase tracking-wider">
                                        Score
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}

function getBadgeColor(percentage: number): string {
    if (percentage >= 80) return 'bg-green-100 text-green-800';
    if (percentage >= 50) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
}

function getProgressColor(percentage: number): string {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 50) return 'bg-yellow-500';
    return 'bg-red-500';
}

function getItemDisplayName(name: string): string {
    const nameMap: Record<string, string> = {
        'title': '網站標題',
        'description': '網站描述',
        'favicon': '網站圖示',
        'https': 'HTTPS 加密連線',
        'performance': '頁面載入速度',
        'mobile_friendly': '行動裝置適配',
        'basic_usability': '基礎可用性',
        'identity_page': '關於/聯繫頁面',
        'social_presence': '社群連結',
        'schema_missing': 'Schema.org 結構化資料',
        'basic_schema': '基礎 Schema 設定',
        'schema_detail': 'Schema 深度分析',
        'organization': '組織資訊',
        'author': '作者資訊',
        'contact': '聯絡資訊',
        'has_jsonld': 'Schema.org 結構化資料',
    };

    return nameMap[name] || name;
}
