import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import EntityCheckForm from '../components/EntityCheck/EntityCheckForm'
import EntityCheckReport from '../components/EntityCheck/EntityCheckReport'
import { Footer } from '../components/Footer'
import { Navigation } from '../components/Navigation'
import { getApiBaseUrl } from '../lib/api'
import { EntityCheckResult } from '../types/entityCheck'

type ApiRecord = Record<string, unknown>

type EntityApiResponse = {
  success?: boolean
  error?: string
  data?: {
    company?: unknown
    validation?: unknown
  }
}

function isApiRecord(value: unknown): value is ApiRecord {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value)
}

function safeJsonParse(raw: unknown) {
  if (typeof raw !== 'string') return null
  try {
    const parsed = JSON.parse(raw)
    return isApiRecord(parsed) ? parsed : null
  } catch {
    return null
  }
}

function normalizeApiContent(source: unknown): ApiRecord | null {
  if (!isApiRecord(source)) return null
  const content = source.content
  if (Array.isArray(content) && isApiRecord(content[0]) && typeof content[0].text === 'string') {
    return safeJsonParse(content[0].text)
  }
  return source
}

function readString(source: ApiRecord | null, key: string, fallback = '') {
  const value = source?.[key]
  return typeof value === 'string' ? value : fallback
}

function readBoolean(source: ApiRecord | null, key: string, fallback = false) {
  const value = source?.[key]
  return typeof value === 'boolean' ? value : fallback
}

function readNumber(source: ApiRecord | null, key: string) {
  const value = source?.[key]
  return typeof value === 'number' ? value : undefined
}

export default function EntityCheck() {
  const { t } = useTranslation()
  const [result, setResult] = useState<EntityCheckResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleCheck = async (data: {
    companyName: string
    taxId: string
    websiteUrl: string
  }) => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const apiUrl = getApiBaseUrl()
      if (!apiUrl) {
        throw new Error('VITE_API_URL is not configured')
      }

      const response = await fetch(`${apiUrl}/api/trust/entity-check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tax_id: data.taxId,
          company_name: data.companyName,
          website_url: data.websiteUrl,
        }),
      })

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`)
      }

      const apiResult = await response.json() as EntityApiResponse

      if (!apiResult.success) {
        throw new Error(apiResult.error || 'Entity check failed')
      }

      const companyPayload = normalizeApiContent(apiResult.data?.company)
      const validationPayload = normalizeApiContent(apiResult.data?.validation)

      const companyInfo = {
        name: readString(companyPayload, 'company_name', data.companyName),
        taxId: data.taxId,
        status: readString(companyPayload, 'status', '未知'),
        address: readString(companyPayload, 'address'),
        registerAuthority: readString(companyPayload, 'register_authority'),
        capitalAmount: readNumber(companyPayload, 'capital_amount'),
        responsibleName: readString(companyPayload, 'responsible_name'),
      }

      const validationInfo = {
        taxIdValid: readBoolean(validationPayload, 'valid'),
        rule: readString(validationPayload, 'rule'),
      }

      const riskSignals = [] as EntityCheckResult['riskSignals']
      if (companyInfo.status === '撤銷' || companyInfo.status === '廢止') {
        riskSignals.push({
          title: '公司登記狀態異常',
          description: '公司已處於撤銷或廢止狀態，代表目前登記可能無法正常營運。',
          severity: 'high',
          source: '經濟部商業司',
        })
      } else if (companyInfo.status === '停業' || companyInfo.status === '歇業') {
        riskSignals.push({
          title: '公司登記為停業/歇業',
          description: '公司目前登記為停業或歇業，建議進一步確認營運狀態。',
          severity: 'medium',
          source: '經濟部商業司',
        })
      }

      if (!data.websiteUrl) {
        riskSignals.push({
          title: '缺少公司網站',
          description: '未提供公司網站，無法進一步分析 AI 可讀性與引用可信度。',
          severity: 'low',
          source: '使用者輸入',
        })
      }

      const calculateTrustScore = () => {
        let score = 50
        if (data.websiteUrl) score += 20
        if (companyInfo.status === '撤銷' || companyInfo.status === '廢止') score -= 30
        if (companyInfo.status === '停業' || companyInfo.status === '歇業') score -= 15
        return Math.max(0, Math.min(100, score))
      }

      const entityCheckResult: EntityCheckResult = {
        companyInfo,
        validation: validationInfo,
        riskSignals,
        websiteAnalysis: {
          url: data.websiteUrl,
          trustScore: calculateTrustScore(),
          aiReadability: data.websiteUrl ? '待分析' : '未提供網站',
          lastAnalyzed: new Date().toISOString(),
        },
        dataSources: [
          {
            name: '經濟部商業司',
            type: 'company_registration',
            lastUpdated: new Date().toISOString(),
            url: 'https://gcis.nat.gov.tw/',
          },
        ],
        generatedAt: new Date().toISOString(),
      }

      setResult(entityCheckResult)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-brand-light dark:bg-brand-navy transition-colors duration-300">
      <Navigation />

      <main>
        <section className="bg-brand-navy pt-32 pb-16 text-white md:pt-40 md:pb-24">
          <div className="mx-auto grid max-w-7xl items-center gap-12 px-6 lg:grid-cols-[1fr_0.95fr]">
            <div>
              <div className="mb-8 inline-flex items-center gap-3 rounded-full border border-brand-blue/40 bg-brand-blue/10 px-4 py-2 text-sm font-black text-brand-cyan">
                <span className="h-2 w-2 rounded-full bg-brand-cyan" />
                WEDO 資料查核 Agent Lab
              </div>

              <h1 className="max-w-3xl text-5xl font-black leading-[1.05] tracking-tight md:text-7xl">
                {t('entityCheck.title', '企業實體查核')}
              </h1>
              <p className="mt-8 max-w-2xl text-xl leading-relaxed text-brand-light/80 md:text-2xl">
                {t('entityCheck.subtitle', '輸入公司名稱、統一編號與網站 URL，獲取公開資料版企業信任報告')}
              </p>

              <div className="mt-10 grid max-w-xl gap-3 sm:grid-cols-3">
                {[
                  ['01', '統編驗證'],
                  ['02', '登記資料'],
                  ['03', '風險摘要'],
                ].map(([step, label]) => (
                  <div key={step} className="border-l-2 border-brand-blue/70 pl-4">
                    <div className="text-sm font-black text-brand-blue">{step}</div>
                    <div className="mt-1 text-sm font-bold text-brand-light/70">{label}</div>
                  </div>
                ))}
              </div>
            </div>

            <EntityCheckForm onSubmit={handleCheck} loading={loading} />
          </div>
        </section>

        {error && (
          <section className="bg-brand-light px-6 pt-10 dark:bg-brand-navy">
            <div className="mx-auto max-w-7xl rounded-3xl border border-red-200 bg-red-50 p-5 text-red-800">
              <div className="flex gap-3">
                <svg className="mt-0.5 h-5 w-5 flex-none text-red-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <div>
                  <h3 className="text-sm font-black">
                    {t('entityCheck.error.title', '查核失敗')}
                  </h3>
                  <p className="mt-1 text-sm font-medium">{error}</p>
                </div>
              </div>
            </div>
          </section>
        )}

        {result && (
          <section className="bg-brand-light px-6 py-14 dark:bg-brand-navy">
            <EntityCheckReport result={result} />
          </section>
        )}
      </main>

      <Footer />
    </div>
  )
}
