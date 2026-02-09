import React from 'react'
import { useTranslation } from 'react-i18next'

export const TrustSignals = () => {
  const { t } = useTranslation()

  const signals = [
    {
      value: t('trustSignals.signal1.value'),
      label: t('trustSignals.signal1.label'),
    },
    {
      value: t('trustSignals.signal2.value'),
      label: t('trustSignals.signal2.label'),
    },
    {
      value: t('trustSignals.signal3.value'),
      label: t('trustSignals.signal3.label'),
    },
  ]

  return (
    <section className="py-12 bg-white dark:bg-brand-navy border-y border-brand-navy/5 dark:border-brand-light/5">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12">
          {signals.map((signal, index) => (
            <div key={index} className="flex flex-col items-center text-center group">
              <span className="text-3xl md:text-4xl font-black text-brand-blue dark:text-brand-cyan mb-2 group-hover:scale-110 transition-transform">
                {signal.value}
              </span>
              <span className="text-brand-slate dark:text-brand-light/60 font-medium text-sm md:text-base tracking-wide uppercase">
                {signal.label}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
