import { useEffect, useState } from 'react'
import LoadingSpinner from '../../components/LoadingSpinner'
import AlertMessage from '../../components/AlertMessage'
import { getAdminEnquiries, updateEnquiryStatus } from '../../services/adminService'
import { getErrorMessage } from '../../services/api'

const STATUSES = ['Pending', 'Contacted', 'In Review', 'Closed']

export default function AdminEnquiriesPage() {
  const [items, setItems] = useState([])
  const [status, setStatus] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [busyId, setBusyId] = useState(null)

  const load = (filter = status) => {
    setLoading(true)
    getAdminEnquiries(filter ? { status: filter } : {})
      .then((res) => setItems(res.data?.data?.items || []))
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const onStatusChange = async (enquiryId, nextStatus) => {
    setBusyId(enquiryId)
    try {
      const res = await updateEnquiryStatus(enquiryId, nextStatus)
      const updated = res.data?.data?.enquiry
      setItems((prev) => prev.map((item) => (item.id === enquiryId ? updated : item)))
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div className="container py-4">
      <h1 className="h3 mb-1">Manage enquiries</h1>
      <p className="text-muted mb-3">Update admission enquiry status.</p>
      <div className="mb-3" style={{ maxWidth: 240 }}>
        <label className="form-label small">Filter by status</label>
        <select
          className="form-select"
          value={status}
          onChange={(e) => {
            setStatus(e.target.value)
            load(e.target.value)
          }}
        >
          <option value="">All</option>
          {STATUSES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </div>
      <AlertMessage message={error} onClose={() => setError('')} />
      {loading && <LoadingSpinner />}
      {!loading && (
        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead className="table-light">
              <tr>
                <th>Parent</th>
                <th>Student</th>
                <th>School</th>
                <th>Class</th>
                <th>Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td>{item.parent_name}</td>
                  <td>{item.student_name}</td>
                  <td>{item.school?.name || '—'}</td>
                  <td>{item.class_name || '—'}</td>
                  <td>
                    {item.created_at ? new Date(item.created_at).toLocaleDateString() : '—'}
                  </td>
                  <td>
                    <select
                      className="form-select form-select-sm"
                      value={item.status}
                      disabled={busyId === item.id}
                      onChange={(e) => onStatusChange(item.id, e.target.value)}
                    >
                      {STATUSES.map((s) => (
                        <option key={s} value={s}>
                          {s}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
