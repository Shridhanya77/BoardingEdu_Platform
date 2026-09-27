import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
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
      const base = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api').replace('/api', '')
      return (
        `Network error. Check that the API server is running at ${base}.\n` +
        'Run: cd backend ; python app.py'
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
