/**
 * Format a date string to a more readable format
 * @param dateString - ISO date string
 * @returns Formatted date string
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date)
}

/**
 * Format a score value to a percentage
 * @param score - Score value (0-100)
 * @returns Formatted percentage string
 */
export function formatScore(score: number | null | undefined): string {
  if (score === null || score === undefined) return "-"
  return `${Math.round(score)}%`
}
