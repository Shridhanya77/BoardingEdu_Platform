export default function EmptyState({
  title = 'Nothing here yet',
  message = 'Try adjusting your filters or check back later.',
  action,
}) {
  return (
    <div className="text-center py-5 px-3 be-empty">
      <i className="bi bi-inbox display-5 text-muted" aria-hidden="true" />
      <h2 className="h5 mt-3">{title}</h2>
      <p className="text-muted mb-3">{message}</p>
      {action}
    </div>
  )
}
