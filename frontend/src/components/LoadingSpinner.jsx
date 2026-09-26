export default function LoadingSpinner({ label = 'Loading...' }) {
  return (
    <div className="text-center py-5" role="status">
      <div className="spinner-border text-primary" aria-hidden="true" />
      <p className="text-muted mt-3 mb-0">{label}</p>
    </div>
  )
}
