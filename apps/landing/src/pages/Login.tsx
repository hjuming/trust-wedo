import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

export default function Login() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Login failed')
      }

      const data = await response.json()
      localStorage.setItem('token', data.access_token)
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
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
              className="w-full px-4 py-3 rounded-xl border border-brand-navy/10 dark:border-brand-light/10 bg-white dark:bg-brand-navy focus:outline-none focus:ring-2 focus:ring-brand-blue text-brand-navy dark:text-brand-light"
            />
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
