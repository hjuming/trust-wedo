import React from 'react'
import { useTranslation } from 'react-i18next'

export const ProblemSection = () => {
  const { t } = useTranslation()

  return (
    <section className="py-24 bg-gradient-to-b from-white to-brand-light/50 dark:from-brand-navy dark:to-brand-navy/50">
      <div className="max-w-4xl mx-auto px-6 text-center">
        <h2 className="text-4xl md:text-5xl font-black tracking-tight text-brand-navy dark:text-brand-light mb-6">
          {t('problem.title')}
        </h2>
        <p className="text-lg md:text-xl text-brand-slate dark:text-brand-light/70 leading-relaxed max-w-2xl mx-auto">
          {t('problem.description')}
        </p>
      </div>
    </section>
  )
}
