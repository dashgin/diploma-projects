/**
 * Simple analytics utility for logging user events
 */

type EventType = "quiz" | "assignment" | "user" | "navigation"

interface EventData {
  [key: string]: any
}

/**
 * Log an analytics event
 * @param category - Type of event
 * @param action - Event action name
 * @param data - Additional event data
 */
export const logEvent = (
  category: EventType,
  action: string,
  data: EventData = {},
) => {
  // Log to console in development
  if (import.meta.env.DEV) {
    console.log(`[Analytics] ${category}:${action}`, data)
  }

  // In production, you could send to an analytics service
  // For example:
  // if (import.meta.env.PROD) {
  //   // Send to your analytics service
  //   analyticsService.trackEvent(category, action, data);
  // }
}
