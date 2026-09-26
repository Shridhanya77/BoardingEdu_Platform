import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { CompareProvider } from './context/CompareContext'
import MainLayout from './layouts/MainLayout'
import ProtectedRoute from './components/ProtectedRoute'
import ErrorBoundary from './components/ErrorBoundary'
import HomePage from './pages/HomePage'
import SchoolsPage from './pages/SchoolsPage'
import SchoolDetailPage from './pages/SchoolDetailPage'
import ComparePage from './pages/ComparePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import ShortlistedPage from './pages/ShortlistedPage'
import EnquiriesPage from './pages/EnquiriesPage'
import ProfilePage from './pages/ProfilePage'
import AdminDashboardPage from './pages/admin/AdminDashboardPage'
import AdminSchoolsPage from './pages/admin/AdminSchoolsPage'
import AdminSchoolFormPage from './pages/admin/AdminSchoolFormPage'
import AdminEnquiriesPage from './pages/admin/AdminEnquiriesPage'
import AdminUsersPage from './pages/admin/AdminUsersPage'

function NotFoundPage() {
  return (
    <div className="container py-5 text-center">
      <h1 className="h3">Page not found</h1>
      <p className="text-muted">The page you requested does not exist.</p>
      <a href="/" className="btn btn-primary btn-sm">
        Go home
      </a>
    </div>
  )
}

export default function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <CompareProvider>
          <BrowserRouter>
            <MainLayout>
              <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/schools" element={<SchoolsPage />} />
              <Route path="/schools/:id" element={<SchoolDetailPage />} />
              <Route path="/compare" element={<ComparePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />

              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute roles={['parent', 'student']}>
                    <DashboardPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/shortlisted"
                element={
                  <ProtectedRoute roles={['parent', 'student']}>
                    <ShortlistedPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/enquiries"
                element={
                  <ProtectedRoute roles={['parent', 'student']}>
                    <EnquiriesPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/profile"
                element={
                  <ProtectedRoute>
                    <ProfilePage />
                  </ProtectedRoute>
                }
              />

              <Route
                path="/admin"
                element={
                  <ProtectedRoute roles={['admin']}>
                    <AdminDashboardPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/schools"
                element={
                  <ProtectedRoute roles={['admin']}>
                    <AdminSchoolsPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/schools/new"
                element={
                  <ProtectedRoute roles={['admin']}>
                    <AdminSchoolFormPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/schools/:id/edit"
                element={
                  <ProtectedRoute roles={['admin']}>
                    <AdminSchoolFormPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/enquiries"
                element={
                  <ProtectedRoute roles={['admin']}>
                    <AdminEnquiriesPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin/users"
                element={
                  <ProtectedRoute roles={['admin']}>
                    <AdminUsersPage />
                  </ProtectedRoute>
                }
              />

              <Route path="/home" element={<Navigate to="/" replace />} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </MainLayout>
        </BrowserRouter>
      </CompareProvider>
    </AuthProvider>
    </ErrorBoundary>
  )
}
