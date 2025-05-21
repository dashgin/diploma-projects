import {
  Box,
  Card,
  Button as ChakraButton,
  Container,
  Flex,
  Heading,
  Progress,
  Spinner,
  Stack,
  Text,
  Textarea,
} from "@chakra-ui/react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import { useState } from "react"

import {
  type AttemptCreate,
  AttemptsService,
  OptionsService,
  QuestionsService,
  QuizzesService,
  type ResponseCreate,
  ResponsesService,
} from "@/client"
import { Button } from "@/components/ui/button"
import { Radio, RadioGroup } from "@/components/ui/radio"
import useCustomToast from "@/hooks/useCustomToast"

interface QuizTakerProps {
  quizId: number
  assignmentId?: number
}

export function QuizTaker({ quizId, assignmentId }: QuizTakerProps) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [attemptId, setAttemptId] = useState<number | null>(null)
  const [responses, setResponses] = useState<Record<number, string | number>>(
    {},
  )
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const navigate = useNavigate()

  // Fetch quiz details
  const { data: quiz, isLoading: isLoadingQuiz } = useQuery({
    queryKey: ["quizzes", quizId],
    queryFn: () => QuizzesService.readQuiz({ quizId }),
  })

  // Fetch questions
  const { data: questionsData, isLoading: isLoadingQuestions } = useQuery({
    queryKey: ["questions", quizId],
    queryFn: () => QuestionsService.readQuestionsByQuiz({ quizId }),
    enabled: !!quizId,
  })

  // Get current user info (for student_id)
  const { data: userData } = useQuery({
    queryKey: ["me"],
    queryFn: () => import("@/client").then((m) => m.UsersService.readUserMe()),
  })

  const questions = questionsData?.data || []
  const currentQuestion = questions[currentQuestionIndex]

  // Fetch options if question is multiple choice
  const { data: optionsResponse, isLoading: isLoadingOptions } = useQuery({
    queryKey: ["options", currentQuestion?.id],
    queryFn: () =>
      OptionsService.readOptionsByQuestion({
        questionId: currentQuestion?.id ?? 0,
      }),
    enabled:
      !!currentQuestion?.id &&
      currentQuestion?.question_type === "multiple_choice",
  })

  const options = optionsResponse?.data || []

  // Create attempt mutation
  const createAttemptMutation = useMutation({
    mutationFn: (attemptData: AttemptCreate) =>
      AttemptsService.createAttempt({
        requestBody: attemptData,
      }),
    onSuccess: (data) => {
      setAttemptId(data.id)
    },
    onError: (error) => {
      showErrorToast("Failed to start quiz attempt")
    },
  })

  // Submit response mutation
  const submitResponseMutation = useMutation({
    mutationFn: (responseData: ResponseCreate) =>
      ResponsesService.createResponse({
        requestBody: responseData,
      }),
    onError: (error) => {
      showErrorToast("Failed to submit response")
    },
  })

  // Complete attempt mutation
  const completeAttemptMutation = useMutation({
    mutationFn: (id: number) =>
      AttemptsService.completeAttempt({
        attemptId: id,
      }),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["attempts"] })
      showSuccessToast("Quiz completed successfully!")
      navigate({ to: `/attempts/${data.id}` })
    },
    onError: (error) => {
      showErrorToast("Failed to complete quiz")
    },
  })

  // Start quiz attempt if not started
  const startQuiz = async () => {
    if (!userData) return

    try {
      await createAttemptMutation.mutateAsync({
        student_id: userData.id,
        quiz_id: quizId,
        assignment_id: assignmentId || null,
      })
    } catch (error) {
      console.error("Failed to start quiz:", error)
    }
  }

  // Submit response for current question
  const submitResponse = async () => {
    if (!attemptId || !currentQuestion) return

    const responseValue = responses[currentQuestion.id]
    if (responseValue === undefined) {
      showErrorToast("Please provide an answer")
      return
    }

    // For multiple choice, the responseValue is the option ID
    // For text questions, the responseValue is the text answer
    const isMultipleChoice = currentQuestion.question_type === "multiple_choice"

    try {
      await submitResponseMutation.mutateAsync({
        attempt_id: attemptId,
        question_id: currentQuestion.id,
        answer_text: isMultipleChoice
          ? options.find((opt) => opt.id === responseValue)?.text || ""
          : (responseValue as string),
        selected_option_id: isMultipleChoice ? (responseValue as number) : null,
      })

      // Move to next question or complete quiz
      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1)
      } else {
        await completeAttemptMutation.mutateAsync(attemptId)
      }
    } catch (error) {
      console.error("Failed to submit response:", error)
    }
  }

  // Skip current question
  const skipQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    } else {
      // If on last question, attempt to complete quiz
      if (attemptId) {
        completeAttemptMutation.mutate(attemptId)
      }
    }
  }

  // Handle response input change
  const handleResponseChange = (value: string | number) => {
    if (!currentQuestion) return

    setResponses({
      ...responses,
      [currentQuestion.id]: value,
    })
  }

  // Loading state
  if (isLoadingQuiz || isLoadingQuestions) {
    return (
      <Flex justify="center" align="center" py={10}>
        <Spinner size="xl" />
      </Flex>
    )
  }

  // Error state
  if (!quiz || !questions.length) {
    return (
      <Box p={5} borderRadius="md" borderWidth="1px" bg="red.50">
        <Text>Quiz not found or no questions available.</Text>
      </Box>
    )
  }

  // Start quiz view
  if (!attemptId) {
    return (
      <Container maxW="full" p={0}>
        <Card.Root p={6}>
          <Stack gap={6}>
            <Heading size="lg">{quiz.title}</Heading>

            {quiz.instructions && (
              <Box>
                <Heading size="sm" mb={2}>
                  Instructions
                </Heading>
                <Text>{quiz.instructions}</Text>
              </Box>
            )}

            <Box>
              <Heading size="sm" mb={2}>
                Questions
              </Heading>
              <Text>{questions.length} questions in this quiz</Text>
            </Box>

            <Flex justify="center">
              <Button
                onClick={startQuiz}
                loading={createAttemptMutation.isPending}
                size="lg"
              >
                Start Quiz
              </Button>
            </Flex>
          </Stack>
        </Card.Root>
      </Container>
    )
  }

  // Quiz taking view
  return (
    <Container maxW="full" p={0}>
      <Card.Root p={6}>
        <Stack gap={6}>
          <Flex justifyContent="space-between" alignItems="center">
            <Heading size="md">{quiz.title}</Heading>
            <Text>
              Question {currentQuestionIndex + 1} of {questions.length}
            </Text>
          </Flex>

          <Progress
            value={((currentQuestionIndex + 1) / questions.length) * 100}
            size="sm"
            borderRadius="md"
          />

          {currentQuestion && (
            <Box>
              <Heading size="sm" mb={4}>
                {currentQuestion.text}
              </Heading>

              {currentQuestion.question_type === "multiple_choice" ? (
                // Multiple choice input
                <RadioGroup
                  defaultValue={responses[currentQuestion.id]?.toString() || ""}
                  onChange={(e: string) => {
                    if (e) {
                      handleResponseChange(Number.parseInt(e))
                    }
                  }}
                >
                  <Stack gap={3}>
                    {isLoadingOptions ? (
                      <Spinner />
                    ) : (
                      options.map((option) => (
                        <Radio key={option.id} value={option.id.toString()}>
                          {option.text}
                        </Radio>
                      ))
                    )}
                  </Stack>
                </RadioGroup>
              ) : (
                // Text input for short/long answer
                <Textarea
                  value={(responses[currentQuestion.id] as string) || ""}
                  onChange={(e) => handleResponseChange(e.target.value)}
                  placeholder="Type your answer here..."
                  size="lg"
                  rows={6}
                />
              )}
            </Box>
          )}

          <Flex justify="space-between">
            <ChakraButton onClick={skipQuestion} variant="outline">
              {currentQuestionIndex < questions.length - 1
                ? "Skip"
                : "Complete Quiz"}
            </ChakraButton>

            <Button
              onClick={submitResponse}
              loading={submitResponseMutation.isPending}
            >
              {currentQuestionIndex < questions.length - 1
                ? "Next Question"
                : "Submit Quiz"}
            </Button>
          </Flex>
        </Stack>
      </Card.Root>
    </Container>
  )
}
