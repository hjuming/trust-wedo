import { useMemo, useState, type FormEvent, type ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { Navigation } from '../components/Navigation'
import { Footer } from '../components/Footer'
import { getApiBaseUrl } from '../lib/api'

type ExamQuestionHit = {
  paper_id: string
  exam_year?: string | number
  exam_year_西元?: number
  exam_name?: string
  subject_name?: string
  question_no?: string | number
  question_type?: string
  stem?: string
  options?: Record<string, string>
  answer?: string | null
  similarity?: number
  question_pdf_url?: string
  answer_pdf_url?: string
}

type ExamSearchResponse = {
  success?: boolean
  n_corpus?: number
  n_returned?: number
  query?: string
  hits?: ExamQuestionHit[]
  error?: string
  detail?: string
}

const sampleHits: ExamQuestionHit[] = [
  {
    paper_id: 'sample-admin-law-01',
    exam_year: '112',
    exam_year_西元: 2023,
    exam_name: '公務人員高等考試三級考試暨普通考試',
    subject_name: '行政法',
    question_no: 2,
    question_type: '申論題',
    stem: '某市政府核發營業許可後，發現原處分作成時所依據之事實認定有誤。試說明行政機關得否撤銷該授益行政處分、應考量之信賴保護原則，以及可能涉及之補償問題。',
    answer: null,
    similarity: 0.812,
  },
  {
    paper_id: 'sample-admin-law-02',
    exam_year: '110',
    exam_year_西元: 2021,
    exam_name: '地方政府公務人員特種考試',
    subject_name: '行政法概要',
    question_no: 12,
    question_type: '測驗題',
    stem: '下列何者最符合行政程序法有關違法行政處分撤銷之敘述？',
    options: {
      A: '授益處分一律不得撤銷',
      B: '撤銷時應兼顧公益與人民信賴利益',
      C: '只要違法即不得給予補償',
      D: '行政機關撤銷處分無須說明理由',
    },
    answer: 'B',
    similarity: 0.786,
  },
]

const quickQueries = ['行政處分 撤銷', '民法 侵權行為', '刑法 正當防衛', '公司法 董事責任']
const examTypes = ['全部', '高等考試', '普通考試', '司法官', '律師', '地方特考', '鐵路人員']
const subjects = ['全部', '行政法', '民法', '刑法', '公司法', '憲法', '英文']

const labSteps = [
  {
    label: '01',
    title: '題目定位',
    body: '用概念、法條或爭點搜尋，不必先知道完整年度與試卷名稱。',
  },
  {
    label: '02',
    title: '脈絡整理',
    body: '把年度、考科、題型、題號與 paper_id 放在同一個查詢結果裡。',
  },
  {
    label: '03',
    title: '複習提問',
    body: '將相似題整理成練習路徑，再交給 Agent 拆考點與建立答題架構。',
  },
]

function displayYear(hit: ExamQuestionHit) {
  if (hit.exam_year_西元) return hit.exam_year_西元
  const rocYear = Number(hit.exam_year)
  return Number.isFinite(rocYear) ? rocYear + 1911 : '未知年份'
}

function displayScore(hit: ExamQuestionHit) {
  if (typeof hit.similarity !== 'number') return 'N/A'
  return `${Math.round(hit.similarity * 100)}`
}

function optionLines(hit: ExamQuestionHit) {
  if (!hit.options) return []
  return Object.entries(hit.options).map(([key, value]) => `${key}. ${value}`)
}

function hitKey(hit: ExamQuestionHit) {
  return `${hit.paper_id}-${hit.question_no ?? 'q'}`
}

function apiPath(path: string) {
  const apiBaseUrl = getApiBaseUrl()
  return `${apiBaseUrl}${path}`
}

export default function ExamBank() {
  const [query, setQuery] = useState('行政處分 撤銷')
  const [examType, setExamType] = useState('全部')
  const [subject, setSubject] = useState('全部')
  const [questionType, setQuestionType] = useState('全部')
  const [yearFrom, setYearFrom] = useState('2012')
  const [yearTo, setYearTo] = useState('2025')
  const [hits, setHits] = useState<ExamQuestionHit[]>(sampleHits)
  const [selectedKey, setSelectedKey] = useState(hitKey(sampleHits[0]))
  const [status, setStatus] = useState<'idle' | 'loading' | 'ready' | 'error'>('idle')
  const [message, setMessage] = useState('目前顯示示範結果；送出查詢後會透過 Trust WEDO API 呼叫國考題庫索引。')
  const [corpusCount, setCorpusCount] = useState(320663)

  const selected = useMemo(
    () => hits.find((hit) => hitKey(hit) === selectedKey) || hits[0],
    [hits, selectedKey],
  )

  async function searchExamQuestions(event?: FormEvent) {
    event?.preventDefault()
    const trimmedQuery = query.trim()
    if (!trimmedQuery) {
      setStatus('error')
      setMessage('請先輸入查詢概念。')
      return
    }

    setStatus('loading')
    setMessage('正在透過 Trust WEDO API 查詢國考題目級語意索引...')

    try {
      const response = await fetch(apiPath('/api/mcp/exam/questions'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: trimmedQuery,
          exam_name_contains: examType === '全部' ? undefined : examType,
          subject_contains: subject === '全部' ? undefined : subject,
          question_type: questionType === '全部' ? undefined : questionType,
          year_from: Number(yearFrom) || undefined,
          year_to: Number(yearTo) || undefined,
          limit: 12,
        }),
      })

      const payload = (await response.json()) as ExamSearchResponse
      if (!response.ok || !payload.success) {
        throw new Error(payload.error || payload.detail || '國考題庫 API 暫時無法查詢。')
      }

      const nextHits = payload.hits || []
      setHits(nextHits.length > 0 ? nextHits : [])
      setSelectedKey(nextHits[0] ? hitKey(nextHits[0]) : '')
      setCorpusCount(payload.n_corpus || corpusCount)
      setStatus('ready')
      setMessage(`已查詢國考題庫：回傳 ${payload.n_returned ?? nextHits.length} 題，語料庫 ${Number(payload.n_corpus || corpusCount).toLocaleString()} 題。`)
    } catch (error) {
      setStatus('error')
      setMessage(error instanceof Error ? error.message : '國考題庫 API 暫時無法查詢。')
    }
  }

  return (
    <div className="min-h-screen overflow-x-hidden bg-[#f6f2ea] text-brand-navy dark:bg-brand-navy">
      <Navigation />

      <main className="w-full pt-28 md:pt-32">
        <section className="mx-auto grid w-full max-w-7xl gap-6 px-4 pb-10 sm:px-6 lg:grid-cols-[minmax(0,1.02fr)_minmax(0,0.98fr)]">
          <div className="w-full min-w-0 max-w-full overflow-hidden rounded-2xl border border-black/10 bg-white/85 p-5 shadow-2xl shadow-slate-900/5 sm:p-6 md:p-10">
            <div className="text-xs font-black uppercase text-brand-blue">
              Trust WEDO Service
            </div>
            <h1 className="mt-5 max-w-full break-words font-serif text-3xl font-black leading-tight sm:text-5xl md:text-7xl">
              國考題庫 Agent Lab
            </h1>
            <p className="mt-6 max-w-2xl break-words text-lg leading-relaxed text-brand-slate">
              串接國家考試題庫索引，支援 2012-2025 試卷與題目級語意搜尋，讓考生與研究團隊快速定位題目、整理引用與建立複習路徑。
            </p>
            <div className="mt-8 grid min-w-0 gap-3 sm:grid-cols-3">
              <Metric label="試卷" value="64,815" />
              <Metric label="題目語料" value={corpusCount.toLocaleString()} />
              <Metric label="年份" value="2012-2025" />
            </div>
          </div>

          <div className="w-full min-w-0 max-w-full overflow-hidden rounded-2xl border border-brand-blue/20 bg-[#0c1118] text-white shadow-2xl shadow-slate-900/20">
            <div className="flex items-center gap-2 border-b border-white/10 px-5 py-4">
              <span className="h-3 w-3 rounded-full bg-red-400" />
              <span className="h-3 w-3 rounded-full bg-yellow-400" />
              <span className="h-3 w-3 rounded-full bg-green-400" />
              <span className="ml-3 text-sm font-black text-slate-200">Exam Semantic Search</span>
            </div>
            <div className="grid min-w-0 gap-4 p-4 sm:p-5">
              <div className="max-w-full break-words rounded-2xl border border-white/10 bg-white/10 px-4 py-3 text-sm sm:justify-self-end">
                請找行政法中有關行政處分撤銷的題目
              </div>
              {['定位相關題目與試卷', '保留來源、年份與題號', '產出可引用查詢摘要'].map((item) => (
                <article key={item} className="min-w-0 rounded-2xl border border-white/10 bg-white/[0.06] p-4">
                  <b className="text-sm text-sky-300">{item}</b>
                  <p className="mt-2 text-sm leading-relaxed text-slate-300">
                    由後端代理呼叫題庫索引，避免前端暴露任何金鑰。
                  </p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="mx-auto grid w-full max-w-7xl gap-6 px-4 pb-14 sm:px-6 lg:grid-cols-[360px_minmax(0,1fr)]">
          <aside className="w-full min-w-0 max-w-full self-start rounded-2xl border border-black/10 bg-white p-5 shadow-xl shadow-slate-900/5">
            <form className="grid gap-4" onSubmit={searchExamQuestions}>
              <label className="grid min-w-0 gap-2">
                <span className="text-sm font-black text-brand-slate">搜尋題目</span>
                <input
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  className="w-full min-w-0 rounded-2xl border border-brand-navy/10 bg-brand-light px-4 py-4 font-bold outline-none transition focus:border-brand-blue focus:ring-4 focus:ring-brand-blue/15"
                  placeholder="輸入考科、題幹或概念"
                />
              </label>

              <div className="grid gap-3">
                <Select label="考試類別" value={examType} options={examTypes} onChange={setExamType} />
                <Select label="考科" value={subject} options={subjects} onChange={setSubject} />
                <Select label="題型" value={questionType} options={['全部', '申論題', '測驗題']} onChange={setQuestionType} />
              </div>

              <div className="grid min-w-0 grid-cols-2 gap-3">
                <label className="grid min-w-0 gap-2">
                  <span className="text-sm font-black text-brand-slate">起年</span>
                  <input className="w-full min-w-0 rounded-2xl border border-brand-navy/10 px-4 py-3 font-bold" value={yearFrom} onChange={(event) => setYearFrom(event.target.value)} />
                </label>
                <label className="grid min-w-0 gap-2">
                  <span className="text-sm font-black text-brand-slate">迄年</span>
                  <input className="w-full min-w-0 rounded-2xl border border-brand-navy/10 px-4 py-3 font-bold" value={yearTo} onChange={(event) => setYearTo(event.target.value)} />
                </label>
              </div>

              <button
                type="submit"
                disabled={status === 'loading'}
                className="w-full rounded-2xl bg-brand-blue px-5 py-4 text-base font-black text-white transition hover:bg-brand-blue/90 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {status === 'loading' ? '查詢中' : '搜尋國考題庫'}
              </button>
            </form>

            <div className="mt-5 flex flex-wrap gap-2">
              {quickQueries.map((item) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => setQuery(item)}
                  className="rounded-full border border-brand-blue/20 bg-brand-blue/5 px-3 py-2 text-sm font-black text-brand-blue"
                >
                  {item}
                </button>
              ))}
            </div>

            <div className={`mt-5 rounded-2xl border px-4 py-3 text-sm font-bold ${
              status === 'error'
                ? 'border-red-200 bg-red-50 text-red-700'
                : status === 'ready'
                  ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
                  : 'border-brand-navy/10 bg-brand-light text-brand-slate'
            }`}
            >
              {message}
            </div>
          </aside>

          <div className="w-full min-w-0 max-w-full overflow-hidden rounded-2xl border border-black/10 bg-white shadow-xl shadow-slate-900/5">
            <div className="flex flex-col gap-3 border-b border-black/10 px-5 py-4 md:flex-row md:items-center md:justify-between">
              <div>
                <h2 className="text-2xl font-black">{hits.length} 題符合條件</h2>
                <p className="text-sm font-semibold text-brand-slate">
                  資料來源：考選部公開試題，經國考題庫 Agent Lab 題目級索引處理。
                </p>
              </div>
              <Link to="/" className="text-sm font-black text-brand-blue">
                回 Trust WEDO
              </Link>
            </div>

            <div className="grid min-w-0 lg:grid-cols-[minmax(0,0.42fr)_minmax(0,0.58fr)]">
              <div className="max-h-[720px] overflow-auto border-b border-black/10 lg:border-b-0 lg:border-r">
                {hits.length === 0 ? (
                  <div className="m-5 rounded-2xl border border-dashed border-brand-navy/20 p-5 text-sm font-semibold text-brand-slate">
                    目前沒有符合條件的題目，請放寬年份或改用更短的查詢詞。
                  </div>
                ) : (
                  hits.map((hit) => (
                    <button
                      key={`${hit.paper_id}-${hit.question_no}`}
                      type="button"
                      onClick={() => setSelectedKey(hitKey(hit))}
                      className={`block w-full border-b border-black/10 p-5 text-left transition hover:bg-brand-blue/5 ${
                        selected && hitKey(selected) === hitKey(hit) ? 'bg-brand-blue/10 shadow-[inset_4px_0_0_#2563eb]' : ''
                      }`}
                    >
                      <span className="text-xs font-black text-brand-blue">
                        {displayYear(hit)} / {hit.question_type || '題目'} / 相關度 {displayScore(hit)}
                      </span>
                      <h3 className="mt-2 break-words text-base font-black leading-snug">
                        {hit.subject_name || '未標示科目'}｜{hit.exam_name || '國家考試'}
                      </h3>
                      <p className="mt-2 line-clamp-3 text-sm leading-relaxed text-brand-slate">
                        {hit.stem}
                      </p>
                    </button>
                  ))
                )}
              </div>

              {selected && (
                <article className="min-w-0 p-5 md:p-7">
                  <div className="flex flex-wrap gap-2">
                    {[displayYear(selected), selected.question_type, selected.subject_name, `第 ${selected.question_no ?? '-'} 題`].filter(Boolean).map((item) => (
                      <span key={String(item)} className="rounded-full bg-brand-navy px-3 py-1 text-xs font-black text-white">
                        {String(item)}
                      </span>
                    ))}
                  </div>
                  <h2 className="mt-5 break-words text-2xl font-black leading-tight md:text-3xl">
                    {selected.exam_name}
                  </h2>
                  <p className="mt-5 whitespace-pre-line break-words text-base leading-relaxed text-brand-navy">
                    {selected.stem}
                  </p>

                  {optionLines(selected).length > 0 && (
                    <div className="mt-5 grid gap-2 rounded-2xl bg-brand-light p-4">
                      {optionLines(selected).map((line) => (
                        <p key={line} className="text-sm font-semibold text-brand-slate">{line}</p>
                      ))}
                    </div>
                  )}

                  <div className="mt-5 grid gap-4 md:grid-cols-2">
                    <InfoBox title="官方答案">
                      {selected.answer || '此題未提供標準答案；申論題需另行整理與校對。'}
                    </InfoBox>
                    <InfoBox title="Agent 解題建議">
                      先確認題型與考點，再比對 PDF 原文；若為申論題，建議拆成定義、判準、步驟與結論。
                    </InfoBox>
                  </div>

                  <div className="mt-5 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm leading-relaxed text-amber-900">
                    <b>引用限制：</b>本頁僅供題庫檢索與學習研究參考。正式引用需附查詢日期、paper_id、原始 PDF，並人工確認答案與題幹完整性。
                    <div className="mt-2 break-all font-mono text-xs">paper_id: {selected.paper_id}</div>
                  </div>
                </article>
              )}
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-4 pb-20 sm:px-6">
          <div className="grid gap-6 rounded-2xl border border-black/10 bg-white p-5 shadow-xl shadow-slate-900/5 md:grid-cols-[0.9fr_1.1fr] md:p-8">
            <div className="min-w-0">
              <div className="text-xs font-black uppercase text-brand-blue">Agent Lab Method</div>
              <h2 className="mt-4 text-3xl font-black leading-tight text-brand-navy md:text-4xl">
                從一個爭點，展開一組可練習的國考題
              </h2>
              <p className="mt-5 text-base leading-relaxed text-brand-slate">
                國考題庫 Agent Lab 的重點不是只列出 PDF，而是把題目拆成可搜尋、可引用、可延伸提問的學習單元。考生可以從常見爭點出發，快速找到相似題，再整理成自己的複習筆記。
              </p>
            </div>

            <div className="grid gap-3">
              {labSteps.map((step) => (
                <article key={step.label} className="grid gap-3 rounded-2xl border border-brand-navy/10 bg-brand-light p-4 sm:grid-cols-[64px_minmax(0,1fr)]">
                  <div className="grid h-12 w-12 place-items-center rounded-2xl bg-brand-navy text-sm font-black text-white">
                    {step.label}
                  </div>
                  <div className="min-w-0">
                    <h3 className="text-base font-black text-brand-navy">{step.title}</h3>
                    <p className="mt-1 text-sm leading-relaxed text-brand-slate">{step.body}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-brand-navy/10 bg-brand-light p-4">
      <div className="text-sm font-black text-brand-slate">{label}</div>
      <div className="mt-2 text-2xl font-black text-brand-blue">{value}</div>
    </div>
  )
}

function Select({
  label,
  value,
  options,
  onChange,
}: {
  label: string
  value: string
  options: string[]
  onChange: (value: string) => void
}) {
  return (
    <label className="grid min-w-0 gap-2">
      <span className="text-sm font-black text-brand-slate">{label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="w-full min-w-0 rounded-2xl border border-brand-navy/10 bg-brand-light px-4 py-3 font-bold outline-none transition focus:border-brand-blue focus:ring-4 focus:ring-brand-blue/15"
      >
        {options.map((option) => <option key={option}>{option}</option>)}
      </select>
    </label>
  )
}

function InfoBox({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="rounded-2xl border border-brand-navy/10 bg-brand-light p-4">
      <h3 className="text-sm font-black text-brand-navy">{title}</h3>
      <p className="mt-3 text-sm leading-relaxed text-brand-slate">{children}</p>
    </div>
  )
}
