import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

interface DimensionData {
    name: string;
    percentage: number;
}

interface ReportRadarChartProps {
    dimensions: Record<string, {
        name: string;
        score: number;
        max: number;
        percentage: number;
    }>;
}

export function ReportRadarChart({ dimensions }: ReportRadarChartProps) {
    // 轉換資料格式供 Recharts 使用
    const data = Object.entries(dimensions).map(([key, dim]) => ({
        dimension: dim.name,
        score: dim.percentage,
        fullMark: 100
    }));

    return (
        <div className="w-full h-80">
            <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={data}>
                    <PolarGrid stroke="#e5e7eb" />
                    <PolarAngleAxis
                        dataKey="dimension"
                        tick={{ fill: '#6b7280', fontSize: 12 }}
                    />
                    <PolarRadiusAxis
                        angle={90}
                        domain={[0, 100]}
                        tick={{ fill: '#9ca3af', fontSize: 10 }}
                    />
                    <Radar
                        name="分數"
                        dataKey="score"
                        stroke="#3b82f6"
                        fill="#3b82f6"
                        fillOpacity={0.6}
                    />
                </RadarChart>
            </ResponsiveContainer>

            {/* 圖例說明 */}
            <div className="mt-4 text-center text-sm text-gray-600">
                <p>五大維度總覽 - 百分比愈高代表該維度表現愈好</p>
            </div>
        </div>
    );
}
