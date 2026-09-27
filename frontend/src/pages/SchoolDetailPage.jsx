import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import LoadingSpinner from '../components/LoadingSpinner'
import AlertMessage from '../components/AlertMessage'
import { getSchool } from '../services/schoolService'
import { addShortlist, getShortlists, removeShortlist } from '../services/shortlistService'
import { submitEnquiry } from '../services/enquiryService'
import { getErrorMessage } from '../services/api'
import { formatFee, formatFeeRange } from '../utils/formatters'
import { useAuth } from '../context/AuthContext'
import { useCompare } from '../context/CompareContext'

export default function SchoolDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { isAuthenticated, isParent, user } = useAuth()
  const { isSelected, toggleSchool, canAdd } = useCompare()
  const [school, setSchool] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [shortlisted, setShortlisted] = useState(false)
  const [busy, setBusy] = useState(false)
  const [showEnquiry, setShowEnquiry] = useState(false)
  const [activeImage, setActiveImage] = useState(0)

  useEffect(() => {
    let ignore = false
    setLoading(true)
    getSchool(id)
      .then((res) => {
        if (!ignore) setSchool(res.data?.data?.school || null)
      })
      .catch((err) => {
        if (!ignore) setError(getErrorMessage(err, 'School not found.'))
      })
      .finally(() => {
        if (!ignore) setLoading(false)
      })
    return () => {
      ignore = true
    }
  }, [id])

  useEffect(() => {
    if (!isAuthenticated || !isParent || !school) return
    getShortlists()
      .then((res) => {
        const found = (res.data?.data?.items || []).some(
          (row) => (row.school_id || row.school?.id) === school.id,
        )
        setShortlisted(found)
      })
      .catch(() => {})
  }, [isAuthenticated, isParent, school])

  const onShortlist = async () => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: `/schools/${id}` } })
      return
    }
    if (!isParent) return
    setBusy(true)
    try {
      if (shortlisted) {
        await removeShortlist(school.id)
        setShortlisted(false)
      } else {
        await addShortlist(school.id)
        setShortlisted(true)
      }
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setBusy(false)
    }
  }

  const onEnquire = () => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: `/schools/${id}` } })
      return
    }
    setShowEnquiry(true)
  }

  if (loading) return <LoadingSpinner label="Loading school profile..." />
  if (error && !school) {
    return (
      <div className="container py-5">
        <AlertMessage message={error} />
        <Link to="/schools">Back to schools</Link>
      </div>
    )
  }
  if (!school) return null

  const images = school.images?.length
    ? school.images
    : [{ image_url: `https://picsum.photos/seed/be-d-${school.id}/1000/520`, caption: 'Campus' }]
  const selected = isSelected(school.id)
  const mainImage = images[activeImage] || images[0]

  return (
    <div className="container py-4">
      <nav aria-label="breadcrumb">
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link to="/">Home</Link>
          </li>
          <li className="breadcrumb-item">
            <Link to="/schools">Schools</Link>
          </li>
          <li className="breadcrumb-item active" aria-current="page">
            {school.name}
          </li>
        </ol>
      </nav>

      <AlertMessage message={error} onClose={() => setError('')} />

      <div className="be-gallery mb-4">
        <div className="be-gallery-main">
          <img
            src={mainImage.image_url}
            alt={mainImage.caption || school.name}
          />
          {images.length > 1 && (
            <>
              <button
                type="button"
                className="be-gallery-nav be-gallery-prev"
                onClick={() =>
                  setActiveImage((i) => (i - 1 + images.length) % images.length)
                }
                aria-label="Previous image"
              >
                <i className="bi bi-chevron-left" />
              </button>
              <button
                type="button"
                className="be-gallery-nav be-gallery-next"
                onClick={() => setActiveImage((i) => (i + 1) % images.length)}
                aria-label="Next image"
              >
                <i className="bi bi-chevron-right" />
              </button>
            </>
          )}
          {mainImage.caption && (
            <div className="be-gallery-caption">{mainImage.caption}</div>
          )}
        </div>
        {images.length > 1 && (
          <div className="be-gallery-thumbs">
            {images.map((img, idx) => (
              <button
                key={idx}
                type="button"
                className={`be-gallery-thumb ${idx === activeImage ? 'active' : ''}`}
                onClick={() => setActiveImage(idx)}
                aria-label={`View image ${idx + 1}: ${img.caption || ''}`}
              >
                <img src={img.image_url} alt={img.caption || ''} loading="lazy" />
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="row g-4">
        <div className="col-lg-8">
          <div className="d-flex flex-wrap gap-2 align-items-start justify-content-between mb-2">
            <div>
              <h1 className="h2 mb-1">{school.name}</h1>
              <p className="text-muted mb-0">
                <i className="bi bi-geo-alt me-1" />
                {school.address ? `${school.address}, ` : ''}
                {school.city}
                {school.state ? `, ${school.state}` : ''}
              </p>
            </div>
            {school.rating != null && (
              <span className="badge text-bg-warning text-dark">
                <i className="bi bi-star-fill me-1" />
                {Number(school.rating).toFixed(1)} demo rating
              </span>
            )}
          </div>

          <div className="d-flex flex-wrap gap-2 mb-4">
            {school.board && <span className="badge text-bg-primary">{school.board}</span>}
            {school.school_type && (
              <span className="badge text-bg-secondary">{school.school_type}</span>
            )}
            {school.gender && <span className="badge text-bg-light border">{school.gender}</span>}
            {school.hostel_available && (
              <span className="badge text-bg-dark">Hostel available</span>
            )}
          </div>

          <Section title="About school">
            <p>{school.description || 'No description provided.'}</p>
          </Section>
          <Section title="Academic information">
            <p>{school.academic_info || '—'}</p>
          </Section>
          <Section title="Fee structure">
            <p className="small text-muted">Demo/sample fee data for evaluation.</p>
            <p className="fw-semibold">
              Annual range: {formatFeeRange(school.min_fee, school.max_fee)}
            </p>
            <div className="table-responsive">
              <table className="table table-sm table-bordered align-middle">
                <thead className="table-light">
                  <tr>
                    <th>Class</th>
                    <th>Admission</th>
                    <th>Tuition</th>
                    <th>Hostel</th>
                    <th>Transport</th>
                    <th>Other</th>
                    <th>Annual</th>
                  </tr>
                </thead>
                <tbody>
                  {(school.fees || []).map((fee) => (
                    <tr key={fee.id}>
                      <td>{fee.class_name}</td>
                      <td>{formatFee(fee.admission_fee)}</td>
                      <td>{formatFee(fee.tuition_fee)}</td>
                      <td>{formatFee(fee.hostel_fee)}</td>
                      <td>{formatFee(fee.transport_fee)}</td>
                      <td>{formatFee(fee.other_fee)}</td>
                      <td className="fw-semibold">{formatFee(fee.annual_fee)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Section>
          <Section title="Infrastructure">
            <ul className="mb-0">
              {(school.infrastructure || []).map((item) => (
                <li key={item.id}>
                  <strong>{item.category}:</strong> {item.description}
                </li>
              ))}
              {!school.infrastructure?.length && <li>—</li>}
            </ul>
          </Section>
          <Section title="Facilities">
            <div className="d-flex flex-wrap gap-2">
              {(school.facilities || []).map((f) => (
                <span key={f.id} className="badge text-bg-light border">
                  {f.name}
                </span>
              ))}
            </div>
          </Section>
          <Section title="Hostel / boarding">
            <p>{school.hostel_info || (school.hostel_available ? 'Available' : 'Not available')}</p>
          </Section>
          <Section title="Sports">
            <p>{school.sports_info || '—'}</p>
          </Section>
          <Section title="Transportation">
            <p>{school.transport_info || '—'}</p>
          </Section>
          <Section title="Admission process">
            <p>{school.admission_process || '—'}</p>
          </Section>
          <Section title="Contact information">
            <ul className="list-unstyled mb-0">
              <li>Phone: {school.phone || '—'}</li>
              <li>Email: {school.email || '—'}</li>
              <li>Website: {school.website || '—'}</li>
            </ul>
          </Section>
        </div>

        <div className="col-lg-4">
          <div className="be-side-actions sticky-lg-top">
            <p className="fw-semibold mb-3">Next steps</p>
            <div className="d-grid gap-2">
              <button
                type="button"
                className={`btn ${shortlisted ? 'btn-outline-danger' : 'btn-outline-primary'}`}
                onClick={onShortlist}
                disabled={busy}
              >
                <i className={`bi ${shortlisted ? 'bi-heart-fill' : 'bi-heart'} me-1`} />
                {shortlisted ? 'Remove shortlist' : 'Shortlist'}
              </button>
              <button
                type="button"
                className={`btn ${selected ? 'btn-warning' : 'btn-outline-secondary'}`}
                onClick={() => toggleSchool(school.id)}
                disabled={!selected && !canAdd}
              >
                {selected ? 'In compare list' : 'Add to compare'}
              </button>
              <button type="button" className="btn btn-primary" onClick={onEnquire}>
                Admission enquiry
              </button>
              <Link to="/compare" className="btn btn-link">
                Go to compare
              </Link>
            </div>
            {!isAuthenticated && (
              <p className="small text-muted mt-3 mb-0">
                Login required to permanently shortlist or submit an enquiry.
              </p>
            )}
          </div>
        </div>
      </div>

      {showEnquiry && (
        <EnquiryModal
          school={school}
          user={user}
          onClose={() => setShowEnquiry(false)}
        />
      )}
    </div>
  )
}

function Section({ title, children }) {
  return (
    <section className="mb-4">
      <h2 className="h5 border-bottom pb-2">{title}</h2>
      {children}
    </section>
  )
}

function EnquiryModal({ school, user, onClose }) {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    student_name: '',
    parent_name: user?.name || '',
    class_name: '',
    academic_year: '2026-27',
    phone: user?.phone || '',
    email: user?.email || '',
    message: '',
  })
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  const onSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      await submitEnquiry({ ...form, school_id: school.id })
      setSuccess(true)
    } catch (err) {
      setError(getErrorMessage(err, 'Unable to submit enquiry.'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="modal show d-block" tabIndex="-1" role="dialog" style={{ background: 'rgba(0,0,0,.45)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h2 className="modal-title h5">Admission enquiry — {school.name}</h2>
            <button type="button" className="btn-close" aria-label="Close" onClick={onClose} />
          </div>
          <div className="modal-body">
            {success ? (
              <div className="text-center py-3">
                <i className="bi bi-check-circle text-success display-6" />
                <p className="mt-3 mb-3">Enquiry submitted. Track it under Enquiries.</p>
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => navigate('/enquiries')}
                >
                  View enquiries
                </button>
              </div>
            ) : (
              <form onSubmit={onSubmit} className="row g-2">
                <AlertMessage message={error} />
                {[
                  ['student_name', 'Student name', true],
                  ['parent_name', 'Parent name', true],
                  ['class_name', 'Class / grade', false],
                  ['academic_year', 'Academic year', false],
                  ['phone', 'Phone', false],
                  ['email', 'Email', false],
                ].map(([key, label, required]) => (
                  <div className="col-12" key={key}>
                    <label className="form-label small">{label}</label>
                    <input
                      className="form-control"
                      required={required}
                      value={form[key]}
                      onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                    />
                  </div>
                ))}
                <div className="col-12">
                  <label className="form-label small">Message</label>
                  <textarea
                    className="form-control"
                    rows="3"
                    value={form.message}
                    onChange={(e) => setForm({ ...form, message: e.target.value })}
                  />
                </div>
                <div className="col-12 d-grid">
                  <button type="submit" className="btn btn-primary" disabled={submitting}>
                    {submitting ? 'Submitting...' : 'Submit enquiry'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
