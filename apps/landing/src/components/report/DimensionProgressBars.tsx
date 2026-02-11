interface DimensionItem {
    name: string;
    score: number;
    max: number;
    status: 'pass' | 'fail' | 'unknown';
    details?: string;
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
                    <div className="space-y-2">
                        {dim.items.map((item, idx) => (
                            <div key={idx} className="flex items-center justify-between text-sm">
                                <span className="flex items-center gap-2">
                                    <span className="text-lg">
                                        {item.status === 'pass' ? '✅' : item.status === 'fail' ? '❌' : '❓'}
                                    </span>
                                    <span className="text-gray-700">{getItemDisplayName(item.name)}</span>
                                </span>
                                <span className="text-gray-600">
                                    +{item.score}
                                    {item.details && <span className="ml-1 text-xs">({item.details})</span>}
                                </span>
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
        'organization': '組織資訊',
        'author': '作者資訊',
        'contact': '聯絡資訊',
        'has_jsonld': 'Schema.org 結構化資料',
        'schema_variety': 'Schema 多樣性',
        'schema_quality': 'Schema 質量',
        'social_links': '社群連結',
        'authority_links': '外部引用連結',
        'https': 'HTTPS 安全協定',
        'performance': '頁面載入速度',
        'basic_usability': '網站基本可用性'
    };

    return nameMap[name] || name;
}
