import React from 'react'
import { useTranslation } from 'react-i18next'

export const PricingSection = () => {
  const { t } = useTranslation()

  // We cast as any because i18next type support for arrays in JSON can be tricky depending on config
  const features = t('pricing.beta.features', { returnObjects: true }) as string[]

  return (
    <section className="py-24 bg-brand-light dark:bg-brand-navy">
      <div className="max-w-7xl mx-auto px-6">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-brand-navy dark:text-brand-light mb-16">
          {t('pricing.title')}
        </h2>
        
        <div className="max-w-md mx-auto relative group">
          {/* Decorative Glow */}
          <div className="absolute -inset-1 bg-gradient-to-r from-brand-blue to-brand-cyan rounded-[2rem] blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
          
          <div className="relative bg-white dark:bg-brand-navy p-10 rounded-[2rem] border border-brand-navy/5 dark:border-brand-light/5 shadow-2xl">
            <h3 className="text-2xl font-bold text-brand-navy dark:text-brand-light mb-2">
              {t('pricing.beta.title')}
            </h3>
            <div className="flex items-baseline gap-1 mb-6">
              <span className="text-5xl font-black text-brand-blue">
                {t('pricing.beta.price')}
              </span>
              <span className="text-brand-slate dark:text-brand-light/60">/month</span>
            </div>
            
            <p className="text-brand-slate dark:text-brand-light/70 mb-8 text-sm leading-relaxed">
              {t('pricing.beta.description')}
            </p>
            
            <ul className="space-y-4 mb-10">
              {Array.isArray(features) && features.map((feature, i) => (
                <li key={i} className="flex items-center gap-3 text-brand-navy dark:text-brand-light/90">
                  <span className="text-brand-success">✓</span>
                  {feature}
                </li>
              ))}
            </ul>
            
            <button className="w-full py-4 bg-brand-blue text-white rounded-2xl font-bold text-lg hover:bg-brand-blue/90 transition-colors shadow-lg shadow-brand-blue/20">
              {t('pricing.beta.cta')}
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}
