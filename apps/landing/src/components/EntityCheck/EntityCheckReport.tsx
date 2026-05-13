import { useTranslation } from 'react-i18next'
import { EntityCheckResult } from '../../types/entityCheck'

interface EntityCheckReportProps {
  result: EntityCheckResult
}

export default function EntityCheckReport({ result }: EntityCheckReportProps) {
  const { t } = useTranslation()

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case '核准設立':
      case '核准變更':
        return 'text-green-600 bg-green-50 dark:bg-green-900/20'
      case '撤銷':
      case '廢止':
        return 'text-red-600 bg-red-50 dark:bg-red-900/20'
      case '停業':
      case '歇業':
        return 'text-yellow-600 bg-yellow-50 dark:bg-yellow-900/20'
      default:
        return 'text-gray-600 bg-gray-50 dark:bg-gray-900/20'
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Report Header */}
      <div className="bg-white dark:bg-brand-navy rounded-2xl shadow-xl p-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-brand-navy dark:text-brand-light mb-2">
              {t('entityCheck.report.title', '企業實體查核報告')}
            </h2>
            <p className="text-brand-slate dark:text-brand-light/80">
              {t('entityCheck.report.generatedAt', '生成時間')}: {new Date(result.generatedAt).toLocaleString('zh-TW')}
            </p>
          </div>
          <div className="text-right">
            <div className="text-sm text-brand-slate dark:text-brand-light/60">
              {t('entityCheck.report.trustScore', '信任評分')}
            </div>
            <div className="text-3xl font-bold text-brand-blue">
              {result.websiteAnalysis?.trustScore || 0}/100
            </div>
          </div>
        </div>
      </div>

      {/* Company Information */}
      <div className="bg-white dark:bg-brand-navy rounded-2xl shadow-xl p-8">
        <h3 className="text-xl font-semibold text-brand-navy dark:text-brand-light mb-6">
          {t('entityCheck.report.companyInfo', '公司基本資料')}
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-brand-slate dark:text-brand-light/60 mb-1">
                {t('entityCheck.report.companyName', '公司名稱')}
              </label>
              <p className="text-lg font-semibold text-brand-navy dark:text-brand-light">
                {result.companyInfo.name}
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-brand-slate dark:text-brand-light/60 mb-1">
                {t('entityCheck.report.taxId', '統一編號')}
              </label>
              <div className="flex items-center space-x-2">
                <p className="text-lg font-semibold text-brand-navy dark:text-brand-light">
                  {result.companyInfo.taxId}
                </p>
                {result.validation.taxIdValid ? (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400">
                    ✓ {t('entityCheck.report.valid', '驗證通過')}
                  </span>
                ) : (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400">
                    ✗ {t('entityCheck.report.invalid', '驗證失敗')}
                  </span>
                )}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-brand-slate dark:text-brand-light/60 mb-1">
                {t('entityCheck.report.status', '登記狀態')}
              </label>
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(result.companyInfo.status)}`}>
                {result.companyInfo.status}
              </span>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-brand-slate dark:text-brand-light/60 mb-1">
                {t('entityCheck.report.address', '登記地址')}
              </label>
              <p className="text-brand-navy dark:text-brand-light">
                {result.companyInfo.address || t('entityCheck.report.notAvailable', '資料未提供')}
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-brand-slate dark:text-brand-light/60 mb-1">
                {t('entityCheck.report.registerAuthority', '登記機關')}
              </label>
              <p className="text-brand-navy dark:text-brand-light">
                {result.companyInfo.registerAuthority || t('entityCheck.report.notAvailable', '資料未提供')}
              </p>
            </div>

            {result.companyInfo.capitalAmount && (
              <div>
                <label className="block text-sm font-medium text-brand-slate dark:text-brand-light/60 mb-1">
                  {t('entityCheck.report.capitalAmount', '資本額')}
                </label>
                <p className="text-brand-navy dark:text-brand-light">
                  NT$ {result.companyInfo.capitalAmount.toLocaleString()}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Risk Signals */}
      <div className="bg-white dark:bg-brand-navy rounded-2xl shadow-xl p-8">
        <h3 className="text-xl font-semibold text-brand-navy dark:text-brand-light mb-6">
          {t('entityCheck.report.riskSignals', '風險訊號')}
        </h3>

        {result.riskSignals.length > 0 ? (
          <div className="space-y-4">
            {result.riskSignals.map((signal, index) => (
              <div key={index} className="flex items-start space-x-3 p-4 bg-red-50 dark:bg-red-900/10 rounded-lg">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-red-800 dark:text-red-200">
                    {signal.title}
                  </h4>
                  <p className="mt-1 text-sm text-red-700 dark:text-red-300">
                    {signal.description}
                  </p>
                  <p className="mt-2 text-xs text-red-600 dark:text-red-400">
                    {t('entityCheck.report.source', '來源')}: {signal.source}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <svg className="mx-auto h-12 w-12 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-green-800 dark:text-green-200">
              {t('entityCheck.report.noRiskSignals', '未發現顯著風險訊號')}
            </h3>
            <p className="mt-1 text-sm text-green-600 dark:text-green-300">
              {t('entityCheck.report.noRiskSignalsDesc', '根據目前查詢的公開資料，未發現重大風險訊號')}
            </p>
          </div>
        )}
      </div>

      {/* Website Analysis */}
      {result.websiteAnalysis && (
        <div className="bg-white dark:bg-brand-navy rounded-2xl shadow-xl p-8">
          <h3 className="text-xl font-semibold text-brand-navy dark:text-brand-light mb-6">
            {t('entityCheck.report.websiteAnalysis', '網站分析')}
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-brand-blue mb-2">
                {result.websiteAnalysis.trustScore}/100
              </div>
              <div className="text-sm text-brand-slate dark:text-brand-light/60">
                {t('entityCheck.report.trustScore', '信任評分')}
              </div>
            </div>

            <div className="text-center">
              <div className="text-lg font-semibold text-brand-navy dark:text-brand-light mb-2">
                {result.websiteAnalysis.aiReadability === 'analyzing' ? '分析中...' : result.websiteAnalysis.aiReadability}
              </div>
              <div className="text-sm text-brand-slate dark:text-brand-light/60">
                {t('entityCheck.report.aiReadability', 'AI 可讀性')}
              </div>
            </div>

            <div className="text-center">
              <div className="text-lg font-semibold text-brand-navy dark:text-brand-light mb-2">
                {result.websiteAnalysis.url}
              </div>
              <div className="text-sm text-brand-slate dark:text-brand-light/60">
                {t('entityCheck.report.websiteUrl', '網站 URL')}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Data Sources */}
      <div className="bg-white dark:bg-brand-navy rounded-2xl shadow-xl p-8">
        <h3 className="text-xl font-semibold text-brand-navy dark:text-brand-light mb-6">
          {t('entityCheck.report.dataSources', '資料來源')}
        </h3>

        <div className="space-y-4">
          {result.dataSources.map((source, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-brand-light/50 dark:bg-brand-navy/50 rounded-lg">
              <div>
                <h4 className="font-medium text-brand-navy dark:text-brand-light">
                  {source.name}
                </h4>
                <p className="text-sm text-brand-slate dark:text-brand-light/60">
                  {source.type} • {t('entityCheck.report.lastUpdated', '最後更新')}: {new Date(source.lastUpdated).toLocaleDateString('zh-TW')}
                </p>
              </div>
              {source.url && (
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-brand-blue hover:text-brand-blue/80 text-sm font-medium"
                >
                  {t('entityCheck.report.viewSource', '查看來源')} →
                </a>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-yellow-50 dark:bg-yellow-900/10 border border-yellow-200 dark:border-yellow-800 rounded-2xl p-6">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-yellow-800 dark:text-yellow-200">
              {t('entityCheck.report.disclaimer.title', '重要聲明')}
            </h3>
            <div className="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
              <p>{t('entityCheck.report.disclaimer.content', '本報告僅供參考，所有資料均來自公開來源。實際商業決策請諮詢專業顧問。本報告不構成法律意見或投資建議。')}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}