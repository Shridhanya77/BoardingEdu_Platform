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

const api = axios.create({
  baseURL: finalBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 20000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('be_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
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
