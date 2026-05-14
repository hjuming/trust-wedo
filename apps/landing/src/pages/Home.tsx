import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { Navigation } from '../components/Navigation'
import { Footer } from '../components/Footer'
import { PricingSection } from '../components/PricingSection'
import { getApiBaseUrl } from '../lib/api'

type ResearchModule = {
  id: string
  title: string
  audience: string
  stage: string
  domain: string
  summary: string
  details: string
  aio: string
}

type DataDomain = {
  key?: string
  id?: string
  name?: string
  name_zh?: string
  title?: string
  scope?: string
  role?: string
  typical_questions?: string[]
}

type DomainsResponse = {
  success?: boolean
  domains?: DataDomain[] | { domains?: DataDomain[] }
}

const workflowSteps = [
  {
    title: '資料定位',
    description: '依照查核目的選擇資料領域、公開資料來源與研究模組，先建立可追溯的查詢路徑。',
  },
  {
    title: '交叉查核',
    description: '透過 Worker 代理層串接 Twinkle Hub MCP，避免前端直連外部服務與金鑰外洩。',
  },
  {
    title: '可引用摘要',
    description: '輸出查詢條件、資料來源、限制與建議下一步，讓團隊能用一致格式交付研究結果。',
  },
]

function getDomainLabel(domain: DataDomain) {
  return domain.name_zh || domain.name || domain.title || domain.key || domain.id || '資料領域'
}

function normalizeDomains(payload: DomainsResponse): DataDomain[] {
  if (Array.isArray(payload.domains)) {
    return payload.domains
  }

  if (payload.domains && Array.isArray(payload.domains.domains)) {
    return payload.domains.domains
  }

  return []
}

function LabConsole({
  modules,
  domains,
  loading,
  error,
}: {
  modules: ResearchModule[]
  domains: DataDomain[]
  loading: boolean
  error: string | null
}) {
  const [selectedDomain, setSelectedDomain] = useState('')
  const [query, setQuery] = useState('鯨魚肚國際行銷有限公司')

  const featuredModules = useMemo(() => modules.slice(0, 4), [modules])
  const activeDomain = selectedDomain || domains[0]?.key || domains[0]?.id || ''

  return (
    <div id="lab-console" className="bg-white/95 text-brand-navy dark:bg-brand-light/95 rounded-3xl border border-white/40 shadow-2xl p-6 md:p-8">
      <div className="flex flex-col gap-2 mb-6">
        <span className="text-xs font-bold tracking-[0.2em] uppercase text-brand-blue">
          Agent Lab Console
        </span>
        <h2 className="text-2xl md:text-3xl font-black tracking-tight">
          先選資料，再啟動查核
        </h2>
        <p className="text-sm md:text-base text-brand-slate leading-relaxed">
          目前已接上 Cloudflare Worker API，可讀取研究模組與 MCP 資料領域。
        </p>
      </div>

      <div className="grid gap-4">
        <label className="grid gap-2">
          <span className="text-sm font-bold text-brand-navy/70">查核線索</span>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            className="w-full rounded-2xl border border-brand-navy/10 bg-brand-light px-4 py-4 text-base font-semibold outline-none transition focus:border-brand-blue focus:ring-4 focus:ring-brand-blue/15"
            placeholder="輸入公司、品牌、議題或公開資料線索"
          />
        </label>

        <label className="grid gap-2">
          <span className="text-sm font-bold text-brand-navy/70">資料領域</span>
          <select
            value={activeDomain}
            onChange={(event) => setSelectedDomain(event.target.value)}
            className="w-full rounded-2xl border border-brand-navy/10 bg-brand-light px-4 py-4 text-base font-semibold outline-none transition focus:border-brand-blue focus:ring-4 focus:ring-brand-blue/15"
          >
            {domains.length === 0 && <option value="">載入資料領域中</option>}
            {domains.map((domain, index) => {
              const value = domain.key || domain.id || String(index)
              return (
                <option key={value} value={value}>
                  {getDomainLabel(domain)}
                </option>
              )
            })}
          </select>
        </label>
      </div>

      <div className="mt-6 flex flex-wrap gap-2">
        {featuredModules.length > 0 ? (
          featuredModules.map((module) => (
            <span
              key={module.id}
              className="rounded-full border border-brand-blue/20 bg-brand-blue/5 px-3 py-2 text-sm font-bold text-brand-blue"
            >
              {module.title}
            </span>
          ))
        ) : (
          <span className="rounded-full border border-brand-navy/10 px-3 py-2 text-sm font-bold text-brand-slate">
            研究模組載入中
          </span>
        )}
      </div>

      <div className="mt-8 grid grid-cols-3 gap-3 text-center">
        <div className="rounded-2xl bg-brand-light p-4">
          <div className="text-2xl font-black text-brand-blue">{domains.length || '-'}</div>
          <div className="text-xs font-bold text-brand-slate">資料領域</div>
        </div>
        <div className="rounded-2xl bg-brand-light p-4">
          <div className="text-2xl font-black text-brand-blue">{modules.length || '-'}</div>
          <div className="text-xs font-bold text-brand-slate">研究模組</div>
        </div>
        <div className="rounded-2xl bg-brand-light p-4">
          <div className="text-2xl font-black text-brand-blue">{loading ? '...' : error ? '!' : 'OK'}</div>
          <div className="text-xs font-bold text-brand-slate">API 狀態</div>
        </div>
      </div>

      {error && (
        <p className="mt-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700">
          {error}
        </p>
      )}

      <div className="mt-8 flex flex-col sm:flex-row gap-3">
        <Link
          to="/entity-check"
          className="inline-flex flex-1 items-center justify-center rounded-2xl bg-brand-blue px-6 py-4 text-base font-black text-white transition hover:bg-brand-blue/90"
        >
          開始實體查核
        </Link>
        <a
          href="#modules"
          className="inline-flex flex-1 items-center justify-center rounded-2xl border border-brand-navy/10 px-6 py-4 text-base font-black text-brand-navy transition hover:border-brand-blue hover:text-brand-blue"
        >
          查看研究模組
        </a>
      </div>
    </div>
  )
}

