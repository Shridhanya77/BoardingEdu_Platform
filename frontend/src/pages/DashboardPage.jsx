import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import LoadingSpinner from '../components/LoadingSpinner'
import { useAuth } from '../context/AuthContext'
import { getShortlists } from '../services/shortlistService'
import { getEnquiries } from '../services/enquiryService'
import { getErrorMessage } from '../services/api'

export default function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState({ shortlists: 0, enquiries: 0, pending: 0 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let ignore = false
    Promise.all([getShortlists(), getEnquiries()])
      .then(([sRes, eRes]) => {
        if (ignore) return
        const shortlists = sRes.data?.data?.items || []
        const enquiries = eRes.data?.data?.items || []
        setStats({
          shortlists: shortlists.length,
          enquiries: enquiries.length,
          pending: enquiries.filter((e) => e.status === 'Pending').length,
        })
      })
      .catch((err) => {
        if (!ignore) setError(getErrorMessage(err))
      })
      .finally(() => {
        if (!ignore) setLoading(false)
      })
    return () => {
      ignore = true
    }
  }, [])

  return (
    <div className="container py-4">
      <h1 className="h3 mb-1">Welcome, {user?.name}</h1>
      <p className="text-muted mb-4">Your BoardingEdu parent dashboard.</p>
      {error && <div className="alert alert-danger">{error}</div>}
      {loading ? (
        <LoadingSpinner />
      ) : (
        <div className="row g-3 mb-4">
          {[
            { label: 'Shortlisted schools', value: stats.shortlists, to: '/shortlisted' },
            { label: 'Enquiries', value: stats.enquiries, to: '/enquiries' },
            { label: 'Pending enquiries', value: stats.pending, to: '/enquiries' },
          ].map((card) => (
            <div className="col-md-4" key={card.label}>
              <Link to={card.to} className="be-stat-card text-decoration-none">
                <div className="display-6 fw-bold">{card.value}</div>
                <div className="text-muted">{card.label}</div>
              </Link>
            </div>
          ))}
        </div>
      )}
      <div className="d-flex flex-wrap gap-2">
        <Link to="/schools" className="btn btn-primary">
          Discover schools
        </Link>
        <Link to="/compare" className="btn btn-outline-primary">
          Compare
        </Link>
        <Link to="/profile" className="btn btn-outline-secondary">
          Profile
        </Link>
      </div>
    </div>
  )
}
