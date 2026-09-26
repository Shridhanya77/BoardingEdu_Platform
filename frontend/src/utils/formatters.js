export function formatFee(amount) {
  if (amount == null || Number.isNaN(Number(amount))) return 'N/A'
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(Number(amount))
}

export function formatFeeRange(minFee, maxFee) {
  if (minFee == null && maxFee == null) return 'Fee on request'
  if (minFee != null && maxFee != null && minFee !== maxFee) {
    return `${formatFee(minFee)} – ${formatFee(maxFee)}`
  }
  return formatFee(minFee ?? maxFee)
}

export function facilityNames(school, limit = 3) {
  const list = school?.facilities || []
  const names = list.map((f) => f.name).filter(Boolean)
  if (names.length <= limit) return names
  return [...names.slice(0, limit), `+${names.length - limit} more`]
}
