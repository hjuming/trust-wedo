import React from 'react'
import { useTranslation } from 'react-i18next'

export const HowItWorks = () => {
  const { t } = useTranslation()

  const steps = [
    {
      id: 1,
      icon: '📝',
      title: t('howItWorks.step1.title'),
      desc: t('howItWorks.step1.desc'),
    },
    {
      id: 2,
      icon: '⚙️',
      title: t('howItWorks.step2.title'),
      desc: t('howItWorks.step2.desc'),
    },
    {
      id: 3,
      icon: '✅',
      title: t('howItWorks.step3.title'),
      desc: t('howItWorks.step3.desc'),
    },
  ]

  return (
    <section className="py-24 bg-white dark:bg-brand-navy/30">
      <div className="max-w-7xl mx-auto px-6">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-brand-navy dark:text-brand-light mb-16">
          {t('howItWorks.title')}
        </h2>
        <div className="grid md:grid-cols-3 gap-12 relative">
          {/* Connector Line (Desktop) */}
          <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-brand-navy/5 dark:bg-brand-light/5 -translate-y-1/2 -z-10" />
          
          {steps.map((step) => (
            <div key={step.id} className="relative bg-white dark:bg-brand-navy p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-xl shadow-brand-navy/5 dark:shadow-none hover:border-brand-blue/20 transition-all text-center">
              <div className="absolute -top-6 left-1/2 -translate-x-1/2 w-12 h-12 rounded-full bg-brand-blue text-white flex items-center justify-center font-bold text-xl border-4 border-white dark:border-brand-navy">
                {step.id}
              </div>
              <div className="text-5xl mb-6 mt-4">
                {step.icon}
              </div>
              <h3 className="text-xl font-bold text-brand-navy dark:text-brand-light mb-4">
                {step.title}
              </h3>
              <p className="text-brand-slate dark:text-brand-light/60">
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
