/**
 * Format a date string into a user-friendly format
 * @param dateString The date string to format
 * @returns Formatted date string
 */
export const formatDate = (dateString: string | null | undefined): string => {
  if (!dateString) return 'N/A';
  
  try {
    const date = new Date(dateString);
    return date.toLocaleString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (error) {
    console.error('Error formatting date:', error);
    return 'Invalid date';
  }
};

/**
 * Format a date string to show only the date part
 * @param dateString The date string to format
 * @returns Formatted date string (date only)
 */
export const formatDateOnly = (dateString: string | null | undefined): string => {
  if (!dateString) return 'N/A';
  
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch (error) {
    console.error('Error formatting date:', error);
    return 'Invalid date';
  }
};

/**
 * Format a score value to a percentage
 * @param score - Score value (0-100)
 * @returns Formatted percentage string
 */
export function formatScore(score: number | null | undefined): string {
  if (score === null || score === undefined) return "-"
  return `${Math.round(score)}%`
}
