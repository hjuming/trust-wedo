import React from 'react'
import { useTranslation } from 'react-i18next'
import { Link } from 'react-router-dom'

export const PricingSection = () => {
  const { t } = useTranslation()

  const features = t('pricing.beta.features', { returnObjects: true }) as string[]

  return (
    <section id="pricing" className="bg-brand-navy py-24 text-white">
      <div className="max-w-7xl mx-auto px-6">
        <h2 className="text-5xl md:text-7xl font-black text-center tracking-tight mb-16">
          {t('pricing.title')}
        </h2>
        
        <div className="max-w-4xl mx-auto relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-brand-blue to-brand-cyan rounded-[2rem] blur opacity-20 group-hover:opacity-35 transition duration-700"></div>
          
          <div className="relative bg-brand-navy p-10 md:p-16 rounded-[2rem] border border-white/10 shadow-2xl">
            <h3 className="text-3xl md:text-4xl font-black mb-6">
              {t('pricing.beta.title')}
            </h3>
            <div className="flex flex-wrap items-baseline gap-3 mb-8">
              <span className="text-6xl md:text-8xl font-black text-brand-blue">
                {t('pricing.beta.price')}
              </span>
              <span className="text-2xl md:text-3xl font-black text-brand-light/70">
                {t('pricing.beta.period')}
              </span>
            </div>
            
            <p className="max-w-2xl text-xl md:text-2xl text-brand-light/70 mb-10 leading-relaxed font-bold">
              {t('pricing.beta.description')}
            </p>
            
            <ul className="space-y-6 mb-12">
              {Array.isArray(features) && features.map((feature, i) => (
                <li key={i} className="flex items-center gap-5 text-2xl font-black text-brand-light">
                  <span className="text-brand-success">✓</span>
                  {feature}
                </li>
              ))}
            </ul>
            
            <Link to="/entity-check" className="block w-full py-5 bg-brand-blue text-white rounded-2xl font-black text-xl hover:bg-brand-blue/90 transition-colors shadow-lg shadow-brand-blue/20 text-center">
              {t('pricing.beta.cta')}
            </Link>
          </div>
        </div>
      </div>
    </section>
  )
}
