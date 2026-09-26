import { Link } from 'react-router-dom'
import { facilityNames, formatFeeRange } from '../utils/formatters'
import { useCompare } from '../context/CompareContext'
import { useAuth } from '../context/AuthContext'

export default function SchoolCard({
  school,
  shortlisted = false,
  onShortlist,
  shortlistBusy = false,
}) {
  const { isSelected, toggleSchool, canAdd } = useCompare()
  const { isAuthenticated, isParent } = useAuth()
  const selected = isSelected(school.id)
  const image =
    school.primary_image ||
    `https://picsum.photos/seed/be-${school.id}/640/360`

  return (
    <article className="school-card h-100">
      <div className="school-card-image">
        <img src={image} alt="" loading="lazy" />
        {school.hostel_available && (
          <span className="badge text-bg-dark school-card-badge">Boarding</span>
        )}
      </div>
      <div className="school-card-body">
        <div className="d-flex justify-content-between gap-2 align-items-start">
          <h3 className="h5 mb-1">
            <Link to={`/schools/${school.id}`} className="stretched-link-off">
              {school.name}
            </Link>
          </h3>
          {school.rating != null && (
            <span className="badge text-bg-warning text-dark flex-shrink-0">
              <i className="bi bi-star-fill me-1" />
              {Number(school.rating).toFixed(1)}
              <span className="visually-hidden"> demo rating</span>
            </span>
          )}
        </div>
        <p className="text-muted small mb-2">
          <i className="bi bi-geo-alt me-1" />
          {school.city}
          {school.state ? `, ${school.state}` : ''}
        </p>
        <div className="d-flex flex-wrap gap-1 mb-2">
          {school.board && <span className="badge text-bg-light border">{school.board}</span>}
          {school.school_type && (
            <span className="badge text-bg-light border">{school.school_type}</span>
          )}
          {school.gender && <span className="badge text-bg-light border">{school.gender}</span>}
        </div>
        <p className="fw-semibold mb-2">{formatFeeRange(school.min_fee, school.max_fee)}</p>
        <p className="small text-muted mb-3">
          {facilityNames(school).join(' · ') || 'Facilities listed on detail page'}
        </p>
        <div className="d-flex flex-wrap gap-2 position-relative" style={{ zIndex: 2 }}>
          <Link to={`/schools/${school.id}`} className="btn btn-sm btn-primary">
            View Details
          </Link>
          <button
            type="button"
            className={`btn btn-sm ${selected ? 'btn-warning' : 'btn-outline-secondary'}`}
            onClick={() => toggleSchool(school.id)}
            disabled={!selected && !canAdd}
            title={!selected && !canAdd ? 'Compare up to 3 schools' : undefined}
          >
            {selected ? 'In Compare' : 'Compare'}
          </button>
          {isAuthenticated && isParent && onShortlist && (
            <button
              type="button"
              className={`btn btn-sm ${shortlisted ? 'btn-outline-danger' : 'btn-outline-primary'}`}
              onClick={() => onShortlist(school)}
              disabled={shortlistBusy}
            >
              <i className={`bi ${shortlisted ? 'bi-heart-fill' : 'bi-heart'} me-1`} />
              {shortlisted ? 'Shortlisted' : 'Shortlist'}
            </button>
          )}
        </div>
      </div>
    </article>
  )
}
