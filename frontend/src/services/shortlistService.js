import api from './api'

export const getShortlists = () => api.get('/shortlists')
export const addShortlist = (schoolId) =>
  api.post('/shortlists', { school_id: schoolId })
export const removeShortlist = (schoolId) =>
  api.delete(`/shortlists/${schoolId}`)
