import axios from 'axios'

const normalizeBaseUrl = (url) => {
  if (!url) return url
  return url
    .trim()
    .replace(/\/+$/, '')
    .replace(/\.+$/, '')
}

const rawBaseUrl = normalizeBaseUrl(import.meta.env.VITE_API_BASE_URL)
const fallbackLocal = 'http://127.0.0.1:5000/api'
const fallbackProduction = 'https://boardingedu-platform-1.onrender.com/api'
const isDevEnv = import.meta.env.DEV
const defaultFallback = isDevEnv ? fallbackLocal : fallbackProduction
const finalBaseUrl = rawBaseUrl || defaultFallback

// eslint-disable-next-line no-console
console.log('[BoardingEdu] API base URL:', finalBaseUrl)

const api = axios.create({
  baseURL: finalBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000,
})

const MAX_RETRIES = 2
const RETRY_DELAY_MS = 1500

const sleep = (ms) => new Promise((res) => setTimeout(res, ms))

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('be_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  if (config.__retryCount == null) {
    config.__retryCount = 0
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config || {}
    const method = (config.method || 'get').toLowerCase()
    const isNetworkError = !error.response
    const isServerHang = error.code === 'ECONNABORTED' || /timeout/i.test(error.message || '')
    const isServerError = error.response && error.response.status >= 500
    const canRetry =
      method === 'get' && (isNetworkError || isServerHang || isServerError)

    if (canRetry && (config.__retryCount || 0) < MAX_RETRIES) {
      config.__retryCount = (config.__retryCount || 0) + 1
      // eslint-disable-next-line no-console
      console.warn(
        `[BoardingEdu] Retrying ${method} ${config.url || ''} (attempt ${config.__retryCount}/${MAX_RETRIES})`,
      )
      await sleep(RETRY_DELAY_MS * config.__retryCount)
      return api.request(config)
    }

    if (error.response?.status === 401) {
      const url = error.config?.url || ''
      if (!url.includes('/auth/login') && !url.includes('/auth/register')) {
        localStorage.removeItem('be_token')
        localStorage.removeItem('be_user')
        if (!window.location.pathname.startsWith('/login')) {
          window.location.assign('/login')
        }
      }
    }

    if (isNetworkError) {
      // eslint-disable-next-line no-console
      console.error('[BoardingEdu] Network error reaching API:', {
        baseURL: finalBaseUrl,
        url: config.url,
        error: error.message,
        code: error.code,
      })
    }

    return Promise.reject(error)
  },
)

export const getApiHealth = () => api.get('/health')

export function getErrorMessage(error, fallback = 'Something went wrong.') {
  const data = error?.response?.data
  if (!data) {
    if (!error?.response) {
      if (!navigator.onLine) {
        return 'No internet connection. Please check your network and try again.'
      }
      const apiBase = finalBaseUrl.replace(/\/api\/?$/, '')
      const isLocal = apiBase.includes('localhost') || apiBase.includes('127.0.0.1')
      const isVercel = typeof window !== 'undefined' && window.location.hostname.includes('vercel.app')
      let hint = ''
      if (isLocal) {
        hint = `\nRun: cd backend ; python app.py`
      } else if (isVercel) {
        hint = `\nVercel hint: Check that VITE_API_BASE_URL is set in Vercel Project → Settings → Environment Variables, then Redeploy.`
      }
      return (
        `Network error. Check that the API server is running at \`${apiBase}\`.` +
        hint
      )
    }
    return fallback
  }
  if (data.errors && typeof data.errors === 'object') {
    const first = Object.values(data.errors)[0]
    if (typeof first === 'string') return first
  }
  return data.message || fallback
}

export function isNetworkError(error) {
  return !error?.response && !!error?.message
}

export default api
