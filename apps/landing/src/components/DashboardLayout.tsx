import React from 'react'
import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useDarkMode } from '../hooks/useDarkMode'
import { useLanguage } from '../hooks/useLanguage'

export default function DashboardLayout() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const location = useLocation()
  const { isDark, toggleDarkMode } = useDarkMode()
  const { currentLang, toggleLanguage } = useLanguage()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  const navItems = [
    { name: t('dashboard.nav.overview'), path: '/dashboard', icon: '📊' },
    { name: t('dashboard.nav.scans'), path: '/dashboard/scans', icon: '🔍' },
    { name: t('dashboard.nav.reports'), path: '/dashboard/reports', icon: '📄' },
    { name: t('dashboard.nav.settings'), path: '/dashboard/settings', icon: '⚙️' },
  ]

  return (
    <div className="min-h-screen bg-brand-light dark:bg-brand-navy flex">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-white dark:bg-brand-navy/50 border-r border-brand-navy/5 dark:border-brand-light/5 p-6 flex flex-col z-50">
        <Link to="/" className="flex items-center gap-2 mb-10 px-4">
          <img src="/logo-icon.svg" alt="Logo" className="w-8 h-8" />
          <span className="text-xl font-black tracking-tighter text-brand-navy dark:text-brand-light">
            Trust <span className="text-brand-blue">WEDO</span>
          </span>
        </Link>

        <nav className="flex-1 space-y-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-medium ${
                  isActive 
                    ? 'bg-brand-blue text-white shadow-lg shadow-brand-blue/20' 
                    : 'text-brand-slate dark:text-brand-light/60 hover:bg-brand-navy/5 dark:hover:bg-brand-light/5'
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                {item.name}
              </Link>
            )
          })}
        </nav>

        <div className="pt-6 border-t border-brand-navy/5 dark:border-brand-light/5 space-y-2">
          <button
            onClick={toggleDarkMode}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-brand-slate dark:text-brand-light/60 hover:bg-brand-navy/5 dark:hover:bg-brand-light/5 transition-all font-medium"
          >
            <span>{isDark ? '☀️' : '🌙'}</span>
            {isDark ? 'Light Mode' : 'Dark Mode'}
          </button>
          <button
            onClick={toggleLanguage}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-brand-slate dark:text-brand-light/60 hover:bg-brand-navy/5 dark:hover:bg-brand-light/5 transition-all font-medium"
          >
            <span>🌐</span>
            {currentLang === 'zh-TW' ? 'English' : '繁體中文'}
          </button>
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-red-500 hover:bg-red-50 dark:hover:bg-red-900/10 transition-all font-medium mt-4"
          >
            <span>🚪</span>
            {t('dashboard.nav.logout')}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-64 min-h-screen p-8 lg:p-12">
        <div className="max-w-6xl mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
