import {
  Accordion,
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Badge,
  Box,
  Button,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Flex,
  Heading,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Text,
  useDisclosure,
} from "@chakra-ui/react"
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
  const { isOpen, onOpen, onClose } = useDisclosure()
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
      <Card mb={6}>
        <CardHeader>
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
        </CardHeader>
      </Card>

      <Heading size="md" mb={4}>
        Responses & Feedback
      </Heading>

      <Accordion allowMultiple>
        {responses.map((response) => (
          <AccordionItem key={response.id}>
            <h2>
              <AccordionButton>
                <Box flex="1" textAlign="left">
                  Question #{response.question_id}
                </Box>
                <Badge
                  colorScheme={response.is_correct ? "green" : "red"}
                  mr={2}
                >
                  {response.is_correct ? "Correct" : "Incorrect"}
                </Badge>
                <AccordionIcon />
              </AccordionButton>
            </h2>
            <AccordionPanel pb={4}>
              <Text fontWeight="bold" mb={2}>
                Student Answer:
              </Text>
              <Text mb={4}>{response.answer_text}</Text>

              <Divider my={4} />

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
            </AccordionPanel>
          </AccordionItem>
        ))}
      </Accordion>

      {/* Feedback Modal */}
      <Modal isOpen={isOpen} onClose={onClose} size="lg">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Add Feedback</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            {selectedResponseId && (
              <FeedbackForm
                responseId={selectedResponseId}
                onSuccess={onClose}
              />
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
    </Box>
  )
}
