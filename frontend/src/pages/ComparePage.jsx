import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import LoadingSpinner from '../components/LoadingSpinner'
import EmptyState from '../components/EmptyState'
import { getSchool } from '../services/schoolService'
import { getErrorMessage } from '../services/api'
import { formatFeeRange } from '../utils/formatters'
import { useCompare } from '../context/CompareContext'

const ROWS = [
  { key: 'name', label: 'School name' },
  { key: 'location', label: 'Location' },
  { key: 'board', label: 'Board' },
  { key: 'school_type', label: 'School type' },
  { key: 'gender', label: 'Gender' },
  { key: 'annual_fee', label: 'Annual fee' },
  { key: 'hostel', label: 'Hostel availability' },
  { key: 'Library', label: 'Library', facility: true },
  { key: 'Computer Lab', label: 'Computer lab', facility: true },
  { key: 'Sports Complex', label: 'Sports facilities', facility: true },
  { key: 'Swimming Pool', label: 'Swimming pool', facility: true },
  { key: 'Transportation', label: 'Transportation', facility: true },
  { key: 'other', label: 'Other facilities' },
]

function hasFacility(school, name) {
  return (school.facilities || []).some(
    (f) => f.name?.toLowerCase() === name.toLowerCase(),
  )
}

function cellValue(school, row) {
  if (row.facility) return hasFacility(school, row.key) ? 'Yes' : 'No'
  switch (row.key) {
    case 'name':
      return school.name
    case 'location':
      return `${school.city}${school.state ? `, ${school.state}` : ''}`
    case 'board':
      return school.board || '—'
    case 'school_type':
      return school.school_type || '—'
    case 'gender':
      return school.gender || '—'
    case 'annual_fee':
      return formatFeeRange(school.min_fee, school.max_fee)
    case 'hostel':
      return school.hostel_available ? 'Yes' : 'No'
    case 'other':
      return (
        (school.facilities || [])
          .map((f) => f.name)
          .filter(
            (n) =>
              ![
                'Library',
                'Computer Lab',
                'Sports Complex',
                'Swimming Pool',
                'Transportation',
              ].includes(n),
          )
          .join(', ') || '—'
      )
    default:
      return '—'
  }
}

export default function ComparePage() {
  const { ids, removeSchool, clear, max } = useCompare()
  const [schools, setSchools] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (ids.length === 0) {
      setSchools([])
      return
    }
    let ignore = false
    setLoading(true)
    setError('')
    Promise.all(ids.map((id) => getSchool(id)))
      .then((responses) => {
        if (ignore) return
        setSchools(responses.map((r) => r.data?.data?.school).filter(Boolean))
      })
      .catch((err) => {
        if (!ignore) setError(getErrorMessage(err, 'Unable to load comparison.'))
      })
      .finally(() => {
        if (!ignore) setLoading(false)
      })
    return () => {
      ignore = true
    }
  }, [ids])

  return (
    <div className="container py-4">
      <div className="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
        <div>
          <h1 className="h3 mb-1">Compare schools</h1>
          <p className="text-muted mb-0">
            Select 2–{max} schools from listings.
          </p>
        </div>
        {ids.length > 0 && (
          <button type="button" className="btn btn-outline-secondary btn-sm" onClick={clear}>
            Clear all
          </button>
        )}
      </div>

      {error && <div className="alert alert-danger">{error}</div>}
      {loading && <LoadingSpinner label="Loading comparison data..." />}

      {!loading && ids.length === 0 && (
        <EmptyState
          title="No schools selected"
          message="Use the Compare button on school cards to add up to 3 schools."
          action={
            <Link to="/schools" className="btn btn-primary btn-sm">
              Browse schools
            </Link>
          }
        />
      )}

      {!loading && ids.length === 1 && (
        <div className="alert alert-info">
          Add at least one more school to compare. Currently selected:{' '}
          <strong>{schools[0]?.name || `School #${ids[0]}`}</strong>
        </div>
      )}

      {!loading && schools.length >= 2 && (
        <div className="table-responsive be-compare-table">
          <table className="table table-bordered align-middle">
            <thead>
              <tr>
                <th scope="col">Attribute</th>
                {schools.map((school) => (
                  <th scope="col" key={school.id}>
                    <div className="d-flex justify-content-between align-items-start gap-2">
                      <Link to={`/schools/${school.id}`}>{school.name}</Link>
                      <button
                        type="button"
                        className="btn btn-sm btn-outline-danger"
                        onClick={() => removeSchool(school.id)}
                        aria-label={`Remove ${school.name}`}
                      >
                        ×
                      </button>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {ROWS.map((row) => (
                <tr key={row.label}>
                  <th scope="row">{row.label}</th>
                  {schools.map((school) => (
                    <td key={`${school.id}-${row.label}`}>{cellValue(school, row)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
