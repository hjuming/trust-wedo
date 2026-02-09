import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

export default function Report() {
  const { jobId } = useParams()
  const { t } = useTranslation()
  const [loading, setLoading] = useState(true)
  const [report, setReport] = useState<any>(null)

  useEffect(() => {
    // 模擬取得報告
    setTimeout(() => {
      setReport({
        id: jobId,
        status: 'completed',
        score: 72,
        conclusion: '你的網站已具備基本可信結構，但仍有改善空間',
        problems: [
          { emoji: '⚠️', title: '網站沒有清楚的「主體身份」', desc: 'AI 無法確認這個網站是由個人還是公司營運。' },
          { emoji: '🚫', title: '缺乏可驗證的引用來源', desc: '文章中的專業數據沒有連結到權威原始出處。' },
        ],
        recommendations: [
          { 
            title: '建議新增「關於我們」結構化資料', 
            desc: '優先級：高 | 預期效果：提升 AI 對網站身份的理解',
            action: '在首頁加入 Organization 類型的 Schema.org 標記'
          },
          { 
            title: '補齊作者背景介紹', 
            desc: '優先級：中 | 預期效果：增加內容的專業權威性',
            action: '在每篇文章下方加入作者簡介與 LinkedIn 連結'
          }
        ]
      })
      setLoading(false)
    }, 1500)
  }, [jobId])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="w-16 h-16 border-4 border-brand-blue/30 border-t-brand-blue rounded-full animate-spin mb-6" />
        <h2 className="text-2xl font-bold text-brand-navy dark:text-brand-light animate-pulse">正在產生成信度報告...</h2>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto py-10">
      <Link to="/dashboard" className="inline-flex items-center gap-2 text-brand-blue font-bold mb-8 hover:translate-x-[-4px] transition-transform">
        ← 返回健檢列表
      </Link>

      {/* 1. 一句話結論 */}
      <div className="bg-white dark:bg-brand-navy/50 p-10 rounded-[2.5rem] mb-8 border border-brand-navy/5 dark:border-brand-light/5 shadow-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8">
           <div className="w-24 h-24 rounded-full border-8 border-brand-blue/10 flex items-center justify-center relative">
              <span className="text-3xl font-black text-brand-blue">{report.score}</span>
              <svg className="absolute inset-0 w-full h-full -rotate-90">
                 <circle cx="48" cy="48" r="40" fill="transparent" stroke="currentColor" strokeWidth="8" strokeDasharray="251" strokeDashoffset={251 - (251 * report.score / 100)} className="text-brand-blue" />
              </svg>
           </div>
        </div>
        <div className="text-6xl mb-6">✅</div>
        <h1 className="text-3xl md:text-4xl font-black text-brand-navy dark:text-brand-light max-w-xl leading-tight">
          {report.conclusion}
        </h1>
      </div>
      
      <div className="grid md:grid-cols-2 gap-8 mb-8">
        {/* 2. 重點問題 */}
        <div className="bg-white dark:bg-brand-navy/50 p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-lg">
          <h2 className="text-xl font-black text-brand-navy dark:text-brand-light mb-6 flex items-center gap-2">
            <span className="w-2 h-8 bg-red-500 rounded-full" />
            目前的信任缺口
          </h2>
          <ul className="space-y-6">
            {report.problems.map((p: any, i: number) => (
              <li key={i} className="flex items-start gap-4">
                <span className="text-3xl">{p.emoji}</span>
                <div>
                  <div className="font-bold text-brand-navy dark:text-brand-light mb-1 leading-tight">
                    {p.title}
                  </div>
                  <div className="text-sm text-brand-slate dark:text-brand-light/60">
                    {p.desc}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
        
        {/* 3. 改善建議 */}
        <div className="bg-white dark:bg-brand-navy/50 p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-lg">
          <h2 className="text-xl font-black text-brand-navy dark:text-brand-light mb-6 flex items-center gap-2">
            <span className="w-2 h-8 bg-brand-success rounded-full" />
            建議採取的行動
          </h2>
          <ul className="space-y-6">
            {report.recommendations.map((r: any, i: number) => (
              <li key={i} className="flex items-start gap-4">
                <span className="text-2xl text-brand-success font-black">0{i+1}</span>
                <div>
                  <div className="font-bold text-brand-navy dark:text-brand-light mb-1 leading-tight">
                    {r.title}
                  </div>
                  <div className="text-xs font-black text-brand-blue uppercase tracking-tighter mb-2">
                    {r.desc}
                  </div>
                  <div className="p-3 bg-brand-light dark:bg-brand-navy rounded-xl text-sm text-brand-slate dark:text-brand-light/80 border border-brand-navy/5">
                    {r.action}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
      
      {/* 4. 進階檢視（折疊） */}
      <details className="group bg-brand-navy/5 dark:bg-brand-navy/30 rounded-[2rem] overflow-hidden transition-all">
        <summary className="p-8 font-black text-brand-navy dark:text-brand-light cursor-pointer list-none flex items-center justify-between">
          <span className="flex items-center gap-3">
             <span className="text-xl">🧬</span> 進階技術分析資料
          </span>
          <span className="text-brand-blue group-open:rotate-180 transition-transform font-black">↓</span>
        </summary>
        <div className="px-8 pb-8">
           <div className="bg-black/90 rounded-2xl p-6 font-mono text-sm text-green-400 overflow-x-auto shadow-inner">
             <pre>{JSON.stringify({ 
               entities: ["Person", "Organization"], 
               graph_completeness: "64%",
               schema_errors: 0,
               citation_density: 1.2
             }, null, 2)}</pre>
           </div>
        </div>
      </details>

      <div className="mt-12 text-center">
         <button className="px-10 py-4 bg-brand-navy dark:bg-brand-light text-white dark:text-brand-navy rounded-2xl font-black hover:scale-105 transition-all shadow-xl">
           匯出 PDF 報告
         </button>
      </div>
    </div>
  )
}
