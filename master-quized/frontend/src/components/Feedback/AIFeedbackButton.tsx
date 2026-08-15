import { Button, Tooltip } from "@chakra-ui/react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import type React from "react"
import { useState } from "react"
import { FeedbackService } from "../../client/sdk.gen"
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
    queryFn: () => FeedbackService.readFeedbackByResponse({ responseId }),
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
        queryClient.invalidateQueries({
          queryKey: ["feedback", "response", responseId],
        })
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
      <Button size="sm" loading colorScheme="blue" variant="outline">
        Checking feedback status
      </Button>
    )
  }

  // If feedback already exists, show that it exists
  if (existingFeedback) {
    return (
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          <Button
            size="sm"
            colorScheme="green"
            variant="solid"
            disabled
            shadow="sm"
          >
            ✓ Feedback Ready
          </Button>
        </Tooltip.Trigger>
        <Tooltip.Content>This response already has AI feedback</Tooltip.Content>
      </Tooltip.Root>
    )
  }

  // If no feedback exists yet, show the request button
  return (
    <Button
      size="sm"
      colorScheme="purple"
      variant="solid"
      loading={isRequesting}
      loadingText="Generating..."
      onClick={() => requestFeedback()}
      shadow="sm"
      _hover={{
        bg: "purple.600",
        transform: "translateY(-1px)",
        shadow: "md",
      }}
    >
      🤖 Generate AI Feedback
    </Button>
  )
}
