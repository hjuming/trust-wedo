import React, { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabase'
import { ReportRadarChart } from '../components/report/ReportRadarChart'
import { DimensionProgressBars } from '../components/report/DimensionProgressBars'
import { QuickWins } from '../components/report/QuickWins'
import { ReportSummaryCard } from '../components/report/ReportSummaryCard'
import { getApiBaseUrl } from '../lib/api'

export default function Report() {
  const { jobId } = useParams()
  const navigate = useNavigate()
  const [report, setReport] = useState<any>(null)
  const [dimensions, setDimensions] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [isExporting, setIsExporting] = useState(false)

  useEffect(() => {
    let timeoutId: any;

    const pollReport = async () => {
      try {
        const { data: { session } } = await supabase.auth.getSession()
        if (!session) throw new Error('Unauthorized')

        const apiUrl = getApiBaseUrl()
        const response = await fetch(`${apiUrl}/api/reports/${jobId}`, {
          headers: {
            'Authorization': `Bearer ${session.access_token}`
          }
        })

        if (!response.ok) throw new Error('無法讀取報告')

        const data = await response.json()
        setReport(data)

        // 如果還在處理中，繼續輪詢
        if (data.status === 'processing' || data.status === 'pending') {
          timeoutId = setTimeout(pollReport, 2000)
        } else {
          // 完成或失敗，停止輪詢並讀取維度
          setLoading(false)
          fetchDimensions()
        }
      } catch (err: any) {
        setError(err.message)
        setLoading(false)
      }
    }

    pollReport()

    return () => {
      if (timeoutId) clearTimeout(timeoutId)
    }
  }, [jobId])

  // Removed fetchReport and fetchDimensions from here (integrated above)



  // Removed fetchReport as logic is moved to useEffect

  const fetchDimensions = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) return

      const apiUrl = getApiBaseUrl()
      const response = await fetch(`${apiUrl}/api/reports/${jobId}/dimensions`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setDimensions(data)
      }
    } catch (err) {
      console.error('無法讀取維度資料:', err)
    }
  }

  const handleReAudit = () => {
    navigate('/dashboard', { state: { prefillUrl: report.url } })
  }

  const handleExportPDF = async () => {
    // ... (Keep existing implementation)
    try {
      // ... existing PDF logic ...
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) return

      const apiUrl = getApiBaseUrl()
      const response = await fetch(`${apiUrl}/api/reports/${jobId}/pdf`, {
        headers: { 'Authorization': `Bearer ${session.access_token}` }
      })

      if (!response.ok) throw new Error('無法下載 PDF')

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      // ... same logic ...

      const contentDisposition = response.headers.get('Content-Disposition')
      let filename = `trust-wedo-report-${jobId}.pdf`

      if (contentDisposition) {
        const matches = /filename="([^"]*)"/.exec(contentDisposition)
        if (matches && matches[1]) filename = matches[1]
      } else if (report?.url) {
        try {
          const urlObj = new URL(report.url)
          filename = `Trust-WEDO-${urlObj.hostname.replace('www.', '')}-${new Date().toISOString().split('T')[0]}.pdf`
        } catch { }
      }

      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      console.error(err)
      window.print()
    }
  }

  const getWorstDimension = (dims: any) => {
    if (!dims) return { name: '未知', score: 0, max: 100 };
    let worstKey = '';
    let minPercentage = 200;

    Object.keys(dims).forEach(key => {
      const d = dims[key];
      if (!d.max) return;
      const percentage = d.score / d.max;
      if (percentage < minPercentage) {
        minPercentage = percentage;
        worstKey = key;
      }
    });

    if (!worstKey) return { name: '無', score: 0, max: 100 };
    return { name: worstKey, score: dims[worstKey].score, max: dims[worstKey].max };
  }

  const isProcessing = loading || (report && (report.status === 'processing' || report.status === 'pending'));

  if (isProcessing) {
    const stage = report?.progress_stage || "準備中...";
    const percentMatch = stage.match(/\[(\d+)%\]/);
    const percent = percentMatch ? parseInt(percentMatch[1]) : 0;
    const message = stage.replace(/\[\d+%\]\s*/, '');

    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] max-w-md mx-auto px-6">
        <div className="relative w-24 h-24 mb-6">
          <div className="absolute inset-0 border-[6px] border-brand-light dark:border-brand-light/10 rounded-full"></div>
          <div className="absolute inset-0 border-[6px] border-brand-blue border-t-transparent rounded-full animate-spin"></div>
          <div className="absolute inset-0 flex items-center justify-center font-black text-xl text-brand-blue">
            {percent}%
          </div>
        </div>
        <h2 className="text-xl font-bold text-brand-navy dark:text-brand-light mb-2 text-center animate-pulse">
          {message || "正在分析..."}
        </h2>
        <p className="text-sm text-brand-slate dark:text-brand-light/60 text-center mb-8">
          AI 正在深入分析您的網站結構與信任訊號，這通常需要 1-2 分鐘...
        </p>

        <div className="w-full h-3 bg-brand-light dark:bg-brand-light/10 rounded-full overflow-hidden shadow-inner">
          <div
            className="h-full bg-gradient-to-r from-brand-blue to-cyan-400 transition-all duration-500 ease-out shadow-[0_0_10px_rgba(59,130,246,0.5)]"
            style={{ width: `${percent}%` }}
          />
        </div>
      </div>
    )
  }

  if (error || !report) {
    return (
      <div className="max-w-4xl mx-auto py-20 text-center">
        <div className="text-6xl mb-6">❌</div>
        <h1 className="text-3xl font-bold text-brand-navy dark:text-brand-light mb-4">讀取報告出錯</h1>
        <p className="text-brand-slate dark:text-brand-light/60 mb-8 font-medium">{error}</p>
        <Link to="/dashboard" className="px-8 py-3 bg-brand-blue text-white rounded-xl font-bold shadow-lg shadow-brand-blue/20 hover:scale-105 transition-transform">返回儀表板</Link>
      </div>
    )
  }

  const { issues, suggestions, signals, site_type, site_type_confidence } = report
  const worstDimension = dimensions ? getWorstDimension(dimensions.dimensions) : { name: '', score: 0, max: 0 };

  const siteTypeNames: any = {
    'ecommerce': '電商網站',
    'blog': '部落格 / 內容網站',
    'corporate': '企業官方網站',
    'personal': '個人品牌網站',
    'unknown': '一般網站'
  }

  return (
    <div className="max-w-4xl mx-auto py-10 px-6">
      <header className="mb-10 flex items-center justify-between">

        <Link to="/dashboard" className="no-print inline-flex items-center gap-2 text-brand-blue font-bold hover:translate-x-[-4px] transition-transform">
          ← 返回健檢列表
        </Link>
        <div className="text-sm font-bold text-brand-slate dark:text-brand-light/40">
          健檢網址: <span className="text-brand-navy dark:text-brand-light">{report.url}</span>
        </div>
      </header>

      {/* 1. Summary Card (New) */}
      {dimensions && (
        <div className="print-avoid-break mb-8">
          <ReportSummaryCard
            score={dimensions.total_score}
            grade={dimensions.grade}
            worstDimension={worstDimension}
            isDifficultSite={report.is_difficult_site}
            difficultSiteInfo={report.difficult_site_info}
            estimatedScore={report.estimated_score}
            estimatedGrade={report.estimated_grade}
            estimatedDimensions={report.estimated_dimensions}
            detectionMessage={report.detection_message}
          />

          {/* Scoring Guide */}
          <div className="bg-brand-blue/5 border border-brand-blue/10 rounded-3xl p-6 my-6 print-avoid-break no-print">
            <h3 className="text-lg font-bold text-brand-navy dark:text-brand-light mb-4 flex items-center gap-2">
              📏 評分標準說明
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-center">
              <div>
                <div className="font-black text-brand-success text-xl">A級 (80+)</div>
                <div className="text-xs font-bold text-brand-slate/60 dark:text-brand-light/40">優秀</div>
              </div>
              <div>
                <div className="font-black text-brand-blue text-xl">B級 (60-79)</div>
                <div className="text-xs font-bold text-brand-slate/60 dark:text-brand-light/40">良好</div>
              </div>
              <div>
                <div className="font-black text-yellow-500 text-xl">C級 (40-59)</div>
                <div className="text-xs font-bold text-brand-slate/60 dark:text-brand-light/40">及格</div>
              </div>
              <div>
                <div className="font-black text-orange-500 text-xl">D級 (20-39)</div>
                <div className="text-xs font-bold text-brand-slate/60 dark:text-brand-light/40">需改善</div>
              </div>
              <div>
                <div className="font-black text-red-500 text-xl">F級 (&lt;20)</div>
                <div className="text-xs font-bold text-brand-slate/60 dark:text-brand-light/40">不及格</div>
              </div>
            </div>
            <div className="mt-4 pt-4 border-t border-brand-navy/5 dark:border-brand-light/5 text-xs text-brand-slate dark:text-brand-light/60 font-medium">
              💡 參考標竿: <span className="font-bold">Apple.com</span> 約 65 分 (B級), <span className="font-bold">Google.com</span> 約 30 分 (D級)
            </div>
          </div>

          <div className="no-print flex flex-col sm:flex-row gap-4 mt-6">
            <button
              onClick={handleReAudit}
              className="flex-1 py-4 bg-brand-blue text-white rounded-2xl font-black text-lg hover:bg-brand-blue/90 hover:scale-[1.02] active:scale-[0.98] transition-all shadow-lg shadow-brand-blue/25"
            >
              ✅ 我已修正，重新健檢
            </button>
            <button
              onClick={handleExportPDF}
              disabled={isExporting}
              className={`flex-1 py-4 bg-white dark:bg-brand-navy border-2 border-brand-blue text-brand-blue rounded-2xl font-black text-lg hover:bg-brand-blue/5 transition-all ${isExporting ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {isExporting ? '⏳ 生成 PDF 中...' : '📄 匯出 PDF 報告'}
            </button>
          </div>
        </div>
      )}

      {/* 2. Site Identity & Signals */}
      <div className="print-avoid-break grid md:grid-cols-3 gap-6 mb-8">
        <div className="md:col-span-1 bg-white dark:bg-brand-navy/50 p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-lg flex flex-col items-center text-center">
          <div className="text-4xl mb-4">🪪</div>
          <h3 className="text-sm font-bold text-brand-slate dark:text-brand-light/40 uppercase tracking-widest mb-2">網站類型識別</h3>
          <div className="text-xl font-black text-brand-navy dark:text-brand-light mb-1">
            {siteTypeNames[site_type] || '未知類型'}
          </div>
          <div className="text-xs font-bold text-brand-blue">
            AI 信心度 {Math.round(site_type_confidence * 100)}%
          </div>
        </div>

        <div className="md:col-span-2 bg-white dark:bg-brand-navy/50 p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-lg">
          <h3 className="text-sm font-bold text-brand-slate dark:text-brand-light/40 uppercase tracking-widest mb-6">偵測到的信任信號</h3>
          <div className="grid grid-cols-2 gap-6">
            <div>
              <div className="text-xs font-bold text-brand-slate dark:text-brand-light/40 mb-2">Schema.org 結構化資料</div>
              <div className="flex flex-wrap gap-2">
                {signals.schema_types && signals.schema_types.length > 0 ? (
                  signals.schema_types.map((type: string) => (
                    <span key={type} className="px-2 py-1 bg-brand-blue/10 text-brand-blue text-[10px] font-black rounded-md border border-brand-blue/20">
                      {type}
                    </span>
                  ))
                ) : (
                  <span className="text-sm text-brand-slate/40 italic">未偵測到有效標記</span>
                )}
              </div>
            </div>
            <div>
              <div className="text-xs font-bold text-brand-slate dark:text-brand-light/40 mb-2">身分與連結</div>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-brand-slate dark:text-brand-light/60">作者資訊</span>
                  <span className={signals.has_author ? 'text-brand-success font-bold' : 'text-brand-slate/40'}>
                    {signals.has_author ? `已偵測 (${signals.author_count})` : '未發現'}
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-brand-slate dark:text-brand-light/60">外部引用連結</span>
                  <span className="text-brand-navy dark:text-brand-light font-bold">
                    {signals.outbound_links_count} 條
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-brand-slate dark:text-brand-light/60">社群證明</span>
                  <span className={signals.has_social_proof ? 'text-brand-success font-bold' : 'text-brand-slate/40'}>
                    {signals.has_social_proof ? '已連結' : '不足'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Visualizations */}
      {dimensions && (
        <>
          <div className="print-avoid-break bg-white dark:bg-brand-navy/50 p-10 rounded-[2.5rem] mb-8 border-2 border-brand-blue/20 shadow-xl">
            <h2 className="text-2xl font-black mb-6 text-brand-navy dark:text-brand-light flex items-center gap-3">
              <span className="text-3xl">📊</span>
              五大維度總覽
            </h2>
            <ReportRadarChart dimensions={dimensions.dimensions} />
          </div>

          {dimensions.quick_wins && dimensions.quick_wins.length > 0 && (
            <div className="print-avoid-break mb-8">
              <QuickWins quickWins={dimensions.quick_wins} />
            </div>
          )}

          <div className="print-avoid-break mb-8">
            <h2 className="text-2xl font-black mb-6 text-brand-navy dark:text-brand-light flex items-center gap-3">
              <span className="text-3xl">📈</span>
              各維度詳細分析
            </h2>
            <DimensionProgressBars dimensions={dimensions.dimensions} />
          </div>
        </>
      )}

      {/* 4. Analysis Details */}
      <div className="grid md:grid-cols-2 gap-8 mb-8 text-brand-navy dark:text-brand-light">
        <div className="print-avoid-break bg-white dark:bg-brand-navy/50 p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-lg">
          <h2 className="text-xl font-black mb-6 flex items-center gap-2 tracking-tight">
            <span className="w-2 h-8 bg-red-500 rounded-full" />
            目前的信任缺口
          </h2>
          {issues.length === 0 ? (
            <p className="text-brand-success font-bold py-4">✨ 恭喜！目前未偵測到重大結構問題。</p>
          ) : (
            <ul className="space-y-6">
              {issues.map((issue: any, i: number) => (
                <li key={i} className="flex items-start gap-4">
                  <span className="text-3xl">
                    {issue.severity === 'high' ? '🔴' : '🟡'}
                  </span>
                  <div>
                    <div className="font-bold mb-1 leading-tight text-lg">
                      {issue.title}
                    </div>
                    <div className="text-sm text-brand-slate dark:text-brand-light/60 font-medium">
                      {issue.description}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="print-avoid-break bg-white dark:bg-brand-navy/50 p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-lg">
          <h2 className="text-xl font-black mb-6 flex items-center gap-2 tracking-tight">
            <span className="w-2 h-8 bg-brand-success rounded-full" />
            建議採取的行動
          </h2>
          {suggestions.length === 0 ? (
            <p className="text-brand-slate dark:text-brand-light/60 py-4">暫無特定建議。</p>
          ) : (
            <ul className="space-y-6">
              {suggestions.map((suggestion: any, i: number) => (
                <li key={i} className="flex items-start gap-4">
                  <span className="text-2xl text-brand-success font-black">0{i + 1}</span>
                  <div>
                    <div className="font-bold mb-1 leading-tight">
                      {suggestion.action}
                    </div>
                    <div className="text-xs font-black text-brand-blue uppercase tracking-tighter mb-2">
                      效果：{suggestion.impact_desc || suggestion.impact}
                    </div>
                    <div className="space-y-2 mt-3">
                      {suggestion.how_to && suggestion.how_to.map((step: string, idx: number) => (
                        <div key={idx} className="text-xs text-brand-slate dark:text-brand-light/60 bg-brand-light/50 dark:bg-brand-navy p-2 rounded-lg border border-brand-navy/5">
                          {step}
                        </div>
                      ))}
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* 5. Footer */}
      <div className="mt-12 text-center text-brand-slate dark:text-brand-light/40 text-sm font-medium">
        這份報告是由 Trust WEDO AI 引擎基於您的網站結構自動生成。<br />
        引擎版本: {report.report_version} • 掃描編號: {report.job_id}
      </div>
    </div>
  )
}
