import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProfilePage() {
  const { user, isAdmin } = useAuth()

  return (
    <div className="container py-4" style={{ maxWidth: 640 }}>
      <h1 className="h3 mb-1">Profile</h1>
      <p className="text-muted mb-4">Your BoardingEdu account details.</p>
      <dl className="row be-profile">
        <dt className="col-sm-3">Name</dt>
        <dd className="col-sm-9">{user?.name}</dd>
        <dt className="col-sm-3">Email</dt>
        <dd className="col-sm-9">{user?.email}</dd>
        <dt className="col-sm-3">Phone</dt>
        <dd className="col-sm-9">{user?.phone || '—'}</dd>
        <dt className="col-sm-3">Role</dt>
        <dd className="col-sm-9 text-capitalize">{user?.role}</dd>
        <dt className="col-sm-3">Joined</dt>
        <dd className="col-sm-9">
          {user?.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}
        </dd>
      </dl>
      <Link to={isAdmin ? '/admin' : '/dashboard'} className="btn btn-outline-primary btn-sm">
        Back to dashboard
      </Link>
    </div>
  )
}
