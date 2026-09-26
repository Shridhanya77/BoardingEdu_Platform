import { useEffect, useState } from 'react'
import LoadingSpinner from '../../components/LoadingSpinner'
import AlertMessage from '../../components/AlertMessage'
import { getAdminUsers } from '../../services/adminService'
import { getErrorMessage } from '../../services/api'

export default function AdminUsersPage() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getAdminUsers()
      .then((res) => setItems(res.data?.data?.items || []))
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="container py-4">
      <h1 className="h3 mb-1">Registered users</h1>
      <p className="text-muted mb-4">Parents and students on the platform.</p>
      <AlertMessage message={error} onClose={() => setError('')} />
      {loading && <LoadingSpinner />}
      {!loading && (
        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead className="table-light">
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Role</th>
                <th>Joined</th>
              </tr>
            </thead>
            <tbody>
              {items.map((user) => (
                <tr key={user.id}>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>{user.phone || '—'}</td>
                  <td className="text-capitalize">{user.role}</td>
                  <td>
                    {user.created_at ? new Date(user.created_at).toLocaleDateString() : '—'}
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
