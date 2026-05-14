import React, { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { supabase } from '../lib/supabase'
import { getApiBaseUrl } from '../lib/api'

export default function Dashboard() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const location = useLocation()

  const [url, setUrl] = useState(location.state?.prefillUrl || '')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [recentScans, setRecentScans] = useState<any[]>([])
  const [progressStage, setProgressStage] = useState('正在初始化...')

  useEffect(() => {
    fetchRecentScans()
  }, [])

  useEffect(() => {
    if (location.state?.prefillUrl) {
      setUrl(location.state.prefillUrl)
    }
  }, [location.state])

  const fetchRecentScans = async () => {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { data } = await supabase
      .from('scan_jobs')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(5)

    if (data) setRecentScans(data)
  }

  const pollJobStatus = async (jobId: string) => {
    let interval = 2000 // 初始 2 秒
    let attempts = 0
    const maxAttempts = 30 // 最多約 2-3 分鐘（隨退避增加）

    const { data: { session } } = await supabase.auth.getSession()
    if (!session) return

    const poll = async () => {
      attempts++

      try {
        const apiUrl = getApiBaseUrl()
        const response = await fetch(`${apiUrl}/api/scans/${jobId}`, {
          headers: {
            'Authorization': `Bearer ${session.access_token}`
          }
        })
        const job = await response.json()

        if (job.progress_stage) {
          setProgressStage(job.progress_stage)
        }

        if (job.status === 'completed') {
          navigate(`/dashboard/reports/${jobId}`)
        } else if (job.status === 'failed') {
          setError(job.error_message || '分析失敗')
          setLoading(false)
          fetchRecentScans()
        } else if (attempts < maxAttempts) {
          // 漸進式退避：2s → 3s → 4.5s → 6.7s...
          interval = Math.min(interval * 1.5, 10000)
          setTimeout(poll, interval)
        } else {
          setError('分析超時，請稍後在歷史記錄中查看結果')
          setLoading(false)
          fetchRecentScans()
        }
      } catch (err) {
        console.error('Polling error:', err)
        setTimeout(poll, 5000) // 出錯則固定 5 秒後再試
      }
    }

    poll()
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setProgressStage('排隊中...')

    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) throw new Error('Session expired')

      const apiUrl = getApiBaseUrl()
      const response = await fetch(`${apiUrl}/api/scans`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`
        },
        body: JSON.stringify({ url })
      })

      if (!response.ok) {
        throw new Error('建立健檢失敗')
      }

      const job = await response.json()
      pollJobStatus(job.id)

    } catch (err: any) {
      setError(err.message || '分析失敗，請稍後再試')
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto py-10">
      {/* Loading Modal */}
      {loading && (
        <div className="fixed inset-0 bg-brand-navy/60 backdrop-blur-sm flex items-center justify-center z-[100] p-6 text-brand-navy dark:text-brand-light">
          <div className="bg-white dark:bg-brand-navy p-10 rounded-[2.5rem] max-w-md w-full shadow-2xl border border-brand-navy/5 dark:border-brand-light/10 text-center">
            <div className="relative w-24 h-24 mx-auto mb-8">
              <div className="absolute inset-0 border-4 border-brand-blue/10 rounded-full" />
              <div className="absolute inset-0 border-4 border-brand-blue border-t-transparent rounded-full animate-spin" />
              <div className="absolute inset-0 flex items-center justify-center text-3xl">🔍</div>
            </div>
            <h3 className="text-2xl font-black mb-2 tracking-tight">
              正在分析中...
            </h3>
            <p className="text-brand-slate dark:text-brand-light/60 mb-8 font-medium">
              正在進行：<span className="text-brand-blue">{progressStage}</span><br />
              預計需要 30-60 秒。
            </p>
            <div className="space-y-4 text-left bg-brand-light/50 dark:bg-brand-navy/30 p-6 rounded-2xl border border-brand-navy/5">
              <div className={`flex items-center gap-3 font-bold ${progressStage.includes('讀取') ? 'text-brand-blue animate-pulse' : 'text-brand-success'}`}>
                <span>{progressStage.includes('讀取') ? '⏳' : '✅'}</span> <span>讀取網站中內容</span>
              </div>
              <div className={`flex items-center gap-3 font-bold ${progressStage.includes('分析') ? 'text-brand-blue animate-pulse' : progressStage.includes('報告') || progressStage.includes('完成') ? 'text-brand-success' : 'text-brand-slate/40'}`}>
                <span>{progressStage.includes('分析') ? '⏳' : progressStage.includes('報告') || progressStage.includes('完成') ? '✅' : '⚪'}</span> <span>分析 AI 識別特徵</span>
              </div>
              <div className={`flex items-center gap-3 font-bold ${progressStage.includes('報告') ? 'text-brand-blue animate-pulse' : progressStage.includes('完成') ? 'text-brand-success' : 'text-brand-slate/40'}`}>
                <span>{progressStage.includes('報告') ? '⏳' : progressStage.includes('完成') ? '✅' : '⚪'}</span> <span>產生成信度報告</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Form */}
      <div className="bg-white dark:bg-brand-navy/50 p-12 rounded-[2.5rem] border border-brand-navy/5 dark:border-brand-light/5 shadow-2xl relative overflow-hidden group">
        <div className="absolute -top-24 -right-24 w-64 h-64 bg-brand-blue/5 rounded-full blur-3xl group-hover:bg-brand-blue/10 transition-colors" />

        <div className="relative">
          <h1 className="text-4xl md:text-5xl font-black text-brand-navy dark:text-brand-light mb-4 text-center tracking-tight text-brand-navy dark:text-brand-light">
            開始一次網站可信度健檢
          </h1>

          <p className="text-center text-xl text-brand-slate dark:text-brand-light/60 mb-12 max-w-2xl mx-auto leading-relaxed">
            適合內容創作者、行銷人、品牌網站。<br />
            輸入網址，讓 AI 告訴你如何提升權威感。
          </p>

          <form onSubmit={handleSubmit} className="space-y-6 max-w-2xl mx-auto">
            <div className="relative">
              <label className="block text-sm font-bold text-brand-navy/40 dark:text-brand-light/40 mb-3 ml-2 uppercase tracking-widest">
                你要檢查的網站網址
              </label>
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://your-brand-website.com"
                required
                className="w-full px-8 py-5 rounded-2xl border-2 border-brand-navy/5 dark:border-brand-light/10 bg-brand-light/50 dark:bg-brand-navy focus:outline-none focus:ring-4 focus:ring-brand-blue/20 focus:border-brand-blue text-brand-navy dark:text-brand-light text-xl transition-all shadow-inner"
              />
            </div>

            {error && (
              <div className="p-4 bg-red-50 dark:bg-red-900/10 border border-red-100 dark:border-red-900/20 rounded-xl text-red-600 dark:text-red-400 text-sm font-bold text-center">
                ❌ {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-6 bg-brand-blue text-white rounded-2xl font-black text-2xl hover:bg-brand-blue/90 hover:scale-[1.02] active:scale-[0.98] transition-all shadow-xl shadow-brand-blue/25 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              立即開始分析
            </button>
          </form>
        </div>
      </div>

      {/* 歷史記錄 */}
      <div className="mt-20">
        <div className="flex items-center justify-between mb-8 px-4">
          <h2 className="text-2xl font-black text-brand-navy dark:text-brand-light tracking-tight">
            歷史檢查記錄
          </h2>
        </div>

        {recentScans.length === 0 ? (
          <div className="bg-white/50 dark:bg-brand-navy/30 border-2 border-dashed border-brand-navy/5 dark:border-brand-light/5 rounded-[2rem] py-16 text-center text-brand-navy dark:text-brand-light">
            <p className="text-brand-slate dark:text-brand-light/40 text-lg font-medium">
              尚未有檢查記錄。
            </p>
          </div>
        ) : (
          <div className="grid gap-4">
            {recentScans.map((scan) => (
              <div
                key={scan.id}
                onClick={() => scan.status === 'completed' && navigate(`/dashboard/reports/${scan.id}`)}
                className={`bg-white dark:bg-brand-navy/40 p-6 rounded-2xl border border-brand-navy/5 dark:border-brand-light/5 flex items-center justify-between group transition-all ${scan.status === 'completed' ? 'hover:border-brand-blue/20 cursor-pointer' : ''}`}
              >
                <div>
                  <div className="text-lg font-bold text-brand-navy dark:text-brand-light mb-1 group-hover:text-brand-blue transition-colors">
                    {scan.url}
                  </div>
                  <div className="text-sm text-brand-slate dark:text-brand-light/40 font-medium">
                    {new Date(scan.created_at).toLocaleString('zh-TW', { hour12: false, year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  {/* 分數顯示 (如果有的話) */}
                  {scan.status === 'completed' && scan.result?.total_score && (
                    <div className="hidden md:flex flex-col items-end mr-2">
                      <div className="text-lg font-black text-brand-navy dark:text-brand-light leading-none">
                        {scan.result.total_score}
                        <span className="text-xs text-brand-slate dark:text-brand-light/60 ml-0.5 font-medium">/100</span>
                      </div>
                      <div className={`text-[10px] font-bold px-1.5 py-0.5 rounded mt-1 ${scan.result.grade === 'A' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                          scan.result.grade === 'B' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' :
                            scan.result.grade === 'C' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                              'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                        }`}>
                        等級 {scan.result.grade}
                      </div>
                    </div>
                  )}

                  <span className={`px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-tighter ${scan.status === 'completed' ? 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400' :
                    scan.status === 'failed' ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400' :
                      'bg-amber-100 text-amber-700 dark:bg-amber-900/20 dark:text-amber-400'
                    }`}>
                    {scan.status}
                  </span>
                  <div className="w-10 h-10 rounded-xl bg-brand-navy/5 dark:bg-brand-light/5 flex items-center justify-center group-hover:bg-brand-blue/10 transition-colors">
                    <svg className="w-5 h-5 text-brand-slate group-hover:text-brand-blue transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
