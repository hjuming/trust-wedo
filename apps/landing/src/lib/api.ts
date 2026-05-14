export function getApiBaseUrl() {
  const configuredUrl = import.meta.env.VITE_API_URL

  if (configuredUrl) {
    return configuredUrl.replace(/\/$/, '')
  }

  if (import.meta.env.DEV) {
    return 'http://localhost:8000'
  }

  return ''
}
