import api from './api'

export const getAdminDashboard = () => api.get('/admin/dashboard')
export const getAdminUsers = () => api.get('/admin/users')
export const getAdminEnquiries = (params = {}) =>
  api.get('/admin/enquiries', { params })
export const updateEnquiryStatus = (id, status) =>
  api.put(`/admin/enquiries/${id}/status`, { status })
