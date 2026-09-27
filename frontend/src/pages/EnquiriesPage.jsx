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

const schoolImage = (school) => {
  if (!school) return 'https://picsum.photos/seed/be-default/160/90'
  if (school.primary_image) return school.primary_image
  const first = school.images?.[0]?.image_url
  if (first) return first
  return `https://picsum.photos/seed/be-${school.id}/160/90`
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
        <div className="card shadow-sm border-0">
          <div className="card-body p-0">
            {items.map((item) => (
              <div key={item.id} className="enquiry-row d-flex align-items-center gap-3 p-3 border-bottom">
                <div className="enquiry-school-image flex-shrink-0">
                  <img
                    src={schoolImage(item.school)}
                    alt={item.school?.name || 'School'}
                    loading="lazy"
                  />
                </div>
                <div className="flex-grow-1 min-w-0">
                  {item.school ? (
                    <Link to={`/schools/${item.school.id}`} className="text-decoration-none">
                      <h3 className="h6 fw-semibold mb-1 text-dark">{item.school.name}</h3>
                    </Link>
                  ) : (
                    <h3 className="h6 fw-semibold mb-1 text-muted">—</h3>
                  )}
                  <p className="small text-muted mb-1">
                    <i className="bi bi-person me-1" /> Student: <strong>{item.student_name}</strong>
                    <span className="mx-2">•</span>
                    Class: {item.class_name || '—'}
                  </p>
                  <p className="small text-muted mb-0">
                    <i className="bi bi-calendar3 me-1" />
                    {item.created_at ? new Date(item.created_at).toLocaleDateString() : '—'}
                  </p>
                </div>
                <div className="flex-shrink-0 d-flex flex-column align-items-end gap-2">
                  <span className={`badge ${STATUS_CLASS[item.status] || 'text-bg-light'}`}>
                    {item.status}
                  </span>
                  {item.school && (
                    <Link to={`/schools/${item.school.id}`} className="btn btn-sm btn-outline-primary">
                      View school
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
