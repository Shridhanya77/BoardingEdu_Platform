import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import LoadingSpinner from '../../components/LoadingSpinner'
import AlertMessage from '../../components/AlertMessage'
import { getAdminDashboard } from '../../services/adminService'
import { getErrorMessage } from '../../services/api'

export default function AdminDashboardPage() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getAdminDashboard()
      .then((res) => setStats(res.data?.data?.stats || null))
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [])

  const cards = [
    { key: 'total_schools', label: 'Total schools', to: '/admin/schools' },
    { key: 'total_users', label: 'Registered users', to: '/admin/users' },
    { key: 'total_shortlists', label: 'Shortlisted schools', to: '/admin' },
    { key: 'total_enquiries', label: 'Admission enquiries', to: '/admin/enquiries' },
    { key: 'pending_enquiries', label: 'Pending enquiries', to: '/admin/enquiries' },
    { key: 'contacted_enquiries', label: 'Contacted enquiries', to: '/admin/enquiries' },
  ]

  return (
    <div className="container py-4">
      <div className="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-4">
        <div>
          <h1 className="h3 mb-1">Admin dashboard</h1>
          <p className="text-muted mb-0">BoardingEdu operations overview</p>
        </div>
        <div className="d-flex flex-wrap gap-2">
          <Link to="/admin/schools" className="btn btn-outline-primary btn-sm">
            Manage schools
          </Link>
          <Link to="/admin/enquiries" className="btn btn-outline-primary btn-sm">
            Enquiries
          </Link>
          <Link to="/admin/users" className="btn btn-outline-secondary btn-sm">
            Users
          </Link>
          <Link to="/admin/schools/new" className="btn btn-primary btn-sm">
            Add school
          </Link>
        </div>
      </div>
      <AlertMessage message={error} onClose={() => setError('')} />
      {loading && <LoadingSpinner />}
      {!loading && stats && (
        <>
          <div className="row g-3 mb-4">
            {cards.map((card) => (
              <div className="col-6 col-md-4" key={card.key}>
                <Link to={card.to} className="be-stat-card text-decoration-none">
                  <div className="h3 mb-1">{stats[card.key] ?? 0}</div>
                  <div className="small text-muted">{card.label}</div>
                </Link>
              </div>
            ))}
          </div>
          <div className="be-chart-bar">
            <h2 className="h6 mb-3">Enquiry status breakdown</h2>
            {[
              ['Pending', stats.pending_enquiries],
              ['Contacted', stats.contacted_enquiries],
              ['In Review', stats.in_review_enquiries],
              ['Closed', stats.closed_enquiries],
            ].map(([label, value]) => {
              const max = Math.max(stats.total_enquiries, 1)
              const pct = Math.round(((value || 0) / max) * 100)
              return (
                <div className="mb-2" key={label}>
                  <div className="d-flex justify-content-between small">
                    <span>{label}</span>
                    <span>{value || 0}</span>
                  </div>
                  <div className="progress" style={{ height: 8 }}>
                    <div
                      className="progress-bar"
                      role="progressbar"
                      style={{ width: `${pct}%` }}
                      aria-valuenow={value || 0}
                      aria-valuemin="0"
                      aria-valuemax={max}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </>
      )}
    </div>
  )
}
