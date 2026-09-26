import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useCompare } from '../context/CompareContext'

export default function Navbar() {
  const { isAuthenticated, isAdmin, isParent, user, logout } = useAuth()
  const { count } = useCompare()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const linkClass = ({ isActive }) =>
    `nav-link ${isActive ? 'active fw-semibold' : ''}`

  return (
    <nav className="navbar navbar-expand-lg be-navbar sticky-top">
      <div className="container">
        <Link className="navbar-brand be-brand" to="/">
          <i className="bi bi-building me-2" aria-hidden="true" />
          BoardingEdu
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#mainNav"
          aria-controls="mainNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="mainNav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <NavLink className={linkClass} to="/" end>
                Home
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className={linkClass} to="/schools">
                Schools
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className={linkClass} to="/compare">
                Compare
                {count > 0 && (
                  <span className="badge text-bg-warning ms-1">{count}</span>
                )}
              </NavLink>
            </li>
            {isParent && (
              <>
                <li className="nav-item">
                  <NavLink className={linkClass} to="/dashboard">
                    Dashboard
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className={linkClass} to="/shortlisted">
                    Shortlisted
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className={linkClass} to="/enquiries">
                    Enquiries
                  </NavLink>
                </li>
              </>
            )}
            {isAdmin && (
              <li className="nav-item">
                <NavLink className={linkClass} to="/admin">
                  Admin
                </NavLink>
              </li>
            )}
          </ul>
          <div className="d-flex align-items-center gap-2">
            {isAuthenticated ? (
              <>
                <Link className="btn btn-sm btn-outline-primary" to="/profile">
                  <i className="bi bi-person me-1" />
                  {user?.name?.split(' ')[0] || 'Profile'}
                </Link>
                <button
                  type="button"
                  className="btn btn-sm btn-primary"
                  onClick={handleLogout}
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link className="btn btn-sm btn-outline-primary" to="/login">
                  Login
                </Link>
                <Link className="btn btn-sm btn-primary" to="/register">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
