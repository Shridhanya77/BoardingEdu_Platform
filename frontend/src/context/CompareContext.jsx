import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'

const CompareContext = createContext(null)
const STORAGE_KEY = 'be_compare_ids'
const MAX_COMPARE = 3

export function CompareProvider({ children }) {
  const [ids, setIds] = useState(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      const parsed = raw ? JSON.parse(raw) : []
      return Array.isArray(parsed) ? parsed.map(Number).filter(Boolean) : []
    } catch {
      return []
    }
  })

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(ids))
  }, [ids])

  const addSchool = useCallback((schoolId) => {
    const id = Number(schoolId)
    setIds((prev) => {
      if (prev.includes(id)) return prev
      if (prev.length >= MAX_COMPARE) return prev
      return [...prev, id]
    })
  }, [])

  const removeSchool = useCallback((schoolId) => {
    const id = Number(schoolId)
    setIds((prev) => prev.filter((x) => x !== id))
  }, [])

  const toggleSchool = useCallback((schoolId) => {
    const id = Number(schoolId)
    setIds((prev) => {
      if (prev.includes(id)) return prev.filter((x) => x !== id)
      if (prev.length >= MAX_COMPARE) return prev
      return [...prev, id]
    })
  }, [])

  const clear = useCallback(() => setIds([]), [])

  const value = useMemo(
    () => ({
      ids,
      count: ids.length,
      max: MAX_COMPARE,
      canAdd: ids.length < MAX_COMPARE,
      isSelected: (schoolId) => ids.includes(Number(schoolId)),
      addSchool,
      removeSchool,
      toggleSchool,
      clear,
    }),
    [ids, addSchool, removeSchool, toggleSchool, clear],
  )

  return <CompareContext.Provider value={value}>{children}</CompareContext.Provider>
}

export function useCompare() {
  const ctx = useContext(CompareContext)
  if (!ctx) throw new Error('useCompare must be used within CompareProvider')
  return ctx
}
