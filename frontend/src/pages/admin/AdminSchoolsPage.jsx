import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import LoadingSpinner from '../../components/LoadingSpinner'
import EmptyState from '../../components/EmptyState'
import AlertMessage from '../../components/AlertMessage'
import { deleteSchool, getSchools } from '../../services/schoolService'
import { getErrorMessage } from '../../services/api'
import { formatFeeRange } from '../../utils/formatters'

export default function AdminSchoolsPage() {
  const [q, setQ] = useState('')
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [busyId, setBusyId] = useState(null)

  const load = (name = q) => {
    setLoading(true)
    getSchools({ q: name || undefined, per_page: 50, sort: 'name' })
      .then((res) => setItems(res.data?.data?.items || []))
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const onDelete = async (school) => {
    if (!window.confirm(`Delete "${school.name}"? This cannot be undone.`)) return
    setBusyId(school.id)
    try {
      await deleteSchool(school.id)
      setItems((prev) => prev.filter((s) => s.id !== school.id))
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div className="container py-4">
      <div className="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
        <div>
          <h1 className="h3 mb-1">Manage schools</h1>
          <p className="text-muted mb-0">Create, edit, and remove school profiles.</p>
        </div>
        <Link to="/admin/schools/new" className="btn btn-primary btn-sm">
          Add school
        </Link>
      </div>
      <form
        className="row g-2 mb-3"
        onSubmit={(e) => {
          e.preventDefault()
          load(q)
        }}
      >
        <div className="col-md-6">
          <input
            className="form-control"
            placeholder="Search by school name"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>
        <div className="col-auto">
          <button type="submit" className="btn btn-outline-primary">
            Search
          </button>
        </div>
      </form>
      <AlertMessage message={error} onClose={() => setError('')} />
      {loading && <LoadingSpinner />}
      {!loading && items.length === 0 && <EmptyState title="No schools found" />}
      {!loading && items.length > 0 && (
        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead className="table-light">
              <tr>
                <th>Name</th>
                <th>City</th>
                <th>Board</th>
                <th>Fees</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {items.map((school) => (
                <tr key={school.id}>
                  <td>
                    <Link to={`/schools/${school.id}`}>{school.name}</Link>
                  </td>
                  <td>{school.city}</td>
                  <td>{school.board}</td>
                  <td>{formatFeeRange(school.min_fee, school.max_fee)}</td>
                  <td className="text-end">
                    <Link
                      to={`/admin/schools/${school.id}/edit`}
                      className="btn btn-sm btn-outline-primary me-1"
                    >
                      Edit
                    </Link>
                    <button
                      type="button"
                      className="btn btn-sm btn-outline-danger"
                      disabled={busyId === school.id}
                      onClick={() => onDelete(school)}
                    >
                      Delete
                    </button>
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
