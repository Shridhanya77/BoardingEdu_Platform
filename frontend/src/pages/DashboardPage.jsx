import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import LoadingSpinner from '../components/LoadingSpinner'
import { useAuth } from '../context/AuthContext'
import { getShortlists } from '../services/shortlistService'
import { getEnquiries } from '../services/enquiryService'
import { getErrorMessage } from '../services/api'

const schoolImage = (school) => {
  if (!school) return 'https://picsum.photos/seed/be-default/320/200'
  if (school.primary_image) return school.primary_image
  const first = school.images?.[0]?.image_url
  if (first) return first
  return `https://picsum.photos/seed/be-${school.id}/320/200`
}

export default function DashboardPage() {
  const { user } = useAuth()
  const [stats, setStats] = useState({ shortlists: 0, enquiries: 0, pending: 0 })
  const [shortlists, setShortlists] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let ignore = false
    Promise.all([getShortlists(), getEnquiries()])
      .then(([sRes, eRes]) => {
        if (ignore) return
        const shortlistItems = sRes.data?.data?.items || []
        const enquiries = eRes.data?.data?.items || []
        setShortlists(shortlistItems)
        setStats({
          shortlists: shortlistItems.length,
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

  const shortlistedSchools = shortlists.map((r) => r.school).filter(Boolean)

  return (
    <div className="container py-4">
      <h1 className="h3 mb-1">Welcome, {user?.name}</h1>
      <p className="text-muted mb-4">Your BoardingEdu parent dashboard.</p>
      {error && <div className="alert alert-danger">{error}</div>}
      {loading ? (
        <LoadingSpinner />
      ) : (
        <>
          <div className="row g-3 mb-5">
            {[
              { label: 'Shortlisted schools', value: stats.shortlists, to: '/shortlisted', icon: 'bi-heart-fill', color: 'primary' },
              { label: 'Enquiries', value: stats.enquiries, to: '/enquiries', icon: 'bi-question-circle-fill', color: 'teal' },
              { label: 'Pending enquiries', value: stats.pending, to: '/enquiries', icon: 'bi-clock-history', color: 'amber' },
            ].map((card) => (
              <div className="col-md-4" key={card.label}>
                <Link to={card.to} className="be-stat-card text-decoration-none">
                  <div className="d-flex align-items-center gap-3 mb-2">
                    <div className={`be-stat-icon bg-${card.color}-subtle text-${card.color}`}>
                      <i className={`bi ${card.icon}`} />
                    </div>
                    <div className="display-6 fw-bold">{card.value}</div>
                  </div>
                  <div className="text-muted">{card.label}</div>
                </Link>
              </div>
            ))}
          </div>

          <section className="mb-5">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h2 className="h4 mb-0">
                <i className="bi bi-images me-2 text-primary" />
                Shortlisted schools
              </h2>
              <Link to="/shortlisted" className="btn btn-sm btn-outline-primary">
                View all
              </Link>
            </div>
            {shortlistedSchools.length === 0 ? (
              <div className="card border-0 bg-light text-center py-5">
                <i className="bi bi-heart display-5 text-muted mb-2" />
                <p className="text-muted mb-3">No shortlisted schools yet.</p>
                <Link to="/schools" className="btn btn-primary">
                  Browse schools
                </Link>
              </div>
            ) : (
              <div className="row g-3">
                {shortlistedSchools.slice(0, 6).map((school) => (
                  <div key={school.id} className="col-6 col-md-4 col-lg-3">
                    <Link
                      to={`/schools/${school.id}`}
                      className="dashboard-school-card text-decoration-none d-block"
                    >
                      <div className="dashboard-school-image">
                        <img
                          src={schoolImage(school)}
                          alt={school.name}
                          loading="lazy"
                        />
                        <span className="badge text-bg-danger position-absolute top-2 start-2 m-2">
                          <i className="bi bi-heart-fill" />
                        </span>
                      </div>
                      <div className="p-2">
                        <h3 className="h6 fw-semibold mb-1 text-dark text-truncate">{school.name}</h3>
                        <p className="small text-muted mb-0 text-truncate">
                          <i className="bi bi-geo-alt me-1" />
                          {school.city}
                        </p>
                      </div>
                    </Link>
                  </div>
                ))}
              </div>
            )}
          </section>

          <div className="d-flex flex-wrap gap-2">
            <Link to="/schools" className="btn btn-primary">
              <i className="bi bi-search me-1" /> Discover schools
            </Link>
            <Link to="/compare" className="btn btn-outline-primary">
              <i className="bi bi-layout-split me-1" /> Compare
            </Link>
            <Link to="/profile" className="btn btn-outline-secondary">
              <i className="bi bi-person me-1" /> Profile
            </Link>
          </div>
        </>
      )}
    </div>
  )
}
