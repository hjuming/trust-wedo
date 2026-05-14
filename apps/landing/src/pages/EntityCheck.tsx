import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import EntityCheckForm from '../components/EntityCheck/EntityCheckForm'
import EntityCheckReport from '../components/EntityCheck/EntityCheckReport'
import { getApiBaseUrl } from '../lib/api'
import { EntityCheckResult } from '../types/entityCheck'

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

      const apiResult = await response.json()

      if (!apiResult.success) {
        throw new Error(apiResult.error || 'Entity check failed')
      }

      const safeJsonParse = (raw: unknown) => {
        if (typeof raw !== 'string') return null
        try {
          return JSON.parse(raw)
        } catch {
          return null
        }
      }

      const normalizeApiContent = (source: unknown) => {
        if (!source || typeof source !== 'object') return null
        const content = (source as any).content
        if (Array.isArray(content) && content[0]?.text) {
          return safeJsonParse(content[0].text) || null
        }
        return source
      }

      const companyPayload = normalizeApiContent(apiResult.data?.company)
      const validationPayload = normalizeApiContent(apiResult.data?.validation)

      const companyInfo = {
        name: companyPayload?.company_name || data.companyName,
        taxId: data.taxId,
        status: companyPayload?.status || '未知',
        address: companyPayload?.address || '',
        registerAuthority: companyPayload?.register_authority || '',
        capitalAmount: companyPayload?.capital_amount,
        responsibleName: companyPayload?.responsible_name || '',
      }

      const validationInfo = {
        taxIdValid: validationPayload?.valid || false,
        rule: validationPayload?.rule || '',
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
    <div className="min-h-screen bg-gradient-to-br from-brand-light via-white to-brand-light/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-brand-navy dark:text-brand-light mb-4">
            {t('entityCheck.title', '企業實體查核')}
          </h1>
          <p className="text-xl text-brand-slate dark:text-brand-light/80 max-w-3xl mx-auto">
            {t('entityCheck.subtitle', '輸入公司名稱、統一編號與網站 URL，獲取公開資料版企業信任報告')}
          </p>
        </div>

        {/* Form */}
        <div className="mb-12">
          <EntityCheckForm onSubmit={handleCheck} loading={loading} />
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-8 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
                  {t('entityCheck.error.title', '查核失敗')}
                </h3>
                <div className="mt-2 text-sm text-red-700 dark:text-red-300">
                  {error}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Report */}
        {result && (
          <EntityCheckReport result={result} />
        )}
      </div>
    </div>
  )
}
