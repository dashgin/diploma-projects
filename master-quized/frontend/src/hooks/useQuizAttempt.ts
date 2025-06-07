import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import { useEffect, useState } from "react"
import {
  AttemptsService,
  QuestionsService,
  ResponsesService,
} from "../client/sdk.gen"
import useCustomToast from "./useCustomToast"

export function useQuizAttempt(attemptId: number | string) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [responses, setResponses] = useState<Record<number, string>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Convert attemptId to number if it's a string
  const attemptIdNumber =
    typeof attemptId === "string" ? Number(attemptId) : attemptId

  // Fetch attempt data
  const { data: attempt, isLoading: isLoadingAttempt } = useQuery({
    queryKey: ["attempt", attemptIdNumber],
    queryFn: () => AttemptsService.readAttempt({ attemptId: attemptIdNumber }),
  })

  // Fetch questions for this quiz
  const { data: questions, isLoading: isLoadingQuestions } = useQuery({
    queryKey: ["questions", attempt?.quiz_id],
    queryFn: () =>
      QuestionsService.readQuestionsByQuiz({
        quizId: attempt?.quiz_id || 0,
        limit: 100,
      }),
    enabled: !!attempt?.quiz_id,
  })

  // Fetch attempt responses with the new structure
  const { data: attemptResponsesData, isLoading: isLoadingResponses } =
    useQuery({
      queryKey: ["responses", attemptIdNumber],
      queryFn: () =>
        ResponsesService.readResponsesByAttempt({
          attemptId: attemptIdNumber,
          limit: 100,
        }),
      enabled: !!attemptIdNumber,
    })

  // Submit response mutation
  const submitResponseMutation = useMutation({
    mutationFn: (data: { questionId: number; answer: string }) => {
      console.log("Submitting response:", data)

      // Check if the answer is a number (indicating a selected option ID for multiple choice)
      const isOptionId = !Number.isNaN(Number(data.answer))
      const selectedOptionId = isOptionId ? Number(data.answer) : null

      console.log(
        "Is option ID:",
        isOptionId,
        "Selected option ID:",
        selectedOptionId,
      )

      return ResponsesService.createResponse({
        requestBody: {
          attempt_id: attemptIdNumber,
          question_id: data.questionId,
          // For multiple choice questions, the answer is the option ID
          answer_text: isOptionId ? "" : data.answer,
          selected_option_id: selectedOptionId,
        },
      })
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["responses", attemptIdNumber],
      })
    },
    onError: (error) => {
      console.error("Error saving response:", error)
      showErrorToast("Failed to save response")
    },
  })

  // Complete attempt mutation
  const completeAttemptMutation = useMutation({
    mutationFn: () => {
      setIsSubmitting(true)
      return AttemptsService.completeAttempt({
        attemptId: attemptIdNumber,
        score: null, // Score will be calculated on the server
      })
    },
    onSuccess: (data) => {
      setIsSubmitting(false)
      showSuccessToast("Quiz submitted successfully")
      navigate({ to: `/quizzes/${data.quiz_id}` })
    },
    onError: (error) => {
      setIsSubmitting(false)
      console.error("Error completing attempt:", error)
      showErrorToast("Failed to submit quiz")
    },
  })

  // Initialize responses from existing data with the new structure
  useEffect(() => {
    if (
      attemptResponsesData?.responses &&
      attemptResponsesData.responses.length > 0
    ) {
      console.log("Attempt responses data:", attemptResponsesData)

      const savedResponses: Record<number, string> = {}
      for (const responseItem of attemptResponsesData.responses) {
        const questionId = responseItem.question.id

        if (
          responseItem.answer.type === "multiple_choice" &&
          typeof responseItem.answer.answer === "object"
        ) {
          // For multiple-choice, use the option_id as the value
          savedResponses[questionId] =
            responseItem.answer.answer.option_id?.toString() || ""
          console.log(
            "Setting multiple choice response for question:",
            questionId,
            "to option:",
            responseItem.answer.answer.option_id,
          )
        } else {
          // For short-answer, use the answer text
          savedResponses[questionId] =
            responseItem.answer.answer?.toString() || ""
          console.log(
            "Setting text response for question:",
            questionId,
            "to:",
            responseItem.answer.answer,
          )
        }
      }

      console.log("Saved responses:", savedResponses)
      setResponses(savedResponses)
    }
  }, [attemptResponsesData])

  // Handle response change
  const handleResponseChange = (questionId: number, answer: string) => {
    setResponses((prev) => ({ ...prev, [questionId]: answer }))
  }

  // Save current response
  const saveCurrentResponse = (questionId: number) => {
    const answer = responses[questionId] || ""

    if (answer.trim()) {
      submitResponseMutation.mutate({ questionId, answer })
    }
  }

  // Navigate to next question
  const handleNext = () => {
    if (!questions?.data?.[currentQuestionIndex]) return

    saveCurrentResponse(questions.data[currentQuestionIndex].id)
    if (questions && currentQuestionIndex < questions.data.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    }
  }

  // Navigate to previous question
  const handlePrevious = () => {
    if (!questions?.data?.[currentQuestionIndex]) return

    saveCurrentResponse(questions.data[currentQuestionIndex].id)
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  // Navigate to specific question
  const handleQuestionSelect = (index: number) => {
    if (!questions?.data?.[currentQuestionIndex]) return

    saveCurrentResponse(questions.data[currentQuestionIndex].id)
    setCurrentQuestionIndex(index)
  }

  // Submit quiz
  const handleSubmitQuiz = () => {
    if (questions?.data?.[currentQuestionIndex]) {
      saveCurrentResponse(questions.data[currentQuestionIndex].id)
    }
    completeAttemptMutation.mutate()
  }

  return {
    attempt,
    questions,
    attemptResponsesData,
    currentQuestionIndex,
    responses,
    isSubmitting,
    isLoading: isLoadingAttempt || isLoadingQuestions || isLoadingResponses,
    handleResponseChange,
    saveCurrentResponse,
    handleNext,
    handlePrevious,
    handleQuestionSelect,
    handleSubmitQuiz,
  }
}
