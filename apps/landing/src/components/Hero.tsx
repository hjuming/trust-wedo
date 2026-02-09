import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

export const Hero = () => {
  const { t } = useTranslation()

  return (
    <section className="relative min-h-[90vh] flex items-center justify-center px-6 py-20 overflow-hidden">
      {/* Animated Background Decor */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10">
        <div className="absolute top-[-10%] left-[-20%] w-[60%] h-[60%] bg-brand-blue/10 rounded-full blur-[140px] animate-pulse" />
        <div className="absolute bottom-[0%] right-[-10%] w-[40%] h-[40%] bg-brand-cyan/10 rounded-full blur-[100px] animate-pulse delay-700" />
      </div>

      <div className="max-w-4xl mx-auto text-center">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-blue/10 border border-brand-blue/20 text-brand-blue text-sm font-bold mb-10 animate-fade-in shadow-sm">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-blue opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-blue"></span>
          </span>
          Trust WEDO Beta 1.0
        </div>

        <h1 className="text-5xl md:text-8xl font-black tracking-tight text-brand-navy dark:text-brand-light mb-8 leading-[1.05]">
          {t('hero.title')}
        </h1>
        
        <p className="max-w-2xl mx-auto text-xl md:text-2xl text-brand-navy/80 dark:text-brand-light/90 mb-6 font-semibold whitespace-pre-line leading-relaxed">
          {t('hero.subtitle')}
        </p>
        
        <p className="max-w-xl mx-auto text-lg text-brand-slate dark:text-brand-light/60 mb-14 whitespace-pre-line leading-relaxed">
          {t('hero.description')}
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
          <Link
            to="/signup"
            className="w-full sm:w-auto px-12 py-5 bg-brand-blue text-white rounded-2xl font-black text-xl hover:bg-brand-blue/90 hover:scale-105 transition-all shadow-2xl shadow-brand-blue/30 text-center active:scale-95"
          >
            {t('hero.cta')}
          </Link>
          <button className="w-full sm:w-auto px-12 py-5 bg-white/50 dark:bg-brand-light/5 text-brand-navy dark:text-brand-light rounded-2xl font-bold text-lg hover:bg-white/80 dark:hover:bg-brand-light/10 transition-all border border-brand-navy/10 dark:border-brand-light/10 backdrop-blur-sm">
            瞭解更多
          </button>
        </div>
      </div>
    </section>
  )
}
