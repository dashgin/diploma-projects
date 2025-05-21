import {
  Badge,
  Box,
  Button,
  Card,
  Container,
  Flex,
  Heading,
  Spinner,
  Stack,
  Text,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"

import {
  AttemptsService,
  QuestionsService,
  QuizzesService,
  ResponsesService,
} from "@/client"
import { formatDate, formatScore } from "@/utils/formatters"

interface AttemptDetailsProps {
  attemptId: number
}

export function AttemptDetails({ attemptId }: AttemptDetailsProps) {
  // Fetch attempt details
  const { data: attempt, isLoading: isLoadingAttempt } = useQuery({
    queryKey: ["attempts", attemptId],
    queryFn: () => AttemptsService.readAttempt({ attemptId }),
  })

  // Fetch quiz details
  const { data: quiz, isLoading: isLoadingQuiz } = useQuery({
    queryKey: ["quizzes", attempt?.quiz_id],
    queryFn: () => QuizzesService.readQuiz({ quizId: attempt?.quiz_id ?? 0 }),
    enabled: !!attempt?.quiz_id,
  })

  // Fetch questions
  const { data: questionsData, isLoading: isLoadingQuestions } = useQuery({
    queryKey: ["questions", attempt?.quiz_id],
    queryFn: () =>
      QuestionsService.readQuestionsByQuiz({
        quizId: attempt?.quiz_id ?? 0,
      }),
    enabled: !!attempt?.quiz_id,
  })

  // Fetch responses
  const { data: responsesList, isLoading: isLoadingResponses } = useQuery({
    queryKey: ["responses", attemptId],
    queryFn: () =>
      ResponsesService.readResponsesByAttempt({
        attemptId,
        skip: 0,
        limit: 100,
      }),
    enabled: !!attemptId,
  })

  const questions = questionsData?.data || []
  const responses = responsesList || []

  // Loading state
  if (
    isLoadingAttempt ||
    isLoadingQuiz ||
    isLoadingQuestions ||
    isLoadingResponses
  ) {
    return (
      <Flex justify="center" align="center" py={10}>
        <Spinner size="xl" />
      </Flex>
    )
  }

  // Error state
  if (!attempt || !quiz) {
    return (
      <Box p={5} borderRadius="md" borderWidth="1px" bg="red.50">
        <Text>Attempt not found or you don't have permission to view it.</Text>
      </Box>
    )
  }

  return (
    <Container maxW="full" p={0}>
      <Card.Root p={6} mb={6}>
        <Stack gap={4}>
          <Flex justifyContent="space-between" alignItems="center">
            <Heading size="md">Quiz Attempt #{attempt.id}</Heading>
            <Badge
              colorScheme={attempt.is_completed ? "green" : "yellow"}
              fontSize="md"
              py={1}
              px={2}
              borderRadius="md"
            >
              {attempt.is_completed ? "Completed" : "In Progress"}
            </Badge>
          </Flex>

          <Box h="1px" bg="gray.200" />

          <Box>
            <Heading size="sm" mb={2}>
              Quiz
            </Heading>
            <Text fontWeight="medium">{quiz.title}</Text>
          </Box>

          <Stack direction="row" gap={8}>
            <Box>
              <Heading size="sm" mb={2}>
                Score
              </Heading>
              <Text fontWeight="medium">
                {attempt.is_completed
                  ? formatScore(attempt.score)
                  : "Not completed"}
              </Text>
            </Box>

            <Box>
              <Heading size="sm" mb={2}>
                Completion Date
              </Heading>
              <Text fontWeight="medium">
                {attempt.completed_at
                  ? formatDate(attempt.completed_at)
                  : "Not completed"}
              </Text>
            </Box>
          </Stack>
        </Stack>
      </Card.Root>

      <Card.Root p={6}>
        <Flex justifyContent="space-between" alignItems="center" mb={4}>
          <Heading size="md">Responses</Heading>
          {responses.length > 0 && (
            <Link to={`/attempts/${attemptId}/responses`}>
              <Button colorScheme="blue" size="sm">
                View Feedback & Resources
              </Button>
            </Link>
          )}
        </Flex>

        {responses.length === 0 ? (
          <Text>No responses recorded for this attempt.</Text>
        ) : (
          <Stack gap={6}>
            {questions.map((question) => {
              const response = responses.find(
                (r) => r.question_id === question.id,
              )

              return (
                <Box
                  key={question.id}
                  p={4}
                  borderWidth="1px"
                  borderRadius="md"
                  borderColor="gray.200"
                >
                  <Heading size="sm" mb={2}>
                    {question.text}
                  </Heading>

                  {response ? (
                    <Box>
                      <Text fontWeight="bold" mb={1}>
                        Your Answer:
                      </Text>
                      <Text mb={3}>{response.answer_text}</Text>

                      {response.is_correct !== null && (
                        <Badge
                          colorScheme={response.is_correct ? "green" : "red"}
                          mb={2}
                        >
                          {response.is_correct ? "Correct" : "Incorrect"}
                        </Badge>
                      )}

                      {question.model_answer && (
                        <Box mt={2}>
                          <Text fontWeight="bold" mb={1}>
                            Correct Answer:
                          </Text>
                          <Text>{question.model_answer}</Text>
                        </Box>
                      )}
                    </Box>
                  ) : (
                    <Text color="gray.500">No response recorded</Text>
                  )}
                </Box>
              )
            })}
          </Stack>
        )}
      </Card.Root>
    </Container>
  )
}
