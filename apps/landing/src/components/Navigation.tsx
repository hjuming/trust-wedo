import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useDarkMode } from '../hooks/useDarkMode'
import { useLanguage } from '../hooks/useLanguage'

export const Navigation = () => {
  const { t } = useTranslation()
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const { isDark, toggleDarkMode } = useDarkMode()
  const { currentLang, toggleLanguage } = useLanguage()

  const navLinks = [
    { name: t('nav.docs'), href: '/docs' },
    { name: t('nav.pricing'), href: '/pricing' },
    { name: t('nav.playground'), href: '/playground' },
  ]

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <nav
      className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled
        ? 'py-3 bg-brand-light/80 dark:bg-brand-navy/80 backdrop-blur-md shadow-sm'
        : 'py-6 bg-transparent'
        }`}
    >
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <img src="/logo-icon.svg" alt="Logo" className="w-8 h-8 group-hover:rotate-12 transition-transform" />
          <span className="text-xl font-black tracking-tighter text-brand-navy dark:text-brand-light">
            Trust <span className="text-brand-blue">WEDO</span>
          </span>
        </Link>

        {/* Desktop Links */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.href}
              className="text-sm font-medium text-brand-slate hover:text-brand-blue dark:text-brand-light/80 dark:hover:text-brand-cyan transition-colors"
            >
              {link.name}
            </Link>
          ))}
          <div className="h-4 w-[1px] bg-brand-slate/20 mx-2" />
          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-full hover:bg-brand-slate/10 dark:hover:bg-brand-light/10 transition-colors"
            aria-label="Toggle dark mode"
          >
            {isDark ? '🌞' : '🌙'}
          </button>
          <button
            onClick={toggleLanguage}
            className="px-3 py-2 rounded-full hover:bg-brand-slate/10 dark:hover:bg-brand-light/10 transition-colors flex items-center gap-1"
            aria-label="Toggle language"
          >
            <span>🌐</span>
            <span className="text-sm font-medium text-brand-navy dark:text-brand-light">{currentLang}</span>
          </button>
          <a
            href="https://github.com/Trust-WEDO"
            className="bg-brand-navy dark:bg-brand-light text-white dark:text-brand-navy px-5 py-2 rounded-full text-sm font-bold hover:scale-105 transition-transform"
          >
            {t('nav.getStarted')}
          </a>
        </div>

        {/* Mobile Toggle */}
        <div className="md:hidden flex items-center gap-4">
          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-full"
            aria-label="Toggle dark mode"
          >
            {isDark ? '🌞' : '🌙'}
          </button>
          <button
            onClick={toggleLanguage}
            className="px-2 py-1 rounded-full flex items-center gap-1"
            aria-label="Toggle language"
          >
            <span>🌐</span>
            <span className="text-sm font-medium text-brand-navy dark:text-brand-light">{currentLang}</span>
          </button>
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="text-brand-navy dark:text-brand-light focus:outline-none"
            aria-label="Toggle menu"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {isOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu Overlay */}
      <div
        className={`fixed inset-0 top-[60px] bg-brand-light dark:bg-brand-navy z-40 md:hidden transition-transform duration-300 ${isOpen ? 'translate-x-0' : 'translate-x-full'
          }`}
      >
        <div className="flex flex-col items-center justify-center h-full gap-8 p-6">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.href}
              onClick={() => setIsOpen(false)}
              className="text-2xl font-bold text-brand-navy dark:text-brand-light"
            >
              {link.name}
            </Link>
          ))}
          <a
            href="https://github.com/Trust-WEDO"
            className="w-full text-center bg-brand-blue text-white py-4 rounded-xl text-xl font-bold"
          >
            {t('nav.getStarted')}
          </a>
        </div>
      </div>
    </nav>
  )
}
