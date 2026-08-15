import {
  Box,
  Button,
  Flex,
  Input,
  Select,
  Stack,
  Textarea,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import type React from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FeedbackService } from "../../client/sdk.gen"
import type { FeedbackCreate } from "../../client/types.gen"
import useCustomToast from "../../hooks/useCustomToast"
import { Field } from "../ui/field"

interface FeedbackFormProps {
  responseId: number
  onSuccess?: () => void
}

type FeedbackFormValues = Omit<
  FeedbackCreate,
  "feedback_content" | "ai_metadata"
> & {
  confidence_score_percentage?: number
}

const ERROR_TYPES = [
  { value: "conceptual", label: "Conceptual Error" },
  { value: "procedural", label: "Procedural Error" },
  { value: "factual", label: "Factual Error" },
  { value: "minor", label: "Minor Error" },
  { value: "critical", label: "Critical Error" },
]

export const FeedbackForm: React.FC<FeedbackFormProps> = ({
  responseId,
  onSuccess,
}) => {
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const queryClient = useQueryClient()

  const {
    handleSubmit,
    register,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FeedbackFormValues>({
    defaultValues: {
      response_id: responseId,
      feedback_text: "",
      error_type: undefined,
      confidence_score_percentage: 80,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: FeedbackCreate) => {
      return FeedbackService.createFeedback({ requestBody: data })
    },
    onSuccess: () => {
      reset()
      showSuccessToast("Feedback submitted successfully")
      queryClient.invalidateQueries({ queryKey: ["feedback", responseId] })
      if (onSuccess) onSuccess()
    },
    onError: (error) => {
      showErrorToast("Failed to submit feedback")
      console.error("Error submitting feedback:", error)
    },
  })

  const onSubmit: SubmitHandler<FeedbackFormValues> = (data) => {
    // Convert percentage to decimal for the API
    const feedbackData: FeedbackCreate = {
      ...data,
      response_id: responseId,
      confidence_score: data.confidence_score_percentage
        ? data.confidence_score_percentage / 100
        : undefined,
      feedback_content: {}, // Empty object for now
    }
    ;(feedbackData as any).confidence_score_percentage = undefined
    mutation.mutate(feedbackData)
  }

  return (
    <Box as="form" onSubmit={handleSubmit(onSubmit)} w="100%">
      <Stack direction="column" gap={4} align="flex-start">
        <Field
          required
          invalid={!!errors.feedback_text}
          errorText={errors.feedback_text?.message}
          label="Feedback"
        >
          <Textarea
            id="feedback_text"
            placeholder="Enter your feedback here"
            {...register("feedback_text", {
              required: "Feedback is required",
              minLength: {
                value: 5,
                message: "Feedback must be at least 5 characters",
              },
            })}
          />
        </Field>

        <Field
          invalid={!!errors.error_type}
          errorText={errors.error_type?.message}
          label="Error Type"
        >
          <Select.Root
            id="error_type"
            placeholder="Select error type"
            {...register("error_type")}
          >
            {ERROR_TYPES.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </Select.Root>
        </Field>

        <Field
          invalid={!!errors.confidence_score_percentage}
          errorText={errors.confidence_score_percentage?.message}
          label="Confidence Score (%)"
        >
          <Input
            id="confidence_score_percentage"
            type="number"
            min={0}
            max={100}
            {...register("confidence_score_percentage", {
              valueAsNumber: true,
              min: {
                value: 0,
                message: "Confidence score must be at least 0%",
              },
              max: {
                value: 100,
                message: "Confidence score cannot exceed 100%",
              },
            })}
          />
        </Field>

        <Flex justifyContent="flex-end" w="100%" mt={4}>
          <Button
            type="submit"
            colorScheme="blue"
            loading={isSubmitting}
            loadingText="Submitting"
          >
            Submit Feedback
          </Button>
        </Flex>
      </Stack>
    </Box>
  )
}
