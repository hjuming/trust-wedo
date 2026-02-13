import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { supabase } from '../lib/supabase'

export default function Login() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rememberMe, setRememberMe] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      // Supabase 會根據初始化時的 storage 設置自動處理 session 持久化
      // 這裡我們只需要正常登入即可
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      })

      if (error) {
        throw error
      }

      // 如果用戶選擇「保持登入」,我們可以在本地存儲一個標記
      // Supabase 默認會將 session 存儲在 localStorage 中
      if (rememberMe) {
        localStorage.setItem('trust-wedo-remember-me', 'true')
      } else {
        localStorage.removeItem('trust-wedo-remember-me')
      }

      navigate('/dashboard')
    } catch (err: any) {
      setError(err.message || 'Invalid email or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-brand-light dark:bg-brand-navy flex flex-col items-center justify-center px-6">
      <Link to="/" className="mb-8 flex items-center gap-2 group">
        <img src="/logo-icon.svg" alt="Logo" className="w-8 h-8 group-hover:rotate-12 transition-transform" />
        <span className="text-xl font-black tracking-tighter text-brand-navy dark:text-brand-light">
          Trust <span className="text-brand-blue">WEDO</span>
        </span>
      </Link>

      <div className="max-w-md w-full bg-white dark:bg-brand-navy/50 p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-xl">
        <h1 className="text-3xl font-bold text-brand-navy dark:text-brand-light mb-8 text-center">
          {t('auth.login.title')}
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-brand-navy dark:text-brand-light mb-2">
              {t('auth.login.email')}
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="name@company.com"
              className="w-full px-4 py-3 rounded-xl border border-brand-navy/10 dark:border-brand-light/10 bg-white dark:bg-brand-navy focus:outline-none focus:ring-2 focus:ring-brand-blue text-brand-navy dark:text-brand-light"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-brand-navy dark:text-brand-light mb-2">
              {t('auth.login.password')}
            </label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="••••••••"
                className="w-full px-4 py-3 pr-12 rounded-xl border border-brand-navy/10 dark:border-brand-light/10 bg-white dark:bg-brand-navy focus:outline-none focus:ring-2 focus:ring-brand-blue text-brand-navy dark:text-brand-light"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-brand-slate dark:text-brand-light/60 hover:text-brand-navy dark:hover:text-brand-light transition-colors p-1"
                aria-label={showPassword ? "隱藏密碼" : "顯示密碼"}
              >
                {showPassword ? (
                  // 眼睛斜線圖示 (隱藏)
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                ) : (
                  // 眼睛圖示 (顯示)
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          {/* 保持登入狀態 */}
          <div className="flex items-center">
            <input
              id="remember-me"
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="w-4 h-4 text-brand-blue bg-white dark:bg-brand-navy border-brand-navy/20 dark:border-brand-light/20 rounded focus:ring-2 focus:ring-brand-blue cursor-pointer"
            />
            <label
              htmlFor="remember-me"
              className="ml-2 text-sm font-medium text-brand-navy dark:text-brand-light cursor-pointer select-none"
            >
              保持登入狀態
            </label>
          </div>

          {error && (
            <div className="p-3 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm text-center font-medium">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 bg-brand-blue text-white rounded-xl font-bold hover:bg-brand-blue/90 transition-all shadow-lg shadow-brand-blue/20 disabled:opacity-50 disabled:cursor-not-allowed active:scale-[0.98]"
          >
            {loading ? t('auth.login.loading') : t('auth.login.submit')}
          </button>
        </form>

        <p className="mt-8 text-center text-sm text-brand-slate dark:text-brand-light/60 font-medium">
          {t('auth.login.noAccount')}{' '}
          <Link to="/signup" className="text-brand-blue hover:text-brand-cyan transition-colors font-bold">
            {t('auth.login.signupLink')}
          </Link>
        </p>
      </div>
    </div>
  )
}
