import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="be-footer mt-auto">
      <div className="container py-5">
        <div className="row g-4">
          <div className="col-md-5">
            <h5 className="be-brand mb-2">BoardingEdu</h5>
            <p className="text-muted mb-0 small">
              Discover, compare, and enquire about schools — a BoardingEdu
              school discovery &amp; admission prototype for parents and
              students.
            </p>
          </div>
          <div className="col-md-3">
            <h6 className="fw-semibold">Explore</h6>
            <ul className="list-unstyled small">
              <li>
                <Link to="/schools">Schools</Link>
              </li>
              <li>
                <Link to="/compare">Compare</Link>
              </li>
              <li>
                <Link to="/register">Register</Link>
              </li>
            </ul>
          </div>
          <div className="col-md-4">
            <h6 className="fw-semibold">Note</h6>
            <p className="small text-muted mb-0">
              School profiles and fees shown here are not affiliated with real institutions.
            </p>
          </div>
        </div>
        <hr className="my-4" />
        <p className="small text-muted mb-0 text-center">
          © {new Date().getFullYear()} BoardingEdu Platform · Portfolio prototype
        </p>
      </div>
    </footer>
  )
}
