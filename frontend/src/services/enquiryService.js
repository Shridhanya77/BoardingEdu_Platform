import api from './api'

export const submitEnquiry = (payload) => api.post('/enquiries', payload)
export const getEnquiries = (params = {}) => api.get('/enquiries', { params })
export const getEnquiry = (id) => api.get(`/enquiries/${id}`)
