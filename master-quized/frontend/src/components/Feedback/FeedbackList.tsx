import { Alert, Box, Spinner, Text } from "@chakra-ui/react"
import { FiAlertCircle } from "react-icons/fi"

import { useQuery } from "@tanstack/react-query"
import type React from "react"
import { FeedbackService } from "../../client/sdk.gen"
import { FeedbackCard } from "./FeedbackCard"

interface FeedbackListProps {
  responseId: number
  showResources?: boolean
}

export const FeedbackList: React.FC<FeedbackListProps> = ({
  responseId,
  showResources = true,
}) => {
  const {
    data: feedback,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["feedback", responseId],
    queryFn: () => FeedbackService.readFeedbackByResponse({ responseId }),
  })

  if (isLoading) {
    return (
      <Box textAlign="center" py={4}>
        <Spinner size="md" />
        <Text mt={2} fontSize="sm" color="gray.600">
          Loading feedback...
        </Text>
      </Box>
    )
  }

  if (error) {
    return (
      <Alert.Root status="error" borderRadius="md">
        <Alert.Indicator>
          <FiAlertCircle />
        </Alert.Indicator>
        An error occurred while loading feedback. Please try again.
      </Alert.Root>
    )
  }

  if (!feedback) {
    return (
      <Alert.Root status="info" borderRadius="md">
        <Alert.Indicator>
          <FiAlertCircle />
        </Alert.Indicator>
        No feedback available for this response.
      </Alert.Root>
    )
  }

  return (
    <Box>
      <FeedbackCard feedback={feedback} showResources={showResources} />
    </Box>
  )
}
