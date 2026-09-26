import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import SchoolCard from '../components/SchoolCard'
import LoadingSpinner from '../components/LoadingSpinner'
import { getSchools } from '../services/schoolService'
import { getErrorMessage } from '../services/api'

const QUICK_FILTERS = [
  { label: 'Boarding', params: { hostel_available: true } },
  { label: 'Day School', params: { school_type: 'Day School' } },
  { label: 'CBSE', params: { board: 'CBSE' } },
  { label: 'ICSE', params: { board: 'ICSE' } },
  { label: 'IB', params: { board: 'IB' } },
]

const CITIES = ['Mumbai', 'Pune', 'Bengaluru', 'Delhi', 'Chennai', 'Hyderabad']

export default function HomePage() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [city, setCity] = useState('')
  const [featured, setFeatured] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let ignore = false
    getSchools({ sort: 'rating', per_page: 3 })
      .then((res) => {
        if (!ignore) setFeatured(res.data?.data?.items || [])
      })
      .catch((err) => {
        if (!ignore) setError(getErrorMessage(err, 'Unable to load featured schools.'))
      })
      .finally(() => {
        if (!ignore) setLoading(false)
      })
    return () => {
      ignore = true
    }
  }, [])

  const onSearch = (e) => {
    e.preventDefault()
    const params = new URLSearchParams()
    if (name.trim()) params.set('q', name.trim())
    if (city.trim()) params.set('city', city.trim())
    navigate(`/schools?${params.toString()}`)
  }

  return (
    <>
      <section className="be-hero">
        <div className="be-hero-overlay" />
        <div className="container be-hero-content">
          <p className="be-hero-brand">BoardingEdu</p>
          <h1 className="be-hero-title">Find the Right School for Your Child</h1>
          <p className="be-hero-sub">
            Discover schools, explore fees and facilities, compare options, and
            submit admission enquiries — built for parents and students.
          </p>
          <form className="be-hero-search row g-2" onSubmit={onSearch}>
            <div className="col-md-5">
              <label className="visually-hidden" htmlFor="hero-name">
                School name
              </label>
              <input
                id="hero-name"
                className="form-control form-control-lg"
                placeholder="Search by school name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="col-md-4">
              <label className="visually-hidden" htmlFor="hero-city">
                City
              </label>
              <input
                id="hero-city"
                className="form-control form-control-lg"
                placeholder="City / location"
                value={city}
                onChange={(e) => setCity(e.target.value)}
              />
            </div>
            <div className="col-md-3">
              <button type="submit" className="btn btn-lg btn-warning w-100 fw-semibold">
                Search Schools
              </button>
            </div>
          </form>
          <div className="be-quick-filters mt-3">
            {QUICK_FILTERS.map((item) => {
              const qs = new URLSearchParams(item.params).toString()
              return (
                <Link key={item.label} className="be-chip" to={`/schools?${qs}`}>
                  {item.label}
                </Link>
              )
            })}
          </div>
        </div>
      </section>

      <section className="container py-5">
        <div className="d-flex justify-content-between align-items-end mb-4">
          <div>
            <h2 className="h3 mb-1">Featured Schools</h2>
            <p className="text-muted mb-0">Top-rated demo schools to explore first.</p>
          </div>
          <Link to="/schools" className="btn btn-outline-primary btn-sm">
            View all
          </Link>
        </div>
        {loading && <LoadingSpinner label="Loading featured schools..." />}
        {error && <div className="alert alert-danger">{error}</div>}
        {!loading && !error && (
          <div className="row g-4">
            {featured.map((school) => (
              <div className="col-md-4" key={school.id}>
                <SchoolCard school={school} />
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="be-section-alt py-5">
        <div className="container">
          <h2 className="h3 mb-2">Explore Schools by City</h2>
          <p className="text-muted mb-4">Browse popular education hubs across India.</p>
          <div className="row g-3">
            {CITIES.map((c) => (
              <div className="col-6 col-md-4 col-lg-2" key={c}>
                <Link className="be-city-tile" to={`/schools?city=${encodeURIComponent(c)}`}>
                  <i className="bi bi-geo-alt-fill me-2" />
                  {c}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="container py-5">
        <h2 className="h3 mb-2">Why BoardingEdu?</h2>
        <p className="text-muted mb-4">
          A clearer path from discovery to admission enquiry.
        </p>
        <div className="row g-4">
          {[
            {
              icon: 'bi-search',
              title: 'Discover with filters',
              text: 'Search by board, fees, boarding, and facilities — powered by the API.',
            },
            {
              icon: 'bi-layout-three-columns',
              title: 'Compare side by side',
              text: 'Shortlist up to three schools and compare fees, facilities, and more.',
            },
            {
              icon: 'bi-chat-dots',
              title: 'Enquire with confidence',
              text: 'Submit admission enquiries and track status from your parent dashboard.',
            },
          ].map((item) => (
            <div className="col-md-4" key={item.title}>
              <div className="be-feature">
                <i className={`bi ${item.icon} be-feature-icon`} />
                <h3 className="h5">{item.title}</h3>
                <p className="text-muted mb-0">{item.text}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="be-section-alt py-5">
        <div className="container">
          <h2 className="h3 mb-4">How It Works</h2>
          <ol className="be-steps row g-3 list-unstyled mb-0">
            {[
              'Search and filter schools',
              'Open a school profile for fees & facilities',
              'Compare and shortlist favourites',
              'Register and submit an admission enquiry',
            ].map((step, index) => (
              <li className="col-md-3" key={step}>
                <div className="be-step">
                  <span className="be-step-num">{index + 1}</span>
                  <p className="mb-0 fw-semibold">{step}</p>
                </div>
              </li>
            ))}
          </ol>
        </div>
      </section>

      <section className="container py-5">
        <div className="be-cta text-center p-4 p-md-5">
          <h2 className="h3 mb-2">Ready to find the right school?</h2>
          <p className="text-muted mb-4">
            Start with a search, or create a free parent account to shortlist and enquire.
          </p>
          <div className="d-flex flex-wrap gap-2 justify-content-center">
            <Link to="/schools" className="btn btn-primary btn-lg">
              Browse Schools
            </Link>
            <Link to="/register" className="btn btn-outline-primary btn-lg">
              Create Account
            </Link>
          </div>
        </div>
      </section>
    </>
  )
}