function ModulesSection({
  modules,
  domains,
}: {
  modules: ResearchModule[]
  domains: DataDomain[]
}) {
  const visibleModules = modules.slice(0, 6)
  const visibleDomains = domains.slice(0, 8)

  return (
    <section id="modules" className="bg-white py-20 dark:bg-brand-navy/40">
      <div className="mx-auto grid max-w-7xl gap-12 px-6 lg:grid-cols-[0.9fr_1.1fr]">
        <div>
          <span className="text-sm font-black tracking-[0.2em] text-brand-blue uppercase">
            Research Modules
          </span>
          <h2 className="mt-4 text-3xl md:text-5xl font-black tracking-tight text-brand-navy dark:text-brand-light">
            從單點查詢，整理成可複用的研究路徑
          </h2>
          <p className="mt-6 text-lg leading-relaxed text-brand-slate dark:text-brand-light/70">
            Agent Lab 不只回答一次查詢，而是協助團隊把資料來源、判讀邏輯與引用限制整理成一致的查核流程。
          </p>

          <div className="mt-8 flex flex-wrap gap-2">
            {visibleDomains.map((domain, index) => (
              <span
                key={domain.key || domain.id || index}
                className="rounded-full border border-brand-navy/10 px-3 py-2 text-sm font-bold text-brand-slate dark:border-brand-light/10 dark:text-brand-light/70"
              >
                {getDomainLabel(domain)}
              </span>
            ))}
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          {visibleModules.map((module) => (
            <article
              key={module.id}
              className="rounded-2xl border border-brand-navy/10 bg-brand-light p-6 transition hover:border-brand-blue/40 dark:border-brand-light/10 dark:bg-brand-navy/70"
            >
              <div className="mb-4 flex items-center justify-between gap-3">
                <span className="rounded-full bg-brand-blue/10 px-3 py-1 text-xs font-black uppercase tracking-wide text-brand-blue">
                  {module.domain}
                </span>
                <span className="text-xs font-bold text-brand-slate dark:text-brand-light/50">
                  {module.stage}
                </span>
              </div>
              <h3 className="text-xl font-black text-brand-navy dark:text-brand-light">
                {module.title}
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-brand-slate dark:text-brand-light/70">
                {module.summary}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}

function WorkflowSection() {
  return (
    <section className="bg-brand-light py-20 dark:bg-brand-navy">
      <div className="mx-auto max-w-7xl px-6">
        <div className="max-w-3xl">
          <span className="text-sm font-black tracking-[0.2em] text-brand-blue uppercase">
            Operating Model
          </span>
          <h2 className="mt-4 text-3xl md:text-5xl font-black tracking-tight text-brand-navy dark:text-brand-light">
            為公關、研究與決策團隊設計的查核工作流
          </h2>
        </div>

        <div className="mt-12 grid gap-4 md:grid-cols-3">
          {workflowSteps.map((step, index) => (
            <article
              key={step.title}
              className="border-l-4 border-brand-blue bg-white p-6 shadow-sm dark:bg-brand-navy/60"
            >
              <div className="mb-5 text-sm font-black text-brand-blue">
                0{index + 1}
              </div>
              <h3 className="text-2xl font-black text-brand-navy dark:text-brand-light">
                {step.title}
              </h3>
              <p className="mt-4 leading-relaxed text-brand-slate dark:text-brand-light/70">
                {step.description}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}

export default function Home() {
  const [modules, setModules] = useState<ResearchModule[]>([])
  const [domains, setDomains] = useState<DataDomain[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const apiBaseUrl = getApiBaseUrl()

    if (!apiBaseUrl) {
      setError('尚未設定 VITE_API_URL，首頁將暫時無法讀取 Agent Lab API。')
      setLoading(false)
      return
    }

    async function loadLabData() {
      try {
        const [modulesResponse, domainsResponse] = await Promise.all([
          fetch(`${apiBaseUrl}/api/research/modules`),
          fetch(`${apiBaseUrl}/api/mcp/domains`),
        ])

        if (!modulesResponse.ok || !domainsResponse.ok) {
          throw new Error('Agent Lab API 暫時無法讀取。')
        }

        const modulesPayload = (await modulesResponse.json()) as ResearchModule[]
        const domainsPayload = (await domainsResponse.json()) as DomainsResponse

        setModules(Array.isArray(modulesPayload) ? modulesPayload : [])
        setDomains(normalizeDomains(domainsPayload))
        setError(null)
      } catch (fetchError) {
        console.error(fetchError)
        setError('無法連線 Agent Lab API，請稍後再試。')
      } finally {
        setLoading(false)
      }
    }

    void loadLabData()
  }, [])

  return (
    <div className="min-h-screen bg-brand-light dark:bg-brand-navy transition-colors duration-300">
      <Navigation />
      <main>
        <section className="bg-brand-navy pt-32 pb-20 text-white md:pt-40 md:pb-28">
          <div className="mx-auto grid max-w-7xl items-center gap-12 px-6 lg:grid-cols-[1.05fr_0.95fr]">
            <div>
              <div className="mb-8 inline-flex items-center gap-3 rounded-full border border-brand-blue/40 bg-brand-blue/10 px-4 py-2 text-sm font-black text-brand-cyan">
                <span className="h-2 w-2 rounded-full bg-brand-cyan" />
                WEDO 資料查核 Agent Lab
              </div>
              <h1 className="max-w-4xl text-5xl font-black leading-[1.05] tracking-tight md:text-7xl">
                把公開資料，變成可信任的查核流程
              </h1>
              <p className="mt-8 max-w-2xl text-xl leading-relaxed text-brand-light/80 md:text-2xl">
                輸入公司、議題或資料線索，Agent Lab 會協助你選擇資料領域、建立研究路徑，輸出可追溯的查核摘要。
              </p>
              <div className="mt-10 flex flex-col gap-3 sm:flex-row">
                <Link
                  to="/entity-check"
                  className="inline-flex items-center justify-center rounded-2xl bg-brand-blue px-8 py-5 text-lg font-black text-white transition hover:bg-brand-blue/90"
                >
                  開始資料查核
                </Link>
                <a
                  href="#modules"
                  className="inline-flex items-center justify-center rounded-2xl border border-white/20 px-8 py-5 text-lg font-black text-white transition hover:border-brand-cyan hover:text-brand-cyan"
                >
                  瀏覽研究模組
                </a>
              </div>
            </div>

            <LabConsole modules={modules} domains={domains} loading={loading} error={error} />
          </div>
        </section>

        <ModulesSection modules={modules} domains={domains} />
        <WorkflowSection />
        <PricingSection />
      </main>
      <Footer />
    </div>
  )
}
