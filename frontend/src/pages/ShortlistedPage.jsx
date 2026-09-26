import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import SchoolCard from '../components/SchoolCard'
import LoadingSpinner from '../components/LoadingSpinner'
import EmptyState from '../components/EmptyState'
import AlertMessage from '../components/AlertMessage'
import { getShortlists, removeShortlist } from '../services/shortlistService'
import { getErrorMessage } from '../services/api'

export default function ShortlistedPage() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [busyId, setBusyId] = useState(null)

  const load = () => {
    setLoading(true)
    getShortlists()
      .then((res) => setItems(res.data?.data?.items || []))
      .catch((err) => setError(getErrorMessage(err)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
  }, [])

  const onRemove = async (school) => {
    setBusyId(school.id)
    try {
      await removeShortlist(school.id)
      setItems((prev) => prev.filter((row) => (row.school_id || row.school?.id) !== school.id))
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div className="container py-4">
      <h1 className="h3 mb-1">Shortlisted schools</h1>
      <p className="text-muted mb-4">Schools you saved for later.</p>
      <AlertMessage message={error} onClose={() => setError('')} />
      {loading && <LoadingSpinner />}
      {!loading && items.length === 0 && (
        <EmptyState
          title="No shortlisted schools"
          message="Browse schools and tap Shortlist to save them here."
          action={
            <Link to="/schools" className="btn btn-primary btn-sm">
              Browse schools
            </Link>
          }
        />
      )}
      <div className="row g-4">
        {items.map((row) => {
          const school = row.school
          if (!school) return null
          return (
            <div className="col-md-4" key={row.id}>
              <SchoolCard
                school={school}
                shortlisted
                onShortlist={onRemove}
                shortlistBusy={busyId === school.id}
              />
            </div>
          )
        })}
      </div>
    </div>
  )
}
