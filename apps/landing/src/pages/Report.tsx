import React, { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabase'

export default function Report() {
  const { jobId } = useParams()
  const navigate = useNavigate()
  const [report, setReport] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchReport()
  }, [jobId])

  const fetchReport = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) throw new Error('Unauthorized')

      const response = await fetch(`http://localhost:8000/api/reports/${jobId}`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`
        }
      })
      
      if (!response.ok) throw new Error('無法讀取報告')
      
      const data = await response.json()
      setReport(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleReAudit = () => {
    navigate('/dashboard', { state: { prefillUrl: report.url } })
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="w-16 h-16 border-4 border-brand-blue/30 border-t-brand-blue rounded-full animate-spin mb-6" />
        <h2 className="text-2xl font-bold text-brand-navy dark:text-brand-light animate-pulse tracking-tight">正在產生成信度報告...</h2>
      </div>
    )
  }

  if (error || !report) {
    return (
      <div className="max-w-4xl mx-auto py-20 text-center">
        <div className="text-6xl mb-6">❌</div>
        <h1 className="text-3xl font-bold text-brand-navy dark:text-brand-light mb-4">讀取報告出錯</h1>
        <p className="text-brand-slate dark:text-brand-light/60 mb-8 font-medium">{error}</p>
        <Link to="/dashboard" className="px-8 py-3 bg-brand-blue text-white rounded-xl font-bold">返回儀表板</Link>
      </div>
    )
  }

  const { summary, issues, suggestions } = report

  return (
    <div className="max-w-4xl mx-auto py-10 px-6">
      <header className="mb-10 flex items-center justify-between">
        <Link to="/dashboard" className="inline-flex items-center gap-2 text-brand-blue font-bold hover:translate-x-[-4px] transition-transform">
          ← 返回健檢列表
        </Link>
        <div className="text-sm font-bold text-brand-slate dark:text-brand-light/40">
           健檢網址: <span className="text-brand-navy dark:text-brand-light">{report.url}</span>
        </div>
      </header>

      {/* 1. Summary Card */}
      <div className="bg-white dark:bg-brand-navy/50 p-10 rounded-[2.5rem] mb-8 border-2 border-brand-blue/20 shadow-xl relative overflow-hidden">
        <div className="flex flex-col md:flex-row items-center gap-8 relative z-10 text-brand-navy dark:text-brand-light">
          <div className="text-8xl">
            {summary.grade === 'A' && '🎉'}
            {summary.grade === 'B' && '✅'}
            {summary.grade === 'C' && '⚠️'}
            {summary.grade === 'D' && '❌'}
            {summary.grade === 'F' && '🚫'}
            {summary.grade === 'P' && '⏳'}
          </div>
          <div className="text-center md:text-left flex-1">
            <div className="inline-block px-4 py-1 rounded-full bg-brand-blue/10 text-brand-blue text-sm font-black uppercase tracking-widest mb-4">
               可信度等級: {summary.grade}
            </div>
            <h1 className="text-3xl md:text-4xl font-black leading-tight">
              {summary.conclusion}
            </h1>
            
            {/* CTA Close Loop */}
            <div className="flex flex-col sm:flex-row gap-4 mt-8">
              <button
                onClick={handleReAudit}
                className="flex-1 py-4 bg-brand-blue text-white rounded-2xl font-black text-lg hover:bg-brand-blue/90 hover:scale-[1.02] active:scale-[0.98] transition-all shadow-lg shadow-brand-blue/25"
              >
                ✅ 我已修正，重新健檢
              </button>
              <button
                className="flex-1 py-4 bg-white dark:bg-brand-navy border-2 border-brand-blue text-brand-blue rounded-2xl font-black text-lg hover:bg-brand-blue/5 transition-all"
              >
                📄 匯出 PDF 報告
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div className="grid md:grid-cols-2 gap-8 mb-8 text-brand-navy dark:text-brand-light">
        {/* 2. Key Issues */}
        <div className="bg-white dark:bg-brand-navy/50 p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-lg">
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
        
        {/* 3. Action Suggestions */}
        <div className="bg-white dark:bg-brand-navy/50 p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-lg">
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
                  <span className="text-2xl text-brand-success font-black">0{i+1}</span>
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
      
      {/* 4. Advanced Technical Details */}
      <details className="group bg-brand-navy/5 dark:bg-brand-navy/30 rounded-[2rem] overflow-hidden transition-all border border-transparent hover:border-brand-blue/10">
        <summary className="p-8 font-black text-brand-navy dark:text-brand-light cursor-pointer list-none flex items-center justify-between">
          <span className="flex items-center gap-3">
             <span className="text-xl">🧬</span> 進階技術分析資料 (Report Version: {report.report_version})
          </span>
          <span className="text-brand-blue group-open:rotate-180 transition-transform font-black">↓</span>
        </summary>
        <div className="px-8 pb-8">
           <div className="bg-black/90 rounded-2xl p-6 font-mono text-xs text-green-400 overflow-x-auto shadow-inner">
             <pre>{JSON.stringify(report, null, 2)}</pre>
           </div>
        </div>
      </details>

      <div className="mt-12 text-center text-brand-slate dark:text-brand-light/40 text-sm font-medium">
         這份報告是由 Trust WEDO AI 引擎基於您的網站結構自動生成。<br />
         引擎版本: {report.report_version} • 掃描編號: {report.job_id}
      </div>
    </div>
  )
}
