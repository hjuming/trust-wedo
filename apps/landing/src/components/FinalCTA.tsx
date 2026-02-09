import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

export const FinalCTA = () => {
  const { t } = useTranslation()

  return (
    <section className="py-24 overflow-hidden relative">
      <div className="absolute inset-0 bg-gradient-to-r from-brand-blue to-brand-cyan -z-10" />
      
      <div className="max-w-4xl mx-auto px-6 text-center text-white">
        <h2 className="text-4xl md:text-6xl font-black tracking-tight mb-6 leading-tight">
          {t('finalCta.title')}
        </h2>
        <p className="text-xl md:text-2xl text-white/80 mb-12 font-medium">
          {t('finalCta.subtitle')}
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link to="/signup" className="w-full sm:w-auto px-10 py-5 bg-white text-brand-blue rounded-2xl font-black text-xl hover:scale-105 transition-transform shadow-xl inline-block text-center">
            {t('finalCta.primaryCta')}
          </Link>
          <button className="w-full sm:w-auto px-10 py-5 bg-transparent text-white border-2 border-white/30 rounded-2xl font-black text-xl hover:bg-white/10 transition-colors">
            {t('finalCta.secondaryCta')}
          </button>
        </div>
      </div>
      
      {/* Decorative shapes */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2 blur-3xl" />
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-brand-navy/20 rounded-full translate-y-1/2 -translate-x-1/2 blur-3xl" />
    </section>
  )
}
