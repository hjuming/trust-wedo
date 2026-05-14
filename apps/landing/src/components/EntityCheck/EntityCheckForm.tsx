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
    <div className="w-full">
      <div className="bg-white/95 text-brand-navy rounded-3xl border border-white/40 shadow-2xl p-6 md:p-8">
        <div className="mb-6">
          <span className="text-xs font-bold tracking-[0.2em] uppercase text-brand-blue">
            Entity Verification
          </span>
          <h2 className="mt-3 text-2xl md:text-3xl font-black tracking-tight">
            輸入公司資料，啟動公開資料查核
          </h2>
          <p className="mt-3 text-sm leading-relaxed text-brand-slate">
            系統會先驗證統一編號，再查詢公司登記資料，整理成可引用的初步查核報告。
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="companyName" className="mb-2 block text-sm font-bold text-brand-navy/70">
              {t('entityCheck.form.companyName', '公司名稱')} *
            </label>
            <input
              type="text"
              id="companyName"
              value={formData.companyName}
              onChange={(e) => handleChange('companyName', e.target.value)}
              className="w-full rounded-2xl border border-brand-navy/10 bg-brand-light px-4 py-4 text-base font-semibold text-brand-navy outline-none transition placeholder:text-brand-slate/50 focus:border-brand-blue focus:ring-4 focus:ring-brand-blue/15"
              placeholder={t('entityCheck.form.companyNamePlaceholder', '例如：擎天金屬股份有限公司')}
              required
            />
          </div>

          <div>
            <label htmlFor="taxId" className="mb-2 block text-sm font-bold text-brand-navy/70">
              {t('entityCheck.form.taxId', '統一編號')} *
            </label>
            <input
              type="text"
              id="taxId"
              value={formData.taxId}
              onChange={(e) => handleChange('taxId', e.target.value)}
              className="w-full rounded-2xl border border-brand-navy/10 bg-brand-light px-4 py-4 text-base font-semibold text-brand-navy outline-none transition placeholder:text-brand-slate/50 focus:border-brand-blue focus:ring-4 focus:ring-brand-blue/15"
              placeholder={t('entityCheck.form.taxIdPlaceholder', '8 位數字，例如：04595257')}
              pattern="[0-9]{8}"
              maxLength={8}
              required
            />
            <p className="mt-2 text-sm font-medium text-brand-slate">
              {t('entityCheck.form.taxIdHelp', '輸入 8 位統一編號，將自動驗證格式')}
            </p>
          </div>

          <div>
            <label htmlFor="websiteUrl" className="mb-2 block text-sm font-bold text-brand-navy/70">
              {t('entityCheck.form.websiteUrl', '公司網站')}
            </label>
            <input
              type="url"
              id="websiteUrl"
              value={formData.websiteUrl}
              onChange={(e) => handleChange('websiteUrl', e.target.value)}
              className="w-full rounded-2xl border border-brand-navy/10 bg-brand-light px-4 py-4 text-base font-semibold text-brand-navy outline-none transition placeholder:text-brand-slate/50 focus:border-brand-blue focus:ring-4 focus:ring-brand-blue/15"
              placeholder={t('entityCheck.form.websiteUrlPlaceholder', 'https://example.com')}
            />
            <p className="mt-2 text-sm font-medium text-brand-slate">
              {t('entityCheck.form.websiteUrlHelp', '選填，用於網站信任度分析')}
            </p>
          </div>

          <div className="pt-3">
            <button
              type="submit"
              disabled={loading || !formData.companyName.trim() || !formData.taxId.trim()}
              className="flex w-full items-center justify-center gap-2 rounded-2xl bg-brand-blue px-6 py-4 text-base font-black text-white shadow-lg shadow-brand-blue/20 transition hover:bg-brand-blue/90 disabled:cursor-not-allowed disabled:bg-brand-slate/40"
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

        <div className="mt-6 grid grid-cols-3 gap-3 text-center">
          {['統編驗證', '公司登記', '風險摘要'].map((item) => (
            <div key={item} className="rounded-2xl bg-brand-light px-3 py-3">
              <div className="text-xs font-black text-brand-blue">Ready</div>
              <div className="mt-1 text-xs font-bold text-brand-slate">{item}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
