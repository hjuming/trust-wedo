import { useTranslation } from 'react-i18next'
import { EntityCheckResult } from '../../types/entityCheck'

interface EntityCheckReportProps {
  result: EntityCheckResult
}

function formatCurrency(value?: number) {
  if (!value) return '資料未提供'
  return `NT$ ${value.toLocaleString('zh-TW')}`
}

function getStatusTone(status: string) {
  switch (status.toLowerCase()) {
    case '核准設立':
    case '核准變更':
      return 'bg-emerald-50 text-emerald-700 border-emerald-200'
    case '撤銷':
    case '廢止':
      return 'bg-red-50 text-red-700 border-red-200'
    case '停業':
    case '歇業':
      return 'bg-amber-50 text-amber-700 border-amber-200'
    default:
      return 'bg-brand-light text-brand-slate border-brand-navy/10'
  }
}

function Field({
  label,
  value,
}: {
  label: string
  value: string | number
}) {
  return (
    <div>
      <dt className="text-sm font-black text-brand-slate">{label}</dt>
      <dd className="mt-2 text-lg font-bold leading-relaxed text-brand-navy">{value}</dd>
    </div>
  )
}

export default function EntityCheckReport({ result }: EntityCheckReportProps) {
  const { t } = useTranslation()
  const trustScore = result.websiteAnalysis?.trustScore || 0
  const hasRisks = result.riskSignals.length > 0

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <section className="rounded-3xl bg-brand-navy p-6 text-white shadow-xl md:p-8">
        <div className="grid gap-6 md:grid-cols-[1fr_auto] md:items-end">
          <div>
            <span className="text-xs font-black uppercase tracking-[0.2em] text-brand-cyan">
              Verification Report
            </span>
            <h2 className="mt-3 text-3xl font-black tracking-tight md:text-4xl">
              {t('entityCheck.report.title', '企業實體查核報告')}
            </h2>
            <p className="mt-3 text-brand-light/70">
              {t('entityCheck.report.generatedAt', '生成時間')}：{new Date(result.generatedAt).toLocaleString('zh-TW')}
            </p>
          </div>
          <div className="rounded-2xl border border-brand-blue/30 bg-brand-blue/10 px-6 py-5 text-left md:text-right">
            <div className="text-sm font-bold text-brand-light/70">
              {t('entityCheck.report.trustScore', '信任評分')}
            </div>
            <div className="mt-1 text-4xl font-black text-brand-blue">{trustScore}/100</div>
          </div>
        </div>
      </section>

      <section className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
        <article className="rounded-3xl border border-brand-navy/10 bg-white p-6 shadow-sm md:p-8">
          <div className="mb-8 flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <span className="text-xs font-black uppercase tracking-[0.2em] text-brand-blue">
                Registry Data
              </span>
              <h3 className="mt-3 text-2xl font-black text-brand-navy">
                {t('entityCheck.report.companyInfo', '公司基本資料')}
              </h3>
            </div>
            <span className={`inline-flex w-fit items-center rounded-full border px-3 py-1 text-sm font-black ${getStatusTone(result.companyInfo.status)}`}>
              {result.companyInfo.status}
            </span>
          </div>

          <dl className="grid gap-6 md:grid-cols-2">
            <Field label={t('entityCheck.report.companyName', '公司名稱')} value={result.companyInfo.name} />
            <div>
              <dt className="text-sm font-black text-brand-slate">
                {t('entityCheck.report.taxId', '統一編號')}
              </dt>
              <dd className="mt-2 flex flex-wrap items-center gap-3">
                <span className="text-lg font-bold text-brand-navy">{result.companyInfo.taxId}</span>
                <span className={`rounded-full px-3 py-1 text-xs font-black ${result.validation.taxIdValid ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'}`}>
                  {result.validation.taxIdValid
                    ? t('entityCheck.report.valid', '驗證通過')
                    : t('entityCheck.report.invalid', '驗證失敗')}
                </span>
              </dd>
            </div>
            <Field
              label={t('entityCheck.report.address', '登記地址')}
              value={result.companyInfo.address || t('entityCheck.report.notAvailable', '資料未提供')}
            />
            <Field
              label={t('entityCheck.report.registerAuthority', '登記機關')}
              value={result.companyInfo.registerAuthority || t('entityCheck.report.notAvailable', '資料未提供')}
            />
            <Field
              label={t('entityCheck.report.capitalAmount', '資本額')}
              value={formatCurrency(result.companyInfo.capitalAmount)}
            />
            {result.companyInfo.responsibleName && (
              <Field label="代表人" value={result.companyInfo.responsibleName} />
            )}
          </dl>
        </article>

        <article className="rounded-3xl border border-brand-navy/10 bg-white p-6 shadow-sm md:p-8">
          <span className="text-xs font-black uppercase tracking-[0.2em] text-brand-blue">
            Risk Signals
          </span>
          <h3 className="mt-3 text-2xl font-black text-brand-navy">
            {t('entityCheck.report.riskSignals', '風險訊號')}
          </h3>

          {hasRisks ? (
            <div className="mt-6 space-y-3">
              {result.riskSignals.map((signal, index) => (
                <div key={index} className="rounded-2xl border border-red-100 bg-red-50 p-4">
                  <div className="text-sm font-black text-red-700">{signal.title}</div>
                  <p className="mt-2 text-sm leading-relaxed text-red-700/80">{signal.description}</p>
                  <p className="mt-3 text-xs font-bold text-red-600">
                    {t('entityCheck.report.source', '來源')}：{signal.source}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <div className="mt-8 rounded-3xl border border-emerald-100 bg-emerald-50 p-6 text-center">
              <svg className="mx-auto h-14 w-14 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h4 className="mt-4 text-lg font-black text-emerald-700">
                {t('entityCheck.report.noRiskSignals', '未發現顯著風險訊號')}
              </h4>
              <p className="mt-2 text-sm leading-relaxed text-emerald-700/80">
                {t('entityCheck.report.noRiskSignalsDesc', '根據目前查詢的公開資料，未發現重大風險訊號')}
              </p>
            </div>
          )}
        </article>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        {result.websiteAnalysis && (
          <article className="rounded-3xl border border-brand-navy/10 bg-white p-6 shadow-sm md:p-8">
            <span className="text-xs font-black uppercase tracking-[0.2em] text-brand-blue">
              Website Signal
            </span>
            <h3 className="mt-3 text-2xl font-black text-brand-navy">
              {t('entityCheck.report.websiteAnalysis', '網站分析')}
            </h3>

            <div className="mt-8 grid gap-4 sm:grid-cols-3">
              <div>
                <div className="text-3xl font-black text-brand-blue">{result.websiteAnalysis.trustScore}/100</div>
                <div className="mt-1 text-sm font-bold text-brand-slate">
                  {t('entityCheck.report.trustScore', '信任評分')}
                </div>
              </div>
              <div>
                <div className="text-lg font-black text-brand-navy">
                  {result.websiteAnalysis.aiReadability === 'analyzing' ? '分析中' : result.websiteAnalysis.aiReadability}
                </div>
                <div className="mt-1 text-sm font-bold text-brand-slate">
                  {t('entityCheck.report.aiReadability', 'AI 可讀性')}
                </div>
              </div>
              <div className="sm:col-span-1">
                <a
                  href={result.websiteAnalysis.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="break-all text-lg font-black text-brand-navy underline decoration-brand-blue/30 underline-offset-4 hover:text-brand-blue"
                >
                  {result.websiteAnalysis.url}
                </a>
                <div className="mt-1 text-sm font-bold text-brand-slate">
                  {t('entityCheck.report.websiteUrl', '網站 URL')}
                </div>
              </div>
            </div>
          </article>
        )}

        <article className="rounded-3xl border border-brand-navy/10 bg-white p-6 shadow-sm md:p-8">
          <span className="text-xs font-black uppercase tracking-[0.2em] text-brand-blue">
            Sources
          </span>
          <h3 className="mt-3 text-2xl font-black text-brand-navy">
            {t('entityCheck.report.dataSources', '資料來源')}
          </h3>

          <div className="mt-6 space-y-3">
            {result.dataSources.map((source, index) => (
              <div key={index} className="flex flex-col gap-3 border-t border-brand-navy/10 pt-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h4 className="font-black text-brand-navy">{source.name}</h4>
                  <p className="mt-1 text-sm font-medium text-brand-slate">
                    {source.type} / {t('entityCheck.report.lastUpdated', '最後更新')}：{new Date(source.lastUpdated).toLocaleDateString('zh-TW')}
                  </p>
                </div>
                {source.url && (
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm font-black text-brand-blue hover:text-brand-blue/80"
                  >
                    {t('entityCheck.report.viewSource', '查看來源')} →
                  </a>
                )}
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="rounded-3xl border border-amber-200 bg-amber-50 p-6">
        <div className="flex gap-3">
          <svg className="mt-0.5 h-5 w-5 flex-none text-amber-500" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <div>
            <h3 className="text-sm font-black text-amber-800">
              {t('entityCheck.report.disclaimer.title', '重要聲明')}
            </h3>
            <p className="mt-2 text-sm leading-relaxed text-amber-800/80">
              {t('entityCheck.report.disclaimer.content', '本報告僅供參考，所有資料均來自公開來源。實際商業決策請諮詢專業顧問。本報告不構成法律意見或投資建議。')}
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}
