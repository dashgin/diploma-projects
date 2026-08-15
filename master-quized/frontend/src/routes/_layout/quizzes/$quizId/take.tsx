import {
  Alert,
  Box,
  Button,
  Card,
  Center,
  CloseButton,
  Dialog,
  Heading,
  Portal,
  Spinner,
  Stack,
  Text,
  useDisclosure,
} from "@chakra-ui/react"
import { useMutation, useQuery } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { AttemptsService, QuizzesService } from "../../../../client/sdk.gen"

export const Route = createFileRoute("/_layout/quizzes/$quizId/take")({
  component: QuizTakePage,
})

function QuizTakePage() {
  const { quizId } = Route.useParams()
  const navigate = useNavigate()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const disclosure = useDisclosure()

  // Fetch quiz details
  const {
    data: quiz,
    isLoading: isLoadingQuiz,
    error: quizError,
  } = useQuery({
    queryKey: ["quiz", quizId],
    queryFn: () => QuizzesService.readQuiz({ quizId: Number(quizId) }),
  })

  // Create attempt mutation
  const createAttemptMutation = useMutation({
    mutationFn: () => {
      setIsSubmitting(true)
      return AttemptsService.createAttempt({
        requestBody: {
          quiz_id: Number(quizId),
          is_completed: false,
        },
      })
    },
    onSuccess: (data) => {
      setIsSubmitting(false)
      navigate({ to: `/attempts/${data.id}` })
    },
    onError: (error) => {
      setIsSubmitting(false)
      console.error("Error creating attempt:", error)
    },
  })

  // Handle start quiz
  const handleStartQuiz = () => {
    createAttemptMutation.mutate()
  }

  if (isLoadingQuiz) {
    return (
      <Center h="50vh">
        <Spinner size="xl" />
      </Center>
    )
  }

  if (quizError) {
    return (
      <Alert.Root status="error" borderRadius="md">
        <Alert.Description>
          There was an error loading this quiz. Please try again later.
        </Alert.Description>
      </Alert.Root>
    )
  }

  return (
    <Stack
      direction="column"
      gap={6}
      align="stretch"
      w="full"
      maxW="800px"
      mx="auto"
      py={8}
    >
      <Heading as="h1" size="xl">
        {quiz?.title}
      </Heading>

      <Card.Root>
        <Card.Body>
          <Stack direction="column" gap={4} align="start">
            <Heading as="h2" size="md">
              Instructions
            </Heading>
            <Text>
              {quiz?.instructions ||
                "No specific instructions provided for this quiz."}
            </Text>

            <Box borderTop="1px" borderColor="gray.200" pt={4} width="100%">
              <Text fontWeight="bold">Before you begin:</Text>
              <Text>• Make sure you have enough time to complete the quiz</Text>
              <Text>
                • Your answers will be saved automatically as you progress
              </Text>
              <Text>• You can navigate between questions freely</Text>
              <Text>• Submit your quiz when you're finished</Text>
            </Box>
          </Stack>
        </Card.Body>
        <Card.Footer justifyContent="center">
          <Button
            colorScheme="blue"
            onClick={disclosure.onOpen}
            size="lg"
            loading={isSubmitting}
          >
            Start Quiz
          </Button>
        </Card.Footer>
      </Card.Root>

      {/* Confirmation Dialog */}
      <Dialog.Root
        open={disclosure.open}
        onOpenChange={(e) => disclosure.setOpen(e.open)}
      >
        <Portal>
          <Dialog.Backdrop />
          <Dialog.Positioner>
            <Dialog.Content>
              <Dialog.Header>
                <Dialog.Title>Start Quiz</Dialog.Title>
                <Dialog.CloseTrigger asChild>
                  <CloseButton size="sm" />
                </Dialog.CloseTrigger>
              </Dialog.Header>
              <Dialog.Body>
                Are you ready to start this quiz? Once started, your attempt
                will be recorded.
              </Dialog.Body>
              <Dialog.Footer>
                <Button
                  colorScheme="blue"
                  onClick={handleStartQuiz}
                  loading={isSubmitting}
                >
                  Start Now
                </Button>
              </Dialog.Footer>
            </Dialog.Content>
          </Dialog.Positioner>
        </Portal>
      </Dialog.Root>
    </Stack>
  )
}
