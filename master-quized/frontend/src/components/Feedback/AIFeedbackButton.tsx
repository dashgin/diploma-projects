import React, { useState } from "react"
import { Button, Tooltip } from "@chakra-ui/react"
import { FeedbackService } from "../../client/sdk.gen"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import useCustomToast from "../../hooks/useCustomToast"

interface AIFeedbackButtonProps {
  responseId: number
}

export const AIFeedbackButton: React.FC<AIFeedbackButtonProps> = ({
  responseId,
}) => {
  const [isRequesting, setIsRequesting] = useState(false)
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const queryClient = useQueryClient()

  // Check if feedback already exists
  const { data: existingFeedback, isLoading } = useQuery({
    queryKey: ["feedback", "response", responseId],
    queryFn: () =>
      FeedbackService.readFeedbackByResponse({ responseId }),
    retry: false,
  })

  // Create mutation for requesting feedback
  const { mutate: requestFeedback } = useMutation({
    mutationFn: () => FeedbackService.requestFeedbackGeneration({ responseId }),
    onMutate: () => {
      setIsRequesting(true)
    },
    onSuccess: () => {
      showSuccessToast("The feedback is being generated in the background.")
      // Invalidate query to trigger a refetch after 2 seconds
      setTimeout(() => {
        queryClient.invalidateQueries({ queryKey: ["feedback", "response", responseId] })
      }, 2000)
    },
    onError: (error: any) => {
      showErrorToast(error.message || "An unexpected error occurred.")
    },
    onSettled: () => {
      setIsRequesting(false)
    },
  })

  // If we're loading, show a loading state
  if (isLoading) {
    return (
      <Button size="sm" isLoading colorScheme="blue" variant="outline">
        Checking feedback status
      </Button>
    )
  }

  // If feedback already exists, show that it exists
  if (existingFeedback) {
    return (
      <Tooltip label="This response already has AI feedback" placement="top">
        <Button size="sm" colorScheme="green" variant="outline" disabled>
          AI Feedback Available
        </Button>
      </Tooltip>
    )
  }

  // If no feedback exists yet, show the request button
  return (
    <Button
      size="sm"
      colorScheme="blue"
      isLoading={isRequesting}
      loadingText="Requesting"
      onClick={() => requestFeedback()}
    >
      Generate AI Feedback
    </Button>
  )
} 