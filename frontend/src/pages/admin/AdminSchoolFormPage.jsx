import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import AlertMessage from '../../components/AlertMessage'
import LoadingSpinner from '../../components/LoadingSpinner'
import { createSchool, getSchool, updateSchool } from '../../services/schoolService'
import { getErrorMessage } from '../../services/api'

const emptyForm = {
  name: '',
  city: '',
  state: '',
  board: 'CBSE',
  school_type: 'Day School',
  gender: 'Co-ed',
  min_fee: '',
  max_fee: '',
  hostel_available: false,
  rating: 4.0,
  phone: '',
  email: '',
  website: '',
  description: '',
  academic_info: '',
  sports_info: '',
  transport_info: '',
  hostel_info: '',
  admission_process: '',
  address: '',
}

export default function AdminSchoolFormPage() {
  const { id } = useParams()
  const isEdit = Boolean(id)
  const navigate = useNavigate()
  const [form, setForm] = useState(emptyForm)
  const [loading, setLoading] = useState(isEdit)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!isEdit) return
    getSchool(id)
      .then((res) => {
        const s = res.data?.data?.school
        if (!s) return
        setForm({
          name: s.name || '',
          city: s.city || '',
          state: s.state || '',
          board: s.board || 'CBSE',
          school_type: s.school_type || 'Day School',
          gender: s.gender || 'Co-ed',
          min_fee: s.min_fee ?? '',
          max_fee: s.max_fee ?? '',
          hostel_available: Boolean(s.hostel_available),
          rating: s.rating ?? 4.0,
          phone: s.phone || '',
          email: s.email || '',
          website: s.website || '',
          description: s.description || '',
          academic_info: s.academic_info || '',
          sports_info: s.sports_info || '',
          transport_info: s.transport_info || '',
          hostel_info: s.hostel_info || '',
          admission_process: s.admission_process || '',
          address: s.address || '',
        })
      })
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [id, isEdit])

  const onChange = (e) => {
    const { name, value, type, checked } = e.target
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }))
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    const payload = {
      ...form,
      min_fee: form.min_fee === '' ? null : Number(form.min_fee),
      max_fee: form.max_fee === '' ? null : Number(form.max_fee),
      rating: Number(form.rating) || 4.0,
    }
    try {
      if (isEdit) await updateSchool(id, payload)
      else await createSchool(payload)
      navigate('/admin/schools')
    } catch (err) {
      setError(getErrorMessage(err, 'Unable to save school.'))
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div className="container py-4" style={{ maxWidth: 800 }}>
      <nav aria-label="breadcrumb">
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link to="/admin">Admin</Link>
          </li>
          <li className="breadcrumb-item">
            <Link to="/admin/schools">Schools</Link>
          </li>
          <li className="breadcrumb-item active">{isEdit ? 'Edit' : 'Add'}</li>
        </ol>
      </nav>
      <h1 className="h3 mb-3">{isEdit ? 'Edit school' : 'Add school'}</h1>
      <AlertMessage message={error} onClose={() => setError('')} />
      <form onSubmit={onSubmit} className="row g-3">
        {[
          ['name', 'School name', 'text', true],
          ['city', 'City', 'text', true],
          ['state', 'State', 'text', false],
          ['address', 'Address', 'text', false],
          ['phone', 'Phone', 'text', false],
          ['email', 'Email', 'email', false],
          ['website', 'Website', 'text', false],
        ].map(([name, label, type, required]) => (
          <div className="col-md-6" key={name}>
            <label className="form-label">{label}</label>
            <input
              className="form-control"
              name={name}
              type={type}
              required={required}
              value={form[name]}
              onChange={onChange}
            />
          </div>
        ))}
        <div className="col-md-4">
          <label className="form-label">Board</label>
          <select className="form-select" name="board" value={form.board} onChange={onChange}>
            {['CBSE', 'ICSE', 'IB', 'State', 'Cambridge', 'Other'].map((b) => (
              <option key={b}>{b}</option>
            ))}
          </select>
        </div>
        <div className="col-md-4">
          <label className="form-label">School type</label>
          <select
            className="form-select"
            name="school_type"
            value={form.school_type}
            onChange={onChange}
          >
            {['Day School', 'Boarding', 'Day-Boarding'].map((t) => (
              <option key={t}>{t}</option>
            ))}
          </select>
        </div>
        <div className="col-md-4">
          <label className="form-label">Gender</label>
          <select className="form-select" name="gender" value={form.gender} onChange={onChange}>
            {['Co-ed', 'Boys', 'Girls'].map((g) => (
              <option key={g}>{g}</option>
            ))}
          </select>
        </div>
        <div className="col-md-4">
          <label className="form-label">Min fee</label>
          <input
            className="form-control"
            name="min_fee"
            type="number"
            value={form.min_fee}
            onChange={onChange}
          />
        </div>
        <div className="col-md-4">
          <label className="form-label">Max fee</label>
          <input
            className="form-control"
            name="max_fee"
            type="number"
            value={form.max_fee}
            onChange={onChange}
          />
        </div>
        <div className="col-md-4">
          <label className="form-label">Demo rating</label>
          <input
            className="form-control"
            name="rating"
            type="number"
            step="0.1"
            min="0"
            max="5"
            value={form.rating}
            onChange={onChange}
          />
        </div>
        <div className="col-12">
          <div className="form-check">
            <input
              className="form-check-input"
              type="checkbox"
              name="hostel_available"
              id="hostel"
              checked={form.hostel_available}
              onChange={onChange}
            />
            <label className="form-check-label" htmlFor="hostel">
              Hostel / boarding available
            </label>
          </div>
        </div>
        {[
          ['description', 'About / description'],
          ['academic_info', 'Academic information'],
          ['sports_info', 'Sports'],
          ['transport_info', 'Transportation'],
          ['hostel_info', 'Hostel information'],
          ['admission_process', 'Admission process'],
        ].map(([name, label]) => (
          <div className="col-12" key={name}>
            <label className="form-label">{label}</label>
            <textarea
              className="form-control"
              name={name}
              rows="2"
              value={form[name]}
              onChange={onChange}
            />
          </div>
        ))}
        <div className="col-12 d-flex gap-2">
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? 'Saving...' : 'Save school'}
          </button>
          <Link to="/admin/schools" className="btn btn-outline-secondary">
            Cancel
          </Link>
        </div>
      </form>
    </div>
  )
}
