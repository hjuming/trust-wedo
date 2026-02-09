import React, { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'

interface Scan {
  id: string
  url: string
  status: string
  created_at: string
}

export default function Scans() {
  const { t } = useTranslation()
  const [scans, setScans] = useState<Scan[]>([])
  const [loading, setLoading] = useState(true)
  const [newScanUrl, setNewScanUrl] = useState('')
  const [creating, setCreating] = useState(false)

  useEffect(() => {
    fetchScans()
  }, [])

  const fetchScans = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/scans', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setScans(data)
      }
    } catch (error) {
      console.error('Failed to fetch scans:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateScan = async (e: React.FormEvent) => {
    e.preventDefault()
    setCreating(true)

    try {
      const token = localStorage.getItem('token')
      const response = await fetch('http://localhost:8000/api/scans', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ url: newScanUrl })
      })

      if (response.ok) {
        setNewScanUrl('')
        fetchScans()
      }
    } catch (error) {
      console.error('Failed to create scan:', error)
    } finally {
      setCreating(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-50 dark:bg-green-900/20'
      case 'processing': return 'text-blue-600 bg-blue-50 dark:bg-blue-900/20'
      case 'failed': return 'text-red-600 bg-red-50 dark:bg-red-900/20'
      case 'pending': return 'text-amber-600 bg-amber-50 dark:bg-amber-900/20'
      default: return 'text-gray-600 bg-gray-50 dark:bg-gray-900/20'
    }
  }

  return (
    <div>
      <header className="mb-10">
        <h1 className="text-3xl font-bold text-brand-navy dark:text-brand-light">
          {t('dashboard.nav.scans')}
        </h1>
        <p className="text-brand-slate dark:text-brand-light/60 mt-2">
          Manage and monitor your repository scanning tasks.
        </p>
      </header>

      {/* Create Scan Form */}
      <section className="mb-10 p-8 bg-white dark:bg-brand-navy/50 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 shadow-sm">
        <h2 className="text-lg font-bold text-brand-navy dark:text-brand-light mb-4">
          {t('scans.newScan')}
        </h2>
        <form onSubmit={handleCreateScan} className="flex flex-col md:flex-row gap-4">
          <input
            type="url"
            value={newScanUrl}
            onChange={(e) => setNewScanUrl(e.target.value)}
            placeholder="https://example.com"
            required
            className="flex-1 px-4 py-3 rounded-xl border border-brand-navy/10 dark:border-brand-light/10 bg-white dark:bg-brand-navy focus:outline-none focus:ring-2 focus:ring-brand-blue text-brand-navy dark:text-brand-light"
          />
          <button
            type="submit"
            disabled={creating}
            className="px-8 py-3 bg-brand-blue text-white rounded-xl font-bold hover:bg-brand-blue/90 transition-all disabled:opacity-50 shadow-lg shadow-brand-blue/20"
          >
            {creating ? t('scans.creating') : t('scans.create')}
          </button>
        </form>
      </section>

      {/* Scans List */}
      <section>
        <h2 className="text-lg font-bold text-brand-navy dark:text-brand-light mb-4 px-2">
          Recent Scans
        </h2>
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 bg-white/50 dark:bg-brand-navy/30 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 border-dashed">
            <div className="w-10 h-10 border-4 border-brand-blue/30 border-t-brand-blue rounded-full animate-spin mb-4" />
            <p className="text-brand-slate dark:text-brand-light/60 font-medium">
              {t('scans.loading')}
            </p>
          </div>
        ) : scans.length === 0 ? (
          <div className="text-center py-20 bg-white/50 dark:bg-brand-navy/30 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 border-dashed">
            <p className="text-brand-slate dark:text-brand-light/60 font-medium">
              {t('scans.empty')}
            </p>
          </div>
        ) : (
          <div className="grid gap-4">
            {scans.map((scan) => (
              <div
                key={scan.id}
                className="p-6 bg-white dark:bg-brand-navy/50 rounded-2xl border border-brand-navy/5 dark:border-brand-light/5 hover:border-brand-blue/20 transition-all group"
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="flex-1">
                    <div className="text-lg font-bold text-brand-navy dark:text-brand-light mb-1 group-hover:text-brand-blue transition-colors">
                      {scan.url}
                    </div>
                    <div className="text-sm text-brand-slate dark:text-brand-light/40 flex items-center gap-2">
                      <span>ID: {scan.id.split('-')[0]}...</span>
                      <span>•</span>
                      <span>{new Date(scan.created_at).toLocaleString()}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`px-4 py-1.5 rounded-full text-sm font-bold tracking-wide uppercase ${getStatusColor(scan.status)}`}>
                      {t(`scans.status.${scan.status}`)}
                    </span>
                    <button className="p-2 text-brand-slate hover:text-brand-blue transition-colors">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
