import { useCallback, useEffect, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import SchoolCard from '../components/SchoolCard'
import LoadingSpinner from '../components/LoadingSpinner'
import EmptyState from '../components/EmptyState'
import AlertMessage from '../components/AlertMessage'
import { getSchoolFilters, getSchools } from '../services/schoolService'
import { addShortlist, getShortlists, removeShortlist } from '../services/shortlistService'
import { getErrorMessage } from '../services/api'
import { useAuth } from '../context/AuthContext'

const defaultFilters = {
  q: '',
  city: '',
  board: '',
  school_type: '',
  gender: '',
  hostel_available: '',
  min_fee: '',
  max_fee: '',
  facility_ids: '',
  sort: 'name',
}

export default function SchoolsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const { isAuthenticated, isParent } = useAuth()
  const [filters, setFilters] = useState(() => ({
    ...defaultFilters,
    q: searchParams.get('q') || searchParams.get('name') || '',
    city: searchParams.get('city') || '',
    board: searchParams.get('board') || '',
    school_type: searchParams.get('school_type') || '',
    gender: searchParams.get('gender') || '',
    hostel_available:
      searchParams.get('hostel_available') || searchParams.get('boarding') || '',
    min_fee: searchParams.get('min_fee') || '',
    max_fee: searchParams.get('max_fee') || '',
    facility_ids: searchParams.get('facility_ids') || '',
    sort: searchParams.get('sort') || 'name',
  }))
  const [page, setPage] = useState(Number(searchParams.get('page') || 1))
  const [options, setOptions] = useState(null)
  const [items, setItems] = useState([])
  const [pagination, setPagination] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [shortlistedIds, setShortlistedIds] = useState(new Set())
  const [busyId, setBusyId] = useState(null)

  useEffect(() => {
    getSchoolFilters()
      .then((res) => setOptions(res.data?.data || null))
      .catch(() => setOptions(null))
  }, [])

  useEffect(() => {
    if (!isAuthenticated || !isParent) return
    getShortlists()
      .then((res) => {
        const ids = new Set(
          (res.data?.data?.items || []).map((row) => row.school_id || row.school?.id),
        )
        setShortlistedIds(ids)
      })
      .catch(() => {})
  }, [isAuthenticated, isParent])

  const loadSchools = useCallback(async () => {
    setLoading(true)
    setError('')
    const params = {
      page,
      per_page: 9,
      sort: filters.sort || 'name',
    }
    if (filters.q) params.q = filters.q
    if (filters.city) params.city = filters.city
    if (filters.board) params.board = filters.board
    if (filters.school_type) params.school_type = filters.school_type
    if (filters.gender) params.gender = filters.gender
    if (filters.hostel_available !== '') {
      params.hostel_available = filters.hostel_available
    }
    if (filters.min_fee) params.min_fee = filters.min_fee
    if (filters.max_fee) params.max_fee = filters.max_fee
    if (filters.facility_ids) params.facility_ids = filters.facility_ids

    try {
      const res = await getSchools(params)
      setItems(res.data?.data?.items || [])
      setPagination(res.data?.data?.pagination || null)
    } catch (err) {
      setError(getErrorMessage(err, 'Unable to load schools.'))
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [filters, page])

  useEffect(() => {
    loadSchools()
  }, [loadSchools])

  const applyFilters = (e) => {
    e.preventDefault()
    const next = new URLSearchParams()
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== '' && value != null) next.set(key === 'q' ? 'q' : key, value)
    })
    next.set('page', '1')
    setPage(1)
    setSearchParams(next)
  }

  const resetFilters = () => {
    setFilters(defaultFilters)
    setPage(1)
    setSearchParams({})
  }

  const onShortlist = async (school) => {
    if (!isAuthenticated) return
    setBusyId(school.id)
    try {
      if (shortlistedIds.has(school.id)) {
        await removeShortlist(school.id)
        setShortlistedIds((prev) => {
          const next = new Set(prev)
          next.delete(school.id)
          return next
        })
      } else {
        await addShortlist(school.id)
        setShortlistedIds((prev) => new Set(prev).add(school.id))
      }
    } catch (err) {
      setError(getErrorMessage(err, 'Shortlist update failed.'))
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div className="container py-4">
      <nav aria-label="breadcrumb">
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link to="/">Home</Link>
          </li>
          <li className="breadcrumb-item active" aria-current="page">
            Schools
          </li>
        </ol>
      </nav>
      <h1 className="h3 mb-1">Discover Schools</h1>
      <p className="text-muted mb-4">
        Search and filter using live API data. Fees and ratings are demo/sample values.
      </p>

      <div className="row g-4">
        <aside className="col-lg-3">
          <form className="be-filter-panel" onSubmit={applyFilters}>
            <h2 className="h6">Filters</h2>
            <div className="mb-2">
              <label className="form-label small">School name</label>
              <input
                className="form-control form-control-sm"
                value={filters.q}
                onChange={(e) => setFilters({ ...filters, q: e.target.value })}
              />
            </div>
            <div className="mb-2">
              <label className="form-label small">City</label>
              <input
                className="form-control form-control-sm"
                value={filters.city}
                onChange={(e) => setFilters({ ...filters, city: e.target.value })}
                list="city-options"
              />
              <datalist id="city-options">
                {(options?.cities || []).map((c) => (
                  <option key={c} value={c} />
                ))}
              </datalist>
            </div>
            <div className="mb-2">
              <label className="form-label small">Board</label>
              <select
                className="form-select form-select-sm"
                value={filters.board}
                onChange={(e) => setFilters({ ...filters, board: e.target.value })}
              >
                <option value="">Any</option>
                {(options?.boards || ['CBSE', 'ICSE', 'IB', 'State']).map((b) => (
                  <option key={b} value={b}>
                    {b}
                  </option>
                ))}
              </select>
            </div>
            <div className="mb-2">
              <label className="form-label small">School type</label>
              <select
                className="form-select form-select-sm"
                value={filters.school_type}
                onChange={(e) => setFilters({ ...filters, school_type: e.target.value })}
              >
                <option value="">Any</option>
                {(options?.school_types || ['Day School', 'Boarding', 'Day-Boarding']).map(
                  (t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ),
                )}
              </select>
            </div>
            <div className="mb-2">
              <label className="form-label small">Gender</label>
              <select
                className="form-select form-select-sm"
                value={filters.gender}
                onChange={(e) => setFilters({ ...filters, gender: e.target.value })}
              >
                <option value="">Any</option>
                {(options?.genders || ['Co-ed', 'Boys', 'Girls']).map((g) => (
                  <option key={g} value={g}>
                    {g}
                  </option>
                ))}
              </select>
            </div>
            <div className="mb-2">
              <label className="form-label small">Boarding</label>
              <select
                className="form-select form-select-sm"
                value={filters.hostel_available}
                onChange={(e) =>
                  setFilters({ ...filters, hostel_available: e.target.value })
                }
              >
                <option value="">Any</option>
                <option value="true">Available</option>
                <option value="false">Not available</option>
              </select>
            </div>
            <div className="row g-2 mb-2">
              <div className="col-6">
                <label className="form-label small">Min fee</label>
                <input
                  type="number"
                  className="form-control form-control-sm"
                  value={filters.min_fee}
                  onChange={(e) => setFilters({ ...filters, min_fee: e.target.value })}
                />
              </div>
              <div className="col-6">
                <label className="form-label small">Max fee</label>
                <input
                  type="number"
                  className="form-control form-control-sm"
                  value={filters.max_fee}
                  onChange={(e) => setFilters({ ...filters, max_fee: e.target.value })}
                />
              </div>
            </div>
            <div className="mb-3">
              <label className="form-label small">Facility ID(s)</label>
              <input
                className="form-control form-control-sm"
                placeholder="e.g. 1,5"
                value={filters.facility_ids}
                onChange={(e) => setFilters({ ...filters, facility_ids: e.target.value })}
              />
              <div className="form-text">
                Use IDs from filter options (must have all).
              </div>
            </div>
            <div className="d-grid gap-2">
              <button type="submit" className="btn btn-primary btn-sm">
                Apply filters
              </button>
              <button type="button" className="btn btn-outline-secondary btn-sm" onClick={resetFilters}>
                Reset
              </button>
            </div>
          </form>
        </aside>

        <div className="col-lg-9">
          <div className="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
            <p className="mb-0 text-muted small">
              {pagination ? `${pagination.total} schools found` : ' '}
            </p>
            <div className="d-flex align-items-center gap-2">
              <label className="small mb-0" htmlFor="sort">
                Sort
              </label>
              <select
                id="sort"
                className="form-select form-select-sm"
                style={{ width: 'auto' }}
                value={filters.sort}
                onChange={(e) => {
                  const sort = e.target.value
                  setFilters((prev) => ({ ...prev, sort }))
                  setPage(1)
                }}
              >
                <option value="name">Name</option>
                <option value="fee_asc">Fee: low to high</option>
                <option value="fee_desc">Fee: high to low</option>
                <option value="rating">Rating</option>
              </select>
            </div>
          </div>

          <AlertMessage message={error} onClose={() => setError('')} />

          {loading && <LoadingSpinner label="Loading schools..." />}
          {!loading && !error && items.length === 0 && (
            <EmptyState
              title="No schools match"
              message="Try clearing some filters or searching a different city."
              action={
                <button type="button" className="btn btn-outline-primary btn-sm" onClick={resetFilters}>
                  Clear filters
                </button>
              }
            />
          )}
          {!loading && items.length > 0 && (
            <div className="row g-4">
              {items.map((school) => (
                <div className="col-md-6 col-xl-4" key={school.id}>
                  <SchoolCard
                    school={school}
                    shortlisted={shortlistedIds.has(school.id)}
                    onShortlist={onShortlist}
                    shortlistBusy={busyId === school.id}
                  />
                </div>
              ))}
            </div>
          )}

          {pagination && pagination.pages > 1 && (
            <nav className="mt-4" aria-label="School pagination">
              <ul className="pagination justify-content-center">
                <li className={`page-item ${!pagination.has_prev ? 'disabled' : ''}`}>
                  <button
                    type="button"
                    className="page-link"
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={!pagination.has_prev}
                  >
                    Previous
                  </button>
                </li>
                <li className="page-item disabled">
                  <span className="page-link">
                    Page {pagination.page} of {pagination.pages}
                  </span>
                </li>
                <li className={`page-item ${!pagination.has_next ? 'disabled' : ''}`}>
                  <button
                    type="button"
                    className="page-link"
                    onClick={() => setPage((p) => p + 1)}
                    disabled={!pagination.has_next}
                  >
                    Next
                  </button>
                </li>
              </ul>
            </nav>
          )}
        </div>
      </div>
    </div>
  )
}
