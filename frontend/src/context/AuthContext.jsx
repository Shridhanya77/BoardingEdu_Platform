import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import * as authService from '../services/authService'
import { getErrorMessage } from '../services/api'

const AuthContext = createContext(null)

const TOKEN_KEY = 'be_token'
const USER_KEY = 'be_user'

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const raw = localStorage.getItem(USER_KEY)
      return raw ? JSON.parse(raw) : null
    } catch {
      return null
    }
  })
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const [loading, setLoading] = useState(Boolean(localStorage.getItem(TOKEN_KEY)))

  const persist = useCallback((nextUser, nextToken) => {
    setUser(nextUser)
    setToken(nextToken)
    if (nextToken) localStorage.setItem(TOKEN_KEY, nextToken)
    else localStorage.removeItem(TOKEN_KEY)
    if (nextUser) localStorage.setItem(USER_KEY, JSON.stringify(nextUser))
    else localStorage.removeItem(USER_KEY)
  }, [])

  const logout = useCallback(() => {
    persist(null, null)
  }, [persist])

  useEffect(() => {
    if (!token) {
      setLoading(false)
      return
    }
    let ignore = false
    authService
      .getMe()
      .then((res) => {
        if (ignore) return
        const nextUser = res.data?.data?.user
        persist(nextUser, token)
      })
      .catch(() => {
        if (ignore) return
        persist(null, null)
      })
      .finally(() => {
        if (!ignore) setLoading(false)
      })
    return () => {
      ignore = true
    }
  }, [token, persist])

  const login = useCallback(
    async (email, password) => {
      const res = await authService.login({ email, password })
      const payload = res.data?.data
      persist(payload.user, payload.access_token)
      return payload.user
    },
    [persist],
  )

  const register = useCallback(
    async (form) => {
      const res = await authService.register(form)
      const payload = res.data?.data
      persist(payload.user, payload.access_token)
      return payload.user
    },
    [persist],
  )

  const value = useMemo(
    () => ({
      user,
      token,
      loading,
      isAuthenticated: Boolean(user && token),
      isAdmin: user?.role === 'admin',
      isParent: user?.role === 'parent' || user?.role === 'student',
      login,
      register,
      logout,
      getErrorMessage,
    }),
    [user, token, loading, login, register, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
