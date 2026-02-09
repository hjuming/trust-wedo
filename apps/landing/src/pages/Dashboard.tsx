import React, { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { supabase } from '../lib/supabase'

export default function Dashboard() {
  const { t } = useTranslation()
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [recentScans, setRecentScans] = useState<any[]>([])

  useEffect(() => {
    fetchRecentScans()
  }, [])

  const fetchRecentScans = async () => {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) return

    const { data, error } = await supabase
      .from('scan_jobs')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(5)

    if (data) setRecentScans(data)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    // TODO: 呼叫後端 API 建立掃描任務
    // 這裡暫時模擬一個 API 呼叫，實際應呼叫後端服務
    console.log('Starting analysis for:', url)
    
    // 延遲模擬
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    setLoading(false)
    setUrl('')
    fetchRecentScans()
  }

  return (
    <div className="max-w-4xl mx-auto py-10">
      {/* 主卡片 */}
      <div className="bg-white dark:bg-brand-navy/50 p-12 rounded-[2.5rem] border border-brand-navy/5 dark:border-brand-light/5 shadow-2xl relative overflow-hidden group">
        {/* Background glow */}
        <div className="absolute -top-24 -right-24 w-64 h-64 bg-brand-blue/5 rounded-full blur-3xl group-hover:bg-brand-blue/10 transition-colors" />
        
        <div className="relative">
          <h1 className="text-4xl md:text-5xl font-black text-brand-navy dark:text-brand-light mb-4 text-center tracking-tight">
            開始一次網站可信度健檢
          </h1>
          
          <p className="text-center text-xl text-brand-slate dark:text-brand-light/60 mb-12 max-w-2xl mx-auto leading-relaxed">
            適合內容創作者、行銷人、品牌網站、公司官網。<br />
            輸入網址，讓 AI 告訴你如何提升權威感。
          </p>
          
          <form onSubmit={handleSubmit} className="space-y-6 max-w-2xl mx-auto">
            <div className="relative group/input">
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
            
            <button
              type="submit"
              disabled={loading}
              className="w-full py-6 bg-brand-blue text-white rounded-2xl font-black text-2xl hover:bg-brand-blue/90 hover:scale-[1.02] active:scale-[0.98] transition-all shadow-xl shadow-brand-blue/25 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
            >
              {loading ? (
                <>
                  <div className="w-6 h-6 border-4 border-white/30 border-t-white rounded-full animate-spin" />
                  分析中...
                </>
              ) : '立即開始分析'}
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
          <button className="text-brand-blue font-bold hover:underline">
            查看全部
          </button>
        </div>
        
        {recentScans.length === 0 ? (
          <div className="bg-white/50 dark:bg-brand-navy/30 border-2 border-dashed border-brand-navy/5 dark:border-brand-light/5 rounded-[2rem] py-16 text-center">
            <p className="text-brand-slate dark:text-brand-light/40 text-lg font-medium">
              尚未有檢查記錄，立即輸入網址開始第一次分析吧！
            </p>
          </div>
        ) : (
          <div className="grid gap-4">
            {recentScans.map((scan) => (
              <div key={scan.id} className="bg-white dark:bg-brand-navy/40 p-6 rounded-2xl border border-brand-navy/5 dark:border-brand-light/5 flex items-center justify-between group hover:border-brand-blue/20 transition-all cursor-pointer">
                <div>
                  <div className="text-lg font-bold text-brand-navy dark:text-brand-light mb-1 group-hover:text-brand-blue transition-colors">
                    {scan.url}
                  </div>
                  <div className="text-sm text-brand-slate dark:text-brand-light/40 font-medium">
                    {new Date(scan.created_at).toLocaleDateString()} • {new Date(scan.created_at).toLocaleTimeString()}
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <span className={`px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-tighter ${
                    scan.status === 'completed' ? 'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400' :
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
