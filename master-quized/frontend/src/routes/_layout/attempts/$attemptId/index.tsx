import {
  Badge,
  Box,
  Button,
  Card,
  Center,
  CloseButton,
  Container,
  Dialog,
  Flex,
  Grid,
  GridItem,
  HStack,
  Heading,
  Portal,
  Progress,
  Separator,
  Spinner,
  Stack,
  Text,
  useDisclosure,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { OptionsService } from "../../../../client/sdk.gen"
import {
  AIFeedbackButton,
  AIFeedbackDisplay,
} from "../../../../components/Feedback"
import QuestionRenderer from "../../../../components/Quizzes/QuestionRenderer"
import { useQuizAttempt } from "../../../../hooks/useQuizAttempt"
import { formatDate } from "../../../../utils/formatters"

export const Route = createFileRoute("/_layout/attempts/$attemptId/")({
  component: AttemptPage,
})

function AttemptPage() {
  const { attemptId } = Route.useParams()
  const navigate = useNavigate()
  const disclosure = useDisclosure()

  const {
    attempt,
    questions,
    attemptResponsesData,
    currentQuestionIndex,
    isSubmitting,
    isLoading,
    handleResponseChange,
    handleNext,
    handlePrevious,
    handleQuestionSelect,
    handleSubmitQuiz,
    responses,
  } = useQuizAttempt(attemptId)

  // Fetch options for the current question
  const currentQuestionId = questions?.data?.[currentQuestionIndex]?.id
  const currentQuestionType =
    questions?.data?.[currentQuestionIndex]?.question_type

  const { data: optionsData, isLoading: isLoadingOptions } = useQuery({
    queryKey: ["options", currentQuestionId],
    queryFn: () =>
      OptionsService.readOptionsByQuestion({
        questionId: currentQuestionId || 0,
        limit: 20,
      }),
    enabled: !!currentQuestionId && currentQuestionType === "multiple_choice",
  })

  // Debug options data
  console.log("Current question type:", currentQuestionType)
  console.log("Options data:", optionsData)

  // Loading state
  if (isLoading) {
    return (
      <Center height="50vh">
        <Spinner size="xl" />
      </Center>
    )
  }

  // Check if attempt is already completed
  if (attempt?.is_completed) {
    const isLoadingCompletedAttemptData = !attemptResponsesData

    if (isLoadingCompletedAttemptData) {
      return (
        <Center height="50vh">
          <Spinner size="xl" />
        </Center>
      )
    }

    // Get attempt summary data
    const attemptSummary = attemptResponsesData?.attempt
    const responseDetails = attemptResponsesData?.responses || []

    // Create a map of responses by question ID for easier lookup
    const responsesByQuestionId: Record<number, any> = {}
    for (const response of responseDetails) {
      responsesByQuestionId[response.question.id] = response
    }

    return (
      <Container maxW="container.lg" py={8}>
        <Box mb={6}>
          <Flex justifyContent="space-between" alignItems="center">
            <Box>
              <Heading size="lg" color="gray.800" mb={1}>
                Quiz Results
              </Heading>
              <Text color="gray.600" fontSize="md">
                Review your performance and learn from the feedback
              </Text>
            </Box>
            <Button
              onClick={() => navigate({ to: `/quizzes/${attempt.quiz_id}` })}
              variant="outline"
              size="md"
            >
              ← Return to Quiz
            </Button>
          </Flex>

          <Card.Root variant="outline" mt={4}>
            <Card.Body p={6}>
              <Flex
                direction={{ base: "column", md: "row" }}
                align="center"
                justify="space-between"
                gap={6}
              >
                <Box textAlign={{ base: "center", md: "left" }}>
                  <Flex
                    align="center"
                    gap={3}
                    mb={2}
                    justify={{ base: "center", md: "flex-start" }}
                  >
                    <Text fontSize="3xl" fontWeight="bold" color="gray.800">
                      {attemptSummary?.score !== undefined
                        ? `${Math.round(attemptSummary.score)}%`
                        : "Not scored"}
                    </Text>
                    <Box
                      bg={
                        (attemptSummary?.score ?? 0) >= 70
                          ? "green.500"
                          : "orange.500"
                      }
                      color="white"
                      px={4}
                      py={2}
                      borderRadius="full"
                      fontSize="xs"
                      fontWeight="bold"
                      textTransform="uppercase"
                      letterSpacing="wide"
                      shadow="sm"
                    >
                      {(attemptSummary?.score ?? 0) >= 70
                        ? "✓ Passed"
                        : "⚠ Needs Review"}
                    </Box>
                  </Flex>
                  <Text color="gray.600" fontSize="sm">
                    Final Score
                  </Text>
                </Box>

                <Grid
                  templateColumns="repeat(3, 1fr)"
                  gap={6}
                  textAlign="center"
                >
                  <Box>
                    <Text fontSize="2xl" fontWeight="bold" color="gray.800">
                      {attemptSummary?.total_questions || 0}
                    </Text>
                    <Text fontSize="sm" color="gray.600">
                      Total
                    </Text>
                  </Box>
                  <Box>
                    <Text fontSize="2xl" fontWeight="bold" color="gray.800">
                      {attemptSummary?.correct_answers || 0}
                    </Text>
                    <Text fontSize="sm" color="gray.600">
                      Correct
                    </Text>
                  </Box>
                  <Box>
                    <Text fontSize="2xl" fontWeight="bold" color="gray.800">
                      {(attemptSummary?.total_questions || 0) -
                        (attemptSummary?.correct_answers || 0)}
                    </Text>
                    <Text fontSize="sm" color="gray.600">
                      Wrong
                    </Text>
                  </Box>
                </Grid>
              </Flex>

              <Separator my={4} />

              <Grid
                templateColumns={{ base: "1fr", md: "repeat(3, 1fr)" }}
                gap={4}
                fontSize="sm"
                color="gray.600"
              >
                <Text>
                  <Text as="span" fontWeight="medium">
                    Started:
                  </Text>{" "}
                  {formatDate(attempt.started_at)}
                </Text>
                <Text>
                  <Text as="span" fontWeight="medium">
                    Completed:
                  </Text>{" "}
                  {formatDate(attempt.completed_at)}
                </Text>
                <Text>
                  <Text as="span" fontWeight="medium">
                    Duration:
                  </Text>{" "}
                  {(() => {
                    if (attempt.started_at && attempt.completed_at) {
                      const duration =
                        new Date(attempt.completed_at).getTime() -
                        new Date(attempt.started_at).getTime()
                      const minutes = Math.floor(duration / 60000)
                      const seconds = Math.floor((duration % 60000) / 1000)
                      return `${minutes}m ${seconds}s`
                    }
                    return "N/A"
                  })()}
                </Text>
              </Grid>
            </Card.Body>
          </Card.Root>
        </Box>

        <Separator my={6} />

        <Box>
          <Box mb={6}>
            <Heading size="md" color="gray.800" mb={2}>
              Question Review
            </Heading>
            <Text color="gray.600" fontSize="sm">
              {attemptSummary?.correct_answers || 0} of{" "}
              {attemptSummary?.total_questions || 0} questions answered
              correctly
            </Text>
          </Box>

          {questions?.data.map((question, index) => {
            const responseData = responsesByQuestionId[question.id]
            const isCorrect = responseData?.answer?.is_correct

            return (
              <Card.Root key={question.id} mb={3} variant="outline">
                <Card.Header
                  p={4}
                  borderBottom="1px solid"
                  borderBottomColor="gray.200"
                >
                  <Flex justify="space-between" align="center">
                    <Flex align="center" gap={3}>
                      <Text fontWeight="bold" fontSize="lg" color="gray.800">
                        Question {index + 1}
                      </Text>
                      <Box
                        bg={
                          isCorrect === true
                            ? "green.100"
                            : isCorrect === false
                              ? "red.100"
                              : "gray.100"
                        }
                        color={
                          isCorrect === true
                            ? "green.800"
                            : isCorrect === false
                              ? "red.800"
                              : "gray.700"
                        }
                        px={3}
                        py={1}
                        borderRadius="md"
                        fontSize="xs"
                        fontWeight="semibold"
                        border="1px solid"
                        borderColor={
                          isCorrect === true
                            ? "green.300"
                            : isCorrect === false
                              ? "red.300"
                              : "gray.300"
                        }
                      >
                        {isCorrect === true
                          ? "✓ Correct"
                          : isCorrect === false
                            ? "✗ Incorrect"
                            : "• Not Scored"}
                      </Box>
                    </Flex>

                    <Flex align="center" gap={2}>
                      <Text fontSize="sm" color="gray.500">
                        {index + 1} of {questions?.data.length || 0}
                      </Text>
                      <Box
                        w="8px"
                        h="8px"
                        borderRadius="full"
                        bg={
                          isCorrect === true
                            ? "green.400"
                            : isCorrect === false
                              ? "red.400"
                              : "gray.400"
                        }
                      />
                    </Flex>
                  </Flex>
                </Card.Header>
                <Card.Body p={3}>
                  <Box mb={3}>
                    <Text fontSize="md" lineHeight="1.6" color="gray.800">
                      {question.text}
                    </Text>
                  </Box>

                  <Grid
                    templateColumns={{ base: "1fr", lg: "1fr 1fr" }}
                    gap={4}
                  >
                    {/* Your Answer */}
                    <Box>
                      <Box
                        p={4}
                        bg={
                          isCorrect === true
                            ? "green.50"
                            : isCorrect === false
                              ? "red.50"
                              : "gray.50"
                        }
                        borderRadius="lg"
                        border="2px solid"
                        borderColor={
                          isCorrect === true
                            ? "green.200"
                            : isCorrect === false
                              ? "red.200"
                              : "gray.200"
                        }
                      >
                        {(() => {
                          // Handle multiple choice questions
                          if (
                            responseData?.question?.question_type ===
                              "multiple_choice" ||
                            responseData?.question?.question_type ===
                              "multiple_answer"
                          ) {
                            // Handle multiple answers (array of selections)
                            if (Array.isArray(responseData.answer?.answer)) {
                              const selectedOptions = responseData.answer.answer
                                .map((answerId: any) => {
                                  return responseData.question.options?.find(
                                    (opt: any) =>
                                      opt.id.toString() === answerId.toString(),
                                  )
                                })
                                .filter(Boolean)

                              if (selectedOptions.length > 0) {
                                return (
                                  <Stack gap={2}>
                                    {selectedOptions.map(
                                      (option: any, idx: number) => {
                                        const optionIndex =
                                          responseData.question.options.findIndex(
                                            (opt: any) => opt.id === option.id,
                                          )
                                        return (
                                          <Flex
                                            key={option.id}
                                            align="center"
                                            gap={3}
                                          >
                                            <Box
                                              bg={
                                                option.is_correct
                                                  ? "green.500"
                                                  : "red.500"
                                              }
                                              color="white"
                                              borderRadius="full"
                                              w="24px"
                                              h="24px"
                                              display="flex"
                                              alignItems="center"
                                              justifyContent="center"
                                              fontSize="xs"
                                              fontWeight="bold"
                                              flexShrink={0}
                                            >
                                              {String.fromCharCode(
                                                65 + optionIndex,
                                              )}
                                            </Box>
                                            <Text
                                              fontSize="md"
                                              fontWeight="semibold"
                                              color={
                                                option.is_correct
                                                  ? "green.800"
                                                  : "red.800"
                                              }
                                            >
                                              {option.text}
                                            </Text>
                                            <Badge
                                              size="sm"
                                              colorScheme={
                                                option.is_correct
                                                  ? "green"
                                                  : "red"
                                              }
                                              variant="solid"
                                            >
                                              {option.is_correct ? "✓" : "✗"}
                                            </Badge>
                                          </Flex>
                                        )
                                      },
                                    )}
                                  </Stack>
                                )
                              }
                            }

                            // Handle single answer with object format
                            if (
                              typeof responseData.answer?.answer === "object" &&
                              responseData.answer.answer?.text
                            ) {
                              const optionIndex =
                                responseData.question.options?.findIndex(
                                  (opt: any) =>
                                    opt.id ===
                                    responseData.answer.answer?.option_id,
                                )
                              return (
                                <Flex align="center" gap={3}>
                                  <Box
                                    bg={
                                      isCorrect === true
                                        ? "green.500"
                                        : "red.500"
                                    }
                                    color="white"
                                    borderRadius="full"
                                    w="24px"
                                    h="24px"
                                    display="flex"
                                    alignItems="center"
                                    justifyContent="center"
                                    fontSize="xs"
                                    fontWeight="bold"
                                    flexShrink={0}
                                  >
                                    {optionIndex !== -1
                                      ? String.fromCharCode(65 + optionIndex)
                                      : "?"}
                                  </Box>
                                  <Text
                                    fontSize="md"
                                    fontWeight="semibold"
                                    color={
                                      isCorrect === true
                                        ? "green.800"
                                        : isCorrect === false
                                          ? "red.800"
                                          : "gray.700"
                                    }
                                  >
                                    {responseData.answer.answer.text}
                                  </Text>
                                </Flex>
                              )
                            }

                            // Handle single answer with option ID
                            if (
                              responseData.answer?.answer &&
                              responseData.question?.options
                            ) {
                              const selectedOption =
                                responseData.question.options.find(
                                  (opt: any) =>
                                    opt.id.toString() ===
                                    responseData.answer.answer.toString(),
                                )
                              if (selectedOption) {
                                const optionIndex =
                                  responseData.question.options.findIndex(
                                    (opt: any) => opt.id === selectedOption.id,
                                  )
                                return (
                                  <Flex align="center" gap={3}>
                                    <Box
                                      bg={
                                        isCorrect === true
                                          ? "green.500"
                                          : "red.500"
                                      }
                                      color="white"
                                      borderRadius="full"
                                      w="24px"
                                      h="24px"
                                      display="flex"
                                      alignItems="center"
                                      justifyContent="center"
                                      fontSize="xs"
                                      fontWeight="bold"
                                      flexShrink={0}
                                    >
                                      {String.fromCharCode(65 + optionIndex)}
                                    </Box>
                                    <Text
                                      fontSize="md"
                                      fontWeight="semibold"
                                      color={
                                        isCorrect === true
                                          ? "green.800"
                                          : isCorrect === false
                                            ? "red.800"
                                            : "gray.700"
                                      }
                                    >
                                      {selectedOption.text}
                                    </Text>
                                  </Flex>
                                )
                              }
                            }
                          }

                          // For non-multiple choice or fallback
                          return (
                            <Text
                              fontSize="md"
                              fontWeight="semibold"
                              color={
                                isCorrect === true
                                  ? "green.800"
                                  : isCorrect === false
                                    ? "red.800"
                                    : "gray.700"
                              }
                            >
                              {responseData?.answer?.answer || "Not answered"}
                            </Text>
                          )
                        })()}
                      </Box>
                    </Box>

                    {/* All Options for Multiple Choice */}
                    {responseData?.question?.question_type ===
                      "multiple_choice" &&
                      responseData.question.options && (
                        <Box>
                          <Text
                            fontWeight="bold"
                            fontSize="md"
                            color="gray.700"
                            mb={3}
                          >
                            All Options
                          </Text>
                          <Stack gap={2}>
                            {responseData.question.options.map(
                              (option: any, idx: number) => {
                                // Check if this option is the user's answer
                                const isUserAnswer = (() => {
                                  // Handle multiple answers (array)
                                  if (
                                    Array.isArray(responseData.answer?.answer)
                                  ) {
                                    return responseData.answer.answer.some(
                                      (answerId: any) =>
                                        answerId.toString() ===
                                        option.id.toString(),
                                    )
                                  }
                                  // Handle single answer with object format
                                  if (
                                    typeof responseData.answer?.answer ===
                                    "object"
                                  ) {
                                    return (
                                      responseData.answer.answer?.option_id ===
                                      option.id
                                    )
                                  }
                                  // Handle case where answer is stored as option ID
                                  return (
                                    responseData.answer?.answer?.toString() ===
                                    option.id.toString()
                                  )
                                })()
                                const isCorrectOption = option.is_correct

                                return (
                                  <Flex
                                    key={idx}
                                    align="center"
                                    gap={3}
                                    p={3}
                                    bg={
                                      isCorrectOption
                                        ? "green.50"
                                        : isUserAnswer
                                          ? "red.50"
                                          : "white"
                                    }
                                    borderRadius="md"
                                    border="2px solid"
                                    borderColor={
                                      isCorrectOption
                                        ? "green.300"
                                        : isUserAnswer
                                          ? "red.300"
                                          : "gray.200"
                                    }
                                  >
                                    <Box minW="32px" textAlign="center">
                                      {isCorrectOption && (
                                        <Box
                                          bg="green.500"
                                          color="white"
                                          borderRadius="full"
                                          w="24px"
                                          h="24px"
                                          display="flex"
                                          alignItems="center"
                                          justifyContent="center"
                                          fontSize="sm"
                                          fontWeight="bold"
                                        >
                                          ✓
                                        </Box>
                                      )}
                                      {isUserAnswer && !isCorrectOption && (
                                        <Box
                                          bg="red.500"
                                          color="white"
                                          borderRadius="full"
                                          w="24px"
                                          h="24px"
                                          display="flex"
                                          alignItems="center"
                                          justifyContent="center"
                                          fontSize="sm"
                                          fontWeight="bold"
                                        >
                                          ✗
                                        </Box>
                                      )}
                                      {!isCorrectOption && !isUserAnswer && (
                                        <Box
                                          bg="gray.300"
                                          borderRadius="full"
                                          w="24px"
                                          h="24px"
                                          display="flex"
                                          alignItems="center"
                                          justifyContent="center"
                                          fontSize="sm"
                                          color="gray.600"
                                        >
                                          {String.fromCharCode(65 + idx)}
                                        </Box>
                                      )}
                                    </Box>
                                    <Text
                                      fontSize="md"
                                      fontWeight={
                                        isCorrectOption || isUserAnswer
                                          ? "semibold"
                                          : "normal"
                                      }
                                      flex="1"
                                      color={
                                        isCorrectOption
                                          ? "green.800"
                                          : isUserAnswer
                                            ? "red.800"
                                            : "gray.700"
                                      }
                                    >
                                      {option.text}
                                    </Text>
                                    {isCorrectOption && (
                                      <Badge
                                        colorScheme="green"
                                        variant="solid"
                                        size="sm"
                                      >
                                        CORRECT
                                      </Badge>
                                    )}
                                    {isUserAnswer && !isCorrectOption && (
                                      <Badge
                                        colorScheme="red"
                                        variant="solid"
                                        size="sm"
                                      >
                                        YOUR ANSWER
                                      </Badge>
                                    )}
                                  </Flex>
                                )
                              },
                            )}
                          </Stack>
                        </Box>
                      )}
                  </Grid>

                  {/* Learning Resources - Compact Layout */}
                  <Stack align="stretch" gap={3} mt={4}>
                    {/* Model Answer for open-ended questions */}
                    {(responseData?.question?.question_type === "open_ended" ||
                      responseData?.question?.question_type === "text" ||
                      responseData?.question?.question_type === "essay" ||
                      responseData?.question?.question_type === "short_answer") &&
                      responseData?.question?.model_answer && (
                        <Box
                          p={4}
                          bg="gradient-to-r"
                          bgGradient="linear(to-r, green.50, teal.50)"
                          borderRadius="lg"
                          border="1px solid"
                          borderColor="green.200"
                        >
                          <Flex align="center" gap={2} mb={3}>
                            <Box
                              bg="green.500"
                              color="white"
                              borderRadius="full"
                              w="24px"
                              h="24px"
                              display="flex"
                              alignItems="center"
                              justifyContent="center"
                              fontSize="sm"
                            >
                              ✨
                            </Box>
                            <Text fontWeight="bold" fontSize="md" color="green.800">
                              Model Answer
                            </Text>
                          </Flex>
                          <Box
                            p={3}
                            bg="white"
                            borderRadius="md"
                            border="1px solid"
                            borderColor="green.200"
                          >
                            <Text
                              color="green.800"
                              lineHeight="1.6"
                              fontSize="sm"
                              fontWeight="medium"
                            >
                              {responseData.question.model_answer}
                            </Text>
                          </Box>
                        </Box>
                      )}

                    {/* Explanation */}
                    {responseData?.explanation && (
                      <Box
                        p={4}
                        bg="blue.50"
                        borderRadius="lg"
                        border="1px solid"
                        borderColor="blue.200"
                      >
                        <Flex align="center" gap={2} mb={3}>
                          <Box
                            bg="blue.500"
                            color="white"
                            borderRadius="full"
                            w="24px"
                            h="24px"
                            display="flex"
                            alignItems="center"
                            justifyContent="center"
                            fontSize="sm"
                          >
                            💡
                          </Box>
                          <Text fontWeight="bold" fontSize="md" color="blue.800">
                            Explanation
                          </Text>
                        </Flex>
                        <Text color="blue.700" lineHeight="1.6" fontSize="sm">
                          {responseData.explanation}
                        </Text>
                      </Box>
                    )}

                    {/* AI Feedback section - for text-based and subjective questions */}
                    {(responseData?.question?.question_type === "open_ended" ||
                      responseData?.question?.question_type === "text" ||
                      responseData?.question?.question_type === "essay" ||
                      responseData?.question?.question_type === "short_answer") && (
                      <Box
                        p={4}
                        bg="gradient-to-r"
                        bgGradient="linear(to-r, purple.50, blue.50)"
                        borderRadius="lg"
                        border="1px solid"
                        borderColor="purple.200"
                      >
                        <Flex
                          justifyContent="space-between"
                          alignItems="center"
                          mb={3}
                        >
                          <Flex align="center" gap={2}>
                            <Box
                              bg="purple.500"
                              color="white"
                              borderRadius="full"
                              w="24px"
                              h="24px"
                              display="flex"
                              alignItems="center"
                              justifyContent="center"
                              fontSize="sm"
                            >
                              🤖
                            </Box>
                            <Text
                              fontWeight="bold"
                              fontSize="md"
                              color="purple.800"
                            >
                              AI Feedback
                            </Text>
                          </Flex>
                          <AIFeedbackButton responseId={responseData.id} />
                        </Flex>
                        <AIFeedbackDisplay responseId={responseData.id} />
                      </Box>
                    )}

                    {/* AI Feedback for Multiple Choice with detailed explanations */}
                    {responseData?.question?.question_type === "multiple_choice" &&
                      isCorrect === false && (
                        <Box
                          p={4}
                          bg="gradient-to-r"
                          bgGradient="linear(to-r, orange.50, red.50)"
                          borderRadius="lg"
                          border="1px solid"
                          borderColor="orange.200"
                        >
                          <Flex align="center" gap={2} mb={3}>
                            <Box
                              bg="orange.500"
                              color="white"
                              borderRadius="full"
                              w="24px"
                              h="24px"
                              display="flex"
                              alignItems="center"
                              justifyContent="center"
                              fontSize="sm"
                            >
                              💡
                            </Box>
                            <Text
                              fontWeight="bold"
                              fontSize="md"
                              color="orange.800"
                            >
                              Learning Insights
                            </Text>
                          </Flex>
                          <Box
                            p={3}
                            bg="white"
                            borderRadius="md"
                            border="1px solid"
                            borderColor="orange.200"
                          >
                            <Text color="orange.800" lineHeight="1.6" fontSize="sm">
                              <Text as="span" fontWeight="bold">Study Tip:</Text> You selected an incorrect option. 
                              Review the key concepts and consider why the correct answer is more appropriate.
                            </Text>
                            {responseData?.explanation && (
                              <Box mt={2} p={2} bg="orange.50" borderRadius="sm">
                                <Text fontSize="xs" fontStyle="italic" color="orange.700">
                                  💡 {responseData.explanation}
                                </Text>
                              </Box>
                            )}
                          </Box>
                        </Box>
                      )}
                  </Stack>
                </Card.Body>
              </Card.Root>
            )
          })}
        </Box>
      </Container>
    )
  }

  // Current question
  const currentQuestion = questions?.data?.[currentQuestionIndex]
  // Ensure we handle the nested data structure correctly
  const questionOptions = optionsData?.data || []
  console.log("Processed question options:", questionOptions)
  const totalQuestions = questions?.data.length || 0
  const progress = totalQuestions
    ? ((currentQuestionIndex + 1) / totalQuestions) * 100
    : 0

  // If no questions are available, show an error state
  if (!isLoading && (!questions?.data || questions.data.length === 0)) {
    return (
      <Container maxW="container.lg" py={8}>
        <Box textAlign="center">
          <Heading size="lg" mb={4}>
            No Questions Available
          </Heading>
          <Text mb={4}>This quiz doesn't have any questions yet.</Text>
          <Button
            onClick={() => navigate({ to: `/quizzes/${attempt?.quiz_id}` })}
            variant="outline"
          >
            Return to Quiz
          </Button>
        </Box>
      </Container>
    )
  }

  // If current question is not available, reset to first question
  if (!isLoading && currentQuestion === undefined && totalQuestions > 0) {
    return (
      <Center height="50vh">
        <Spinner size="xl" />
      </Center>
    )
  }

  return (
    <Container maxW="container.xl" py={4}>
      {/* Quiz Header */}
      <Flex justifyContent="space-between" alignItems="center" mb={4}>
        <Heading size="md">Quiz Attempt</Heading>
        <Button colorScheme="blue" onClick={disclosure.onOpen}>
          Submit Quiz
        </Button>
      </Flex>

      {/* Progress Bar */}
      <Box mb={6}>
        <Progress.Root
          size="sm"
          colorScheme="blue"
          borderRadius="md"
          value={progress}
        >
          <Progress.Track>
            <Progress.Range />
          </Progress.Track>
        </Progress.Root>
        <Text mt={1} fontSize="sm">
          Question {currentQuestionIndex + 1} of {totalQuestions}
        </Text>
      </Box>

      {/* Main Content */}
      <Grid templateColumns={{ base: "1fr", md: "1fr 3fr" }} gap={6}>
        {/* Question Navigator */}
        <GridItem>
          <Box
            p={4}
            borderWidth="1px"
            borderRadius="md"
            height="fit-content"
            position="sticky"
            top="4"
          >
            <Heading size="sm" mb={4}>
              Questions
            </Heading>
            <Stack direction="column" gap={2}>
              {questions?.data.map((question, index) => (
                <Button
                  key={question.id}
                  variant={index === currentQuestionIndex ? "solid" : "outline"}
                  colorScheme={
                    index === currentQuestionIndex
                      ? "blue"
                      : responses[question.id]
                        ? "green"
                        : "gray"
                  }
                  justifyContent="flex-start"
                  size="sm"
                  onClick={() => handleQuestionSelect(index)}
                >
                  {index + 1}.{" "}
                  {question.text.length > 20
                    ? `${question.text.substring(0, 20)}...`
                    : question.text}
                </Button>
              ))}
            </Stack>
          </Box>
        </GridItem>

        {/* Question Content */}
        <GridItem>
          {isLoadingOptions ? (
            <Center py={10}>
              <Spinner />
            </Center>
          ) : (
            <Box p={6} borderWidth="1px" borderRadius="md">
              <Heading size="md" mb={4}>
                {currentQuestion?.text}
              </Heading>

              {/* Question Type Renderer */}
              {currentQuestion && (
                <QuestionRenderer
                  questionType={currentQuestion.question_type}
                  questionId={currentQuestion.id}
                  options={
                    currentQuestion.question_type === "multiple_choice"
                      ? questionOptions
                      : []
                  }
                  value={responses[currentQuestion.id] || ""}
                  onChange={handleResponseChange}
                />
              )}

              {/* Navigation Buttons */}
              <HStack mt={8} justifyContent="space-between">
                <Button
                  onClick={handlePrevious}
                  disabled={currentQuestionIndex === 0}
                >
                  Previous
                </Button>
                <Button
                  onClick={handleNext}
                  disabled={currentQuestionIndex === totalQuestions - 1}
                  colorScheme="blue"
                >
                  Next
                </Button>
              </HStack>
            </Box>
          )}
        </GridItem>
      </Grid>

      {/* Submit Confirmation Dialog */}
      <Dialog.Root
        open={disclosure.open}
        onOpenChange={(e) => disclosure.setOpen(e.open)}
      >
        <Portal>
          <Dialog.Backdrop />
          <Dialog.Positioner>
            <Dialog.Content>
              <Dialog.Header>
                <Dialog.Title>Submit Quiz</Dialog.Title>
                <Dialog.CloseTrigger asChild>
                  <CloseButton size="sm" />
                </Dialog.CloseTrigger>
              </Dialog.Header>
              <Dialog.Body>
                <Text>
                  Are you sure you want to submit this quiz? You won't be able
                  to change your answers after submission.
                </Text>

                {/* Response status */}
                {totalQuestions > 0 && (
                  <Box mt={4}>
                    <Text fontWeight="medium">Question Status:</Text>
                    <Text>
                      {Object.keys(responses).length} of {totalQuestions}{" "}
                      questions answered
                    </Text>
                    {Object.keys(responses).length < totalQuestions && (
                      <Text color="orange.500" mt={1}>
                        You have unanswered questions.
                      </Text>
                    )}
                  </Box>
                )}
              </Dialog.Body>
              <Dialog.Footer>
                <Button
                  colorScheme="blue"
                  onClick={handleSubmitQuiz}
                  loading={isSubmitting}
                >
                  Submit Quiz
                </Button>
              </Dialog.Footer>
            </Dialog.Content>
          </Dialog.Positioner>
        </Portal>
      </Dialog.Root>
    </Container>
  )
}
