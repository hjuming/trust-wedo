import { useState } from 'react'
import { useTranslation } from 'react-i18next'

interface EntityCheckFormProps {
  onSubmit: (data: {
    companyName: string
    taxId: string
    websiteUrl: string
  }) => void
  loading: boolean
}

export default function EntityCheckForm({ onSubmit, loading }: EntityCheckFormProps) {
  const { t } = useTranslation()
  const [formData, setFormData] = useState({
    companyName: '',
    taxId: '',
    websiteUrl: '',
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.companyName.trim() || !formData.taxId.trim()) {
      return
    }
    onSubmit(formData)
  }

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white dark:bg-brand-navy rounded-2xl shadow-xl p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Company Name */}
          <div>
            <label htmlFor="companyName" className="block text-sm font-medium text-brand-navy dark:text-brand-light mb-2">
              {t('entityCheck.form.companyName', '公司名稱')} *
            </label>
            <input
              type="text"
              id="companyName"
              value={formData.companyName}
              onChange={(e) => handleChange('companyName', e.target.value)}
              className="w-full px-4 py-3 border border-brand-slate/20 dark:border-brand-light/20 rounded-lg focus:ring-2 focus:ring-brand-blue focus:border-transparent bg-white dark:bg-brand-navy text-brand-navy dark:text-brand-light placeholder-brand-slate/60"
              placeholder={t('entityCheck.form.companyNamePlaceholder', '例如：擎天金屬股份有限公司')}
              required
            />
          </div>

          {/* Tax ID */}
          <div>
            <label htmlFor="taxId" className="block text-sm font-medium text-brand-navy dark:text-brand-light mb-2">
              {t('entityCheck.form.taxId', '統一編號')} *
            </label>
            <input
              type="text"
              id="taxId"
              value={formData.taxId}
              onChange={(e) => handleChange('taxId', e.target.value)}
              className="w-full px-4 py-3 border border-brand-slate/20 dark:border-brand-light/20 rounded-lg focus:ring-2 focus:ring-brand-blue focus:border-transparent bg-white dark:bg-brand-navy text-brand-navy dark:text-brand-light placeholder-brand-slate/60"
              placeholder={t('entityCheck.form.taxIdPlaceholder', '8 位數字，例如：04595257')}
              pattern="[0-9]{8}"
              maxLength={8}
              required
            />
            <p className="mt-1 text-sm text-brand-slate dark:text-brand-light/60">
              {t('entityCheck.form.taxIdHelp', '輸入 8 位統一編號，將自動驗證格式')}
            </p>
          </div>

          {/* Website URL */}
          <div>
            <label htmlFor="websiteUrl" className="block text-sm font-medium text-brand-navy dark:text-brand-light mb-2">
              {t('entityCheck.form.websiteUrl', '公司網站')}
            </label>
            <input
              type="url"
              id="websiteUrl"
              value={formData.websiteUrl}
              onChange={(e) => handleChange('websiteUrl', e.target.value)}
              className="w-full px-4 py-3 border border-brand-slate/20 dark:border-brand-light/20 rounded-lg focus:ring-2 focus:ring-brand-blue focus:border-transparent bg-white dark:bg-brand-navy text-brand-navy dark:text-brand-light placeholder-brand-slate/60"
              placeholder={t('entityCheck.form.websiteUrlPlaceholder', 'https://example.com')}
            />
            <p className="mt-1 text-sm text-brand-slate dark:text-brand-light/60">
              {t('entityCheck.form.websiteUrlHelp', '選填，用於網站信任度分析')}
            </p>
          </div>

          {/* Submit Button */}
          <div className="pt-4">
            <button
              type="submit"
              disabled={loading || !formData.companyName.trim() || !formData.taxId.trim()}
              className="w-full bg-brand-blue hover:bg-brand-blue/90 disabled:bg-brand-slate/50 disabled:cursor-not-allowed text-white font-semibold py-4 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  <span>{t('entityCheck.form.checking', '查核中...')}</span>
                </>
              ) : (
                <span>{t('entityCheck.form.submit', '開始查核')}</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}