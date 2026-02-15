import React from 'react'
import { useParams } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import '../styles/pdf-report.css'

interface ReportData {
    url: string
    total_score: number
    grade: string
    conclusion: string
    dimensions: {
        [key: string]: {
            name: string
            score: number
            max: number
            percentage: number
        }
    }
    quick_wins: Array<{
        title: string
        impact: string
        effort: string
        description: string
    }>
    trust_gaps: string[]
    scan_id: string
    engine_version: string
    scan_date: string
}

export default function PDFReportTemplate() {
    const { scanId } = useParams<{ scanId: string }>()
    const [report, setReport] = useState<ReportData | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchReportData()
    }, [scanId])

    const fetchReportData = async () => {
        try {
            const { data: { session } } = await supabase.auth.getSession()
            if (!session) return

            const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

            // Fetch main report
            const reportRes = await fetch(`${apiUrl}/api/reports/${scanId}`, {
                headers: { 'Authorization': `Bearer ${session.access_token}` }
            })
            const reportData = await reportRes.json()

            // Fetch dimensions
            const dimsRes = await fetch(`${apiUrl}/api/reports/${scanId}/dimensions`, {
                headers: { 'Authorization': `Bearer ${session.access_token}` }
            })
            const dimsData = await dimsRes.json()

            // Extract trust gaps (top 5)
            const gaps: string[] = []
            if (!reportData.has_title) gaps.push('缺少網站標題')
            if (!reportData.has_description) gaps.push('缺少網站描述')
            if (!reportData.has_schema) gaps.push('缺少結構化資料')
            if (!reportData.has_author && !reportData.has_organization) gaps.push('缺少作者/組織資訊')
            if (!reportData.has_social_links) gaps.push('社群證明不足')

            setReport({
                url: reportData.url,
                total_score: dimsData.total_score,
                grade: dimsData.grade,
                conclusion: reportData.summary?.conclusion || '分析完成',
                dimensions: dimsData.dimensions,
                quick_wins: (dimsData.quick_wins || []).slice(0, 3), // Top 3 only
                trust_gaps: gaps.slice(0, 5),
                scan_id: scanId || '',
                engine_version: 'r2.0',
                scan_date: new Date().toLocaleDateString('zh-TW')
            })
            setLoading(false)
        } catch (error) {
            console.error('Failed to fetch report:', error)
            setLoading(false)
        }
    }

    if (loading) {
        return <div className="pdf-loading">載入中...</div>
    }

    if (!report) {
        return <div className="pdf-error">無法載入報告</div>
    }

    const getGradeColor = (grade: string) => {
        switch (grade) {
            case 'A': return '#22c55e'
            case 'B': return '#3b82f6'
            case 'C': return '#f59e0b'
            case 'D': return '#ef4444'
            case 'F': return '#dc2626'
            default: return '#6b7280'
        }
    }

    const getScoreColor = (percentage: number) => {
        if (percentage >= 80) return '#22c55e'
        if (percentage >= 60) return '#f59e0b'
        return '#ef4444'
    }

    return (
        <div className="pdf-report">
            {/* Page 1 */}
            <div className="pdf-page">
                {/* Header */}
                <header className="pdf-header">
                    <div className="pdf-logo">
                        <div className="logo-icon">🛡️</div>
                        <div className="logo-text">
                            <div className="logo-title">Trust WEDO</div>
                            <div className="logo-subtitle">AI 信任度健檢報告</div>
                        </div>
                    </div>
                    <div className="pdf-meta">
                        <div className="meta-url">{report.url}</div>
                        <div className="meta-date">{report.scan_date}</div>
                    </div>
                </header>

                {/* Hero Summary */}
                <section className="pdf-hero">
                    <div className="hero-score">
                        <div className="score-value">{report.total_score}</div>
                        <div className="score-max">/100</div>
                    </div>
                    <div className="hero-grade" style={{ backgroundColor: getGradeColor(report.grade) }}>
                        等級 {report.grade}
                    </div>
                    <div className="hero-conclusion">{report.conclusion}</div>
                </section>

                {/* Five Dimensions */}
                <section className="pdf-dimensions">
                    <h2 className="section-title">五大維度分析</h2>
                    <div className="dimensions-grid">
                        {Object.entries(report.dimensions).map(([key, dim]) => (
                            <div key={key} className="dimension-row">
                                <div className="dim-name">{dim.name}</div>
                                <div className="dim-bar-container">
                                    <div
                                        className="dim-bar-fill"
                                        style={{
                                            width: `${dim.percentage}%`,
                                            backgroundColor: getScoreColor(dim.percentage)
                                        }}
                                    />
                                </div>
                                <div className="dim-score">{dim.score}/{dim.max}</div>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Quick Wins */}
                <section className="pdf-quick-wins">
                    <h2 className="section-title">快速提升建議 (Top 3)</h2>
                    <div className="quick-wins-list">
                        {report.quick_wins.map((win, idx) => (
                            <div key={idx} className="quick-win-item">
                                <div className="win-number">{idx + 1}</div>
                                <div className="win-content">
                                    <div className="win-title">{win.title}</div>
                                    <div className="win-meta">
                                        <span className="win-impact">影響: {win.impact}</span>
                                        <span className="win-effort">難度: {win.effort}</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Trust Gaps */}
                <section className="pdf-trust-gaps">
                    <h2 className="section-title">信任缺口摘要</h2>
                    <ul className="gaps-list">
                        {report.trust_gaps.map((gap, idx) => (
                            <li key={idx} className="gap-item">{gap}</li>
                        ))}
                    </ul>
                </section>

                {/* Footer */}
                <footer className="pdf-footer">
                    <div className="footer-left">
                        引擎版本: {report.engine_version} | 掃描編號: {report.scan_id.slice(0, 8)}
                    </div>
                    <div className="footer-right">
                        第 1 頁 / 共 1 頁
                    </div>
                </footer>
            </div>
        </div>
    )
}
