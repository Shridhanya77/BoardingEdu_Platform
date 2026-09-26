import api from './api'

export const getSchools = (params = {}) => api.get('/schools', { params })
export const getSchool = (id) => api.get(`/schools/${id}`)
export const getSchoolFilters = () => api.get('/schools/filters')
export const getSchoolFees = (id) => api.get(`/schools/${id}/fees`)
export const createSchool = (payload) => api.post('/schools', payload)
export const updateSchool = (id, payload) => api.put(`/schools/${id}`, payload)
export const deleteSchool = (id) => api.delete(`/schools/${id}`)
