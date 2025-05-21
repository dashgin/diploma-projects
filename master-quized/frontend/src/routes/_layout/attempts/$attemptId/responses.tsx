import {
  Accordion,
  Badge,
  Box,
  Button,
  Card,
  CloseButton,
  Dialog,
  Flex,
  Heading,
  Portal,
  Separator,
  Text,
  useDisclosure,
} from "@chakra-ui/react"
import { Span } from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import React from "react"
import { AttemptsService, ResponsesService } from "../../../../client/sdk.gen"
import { FeedbackForm, FeedbackList } from "../../../../components/Feedback"

export const Route = createFileRoute("/_layout/attempts/$attemptId/responses")({
  component: AttemptResponsesPage,
})

function AttemptResponsesPage() {
  const { attemptId } = Route.useParams()
  const parsedAttemptId = Number.parseInt(attemptId, 10)
  const { open: isOpen, onOpen, onClose } = useDisclosure()
  const [selectedResponseId, setSelectedResponseId] = React.useState<
    number | null
  >(null)

  const { data: attempt, isLoading: attemptLoading } = useQuery({
    queryKey: ["attempt", parsedAttemptId],
    queryFn: () => AttemptsService.readAttempt({ attemptId: parsedAttemptId }),
    enabled: !Number.isNaN(parsedAttemptId),
  })

  const { data: responses, isLoading: responsesLoading } = useQuery({
    queryKey: ["responses", parsedAttemptId],
    queryFn: () =>
      ResponsesService.readResponsesByAttempt({ attemptId: parsedAttemptId }),
    enabled: !Number.isNaN(parsedAttemptId),
  })

  const handleAddFeedback = (responseId: number) => {
    setSelectedResponseId(responseId)
    onOpen()
  }

  if (attemptLoading || responsesLoading) {
    return <Box>Loading...</Box>
  }

  if (!attempt || !responses) {
    return <Box>No data found</Box>
  }

  return (
    <Box>
      <Card.Root mb={6}>
        <Card.Header>
          <Heading size="md">Quiz Attempt #{attempt.id}</Heading>
          <Text mt={2}>
            Score: {attempt.score !== null ? `${attempt.score}%` : "Not scored"}
          </Text>
          <Text>
            Status:{" "}
            <Badge colorScheme={attempt.is_completed ? "green" : "yellow"}>
              {attempt.is_completed ? "Completed" : "In Progress"}
            </Badge>
          </Text>
        </Card.Header>
      </Card.Root>

      <Heading size="md" mb={4}>
        Responses & Feedback
      </Heading>

      <Accordion.Root multiple>
        {responses.map((response) => (
          <Accordion.Item key={response.id} value={response.id.toString()}>
            <Accordion.ItemTrigger>
              <Span flex="1" textAlign="left">
                Question #{response.question_id}
              </Span>
              <Badge colorScheme={response.is_correct ? "green" : "red"} mr={2}>
                {response.is_correct ? "Correct" : "Incorrect"}
              </Badge>
              <Accordion.ItemIndicator />
            </Accordion.ItemTrigger>
            <Accordion.ItemContent>
              <Accordion.ItemBody>
                <Text fontWeight="bold" mb={2}>
                  Student Answer:
                </Text>
                <Text mb={4}>{response.answer_text}</Text>

                <Separator my={4} />

                <Flex justifyContent="space-between" alignItems="center" mb={4}>
                  <Heading size="sm">Feedback</Heading>
                  <Button
                    size="sm"
                    colorScheme="blue"
                    onClick={() => handleAddFeedback(response.id)}
                  >
                    Add Feedback
                  </Button>
                </Flex>

                <FeedbackList responseId={response.id} />
              </Accordion.ItemBody>
            </Accordion.ItemContent>
          </Accordion.Item>
        ))}
      </Accordion.Root>

      {/* Feedback Modal */}
      <Dialog.Root
        open={isOpen}
        onOpenChange={({ open }: { open: boolean }) => !open && onClose()}
        size="lg"
      >
        <Portal>
          <Dialog.Backdrop />
          <Dialog.Positioner>
            <Dialog.Content>
              <Dialog.Header>
                <Dialog.Title>Add Feedback</Dialog.Title>
                <Dialog.CloseTrigger asChild>
                  <CloseButton size="sm" />
                </Dialog.CloseTrigger>
              </Dialog.Header>
              <Dialog.Body pb={6}>
                {selectedResponseId && (
                  <FeedbackForm
                    responseId={selectedResponseId}
                    onSuccess={onClose}
                  />
                )}
              </Dialog.Body>
            </Dialog.Content>
          </Dialog.Positioner>
        </Portal>
      </Dialog.Root>
    </Box>
  )
}
