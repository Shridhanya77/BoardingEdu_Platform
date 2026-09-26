import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import AlertMessage from '../components/AlertMessage'
import { useAuth } from '../context/AuthContext'
import { getErrorMessage } from '../services/api'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const onSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      const user = await login(form.email, form.password)
      const redirect =
        location.state?.from || (user.role === 'admin' ? '/admin' : '/dashboard')
      navigate(redirect, { replace: true })
    } catch (err) {
      setError(getErrorMessage(err, 'Login failed.'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="container py-5" style={{ maxWidth: 480 }}>
      <h1 className="h3 mb-1">Login</h1>
      <p className="text-muted mb-4">Access your BoardingEdu parent or admin account.</p>
      <AlertMessage message={error} onClose={() => setError('')} />
      <form onSubmit={onSubmit} className="be-auth-form">
        <div className="mb-3">
          <label className="form-label" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            type="email"
            className="form-control"
            required
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            autoComplete="email"
          />
        </div>
        <div className="mb-3">
          <label className="form-label" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            className="form-control"
            required
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            autoComplete="current-password"
          />
        </div>
        <button type="submit" className="btn btn-primary w-100" disabled={submitting}>
          {submitting ? 'Signing in...' : 'Login'}
        </button>
      </form>
      <p className="small text-muted mt-3 mb-0">
        New parent? <Link to="/register">Create an account</Link>
      </p>
    </div>
  )
}
