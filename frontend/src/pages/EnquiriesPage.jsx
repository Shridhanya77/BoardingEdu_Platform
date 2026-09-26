import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import LoadingSpinner from '../components/LoadingSpinner'
import EmptyState from '../components/EmptyState'
import AlertMessage from '../components/AlertMessage'
import { getEnquiries } from '../services/enquiryService'
import { getErrorMessage } from '../services/api'

const STATUS_CLASS = {
  Pending: 'text-bg-warning',
  Contacted: 'text-bg-info',
  'In Review': 'text-bg-primary',
  Closed: 'text-bg-secondary',
}

export default function EnquiriesPage() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getEnquiries()
      .then((res) => setItems(res.data?.data?.items || []))
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="container py-4">
      <h1 className="h3 mb-1">Admission enquiries</h1>
      <p className="text-muted mb-4">Track the status of enquiries you submitted.</p>
      <AlertMessage message={error} onClose={() => setError('')} />
      {loading && <LoadingSpinner />}
      {!loading && items.length === 0 && (
        <EmptyState
          title="No enquiries yet"
          message="Open a school profile and submit an admission enquiry."
          action={
            <Link to="/schools" className="btn btn-primary btn-sm">
              Find a school
            </Link>
          }
        />
      )}
      {!loading && items.length > 0 && (
        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead className="table-light">
              <tr>
                <th>School</th>
                <th>Student</th>
                <th>Class</th>
                <th>Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td>
                    {item.school ? (
                      <Link to={`/schools/${item.school.id}`}>{item.school.name}</Link>
                    ) : (
                      '—'
                    )}
                  </td>
                  <td>{item.student_name}</td>
                  <td>{item.class_name || '—'}</td>
                  <td>{item.created_at ? new Date(item.created_at).toLocaleDateString() : '—'}</td>
                  <td>
                    <span className={`badge ${STATUS_CLASS[item.status] || 'text-bg-light'}`}>
                      {item.status}
                    </span>
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
