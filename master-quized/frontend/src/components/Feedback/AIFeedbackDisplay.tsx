"use client"

import {
  Badge,
  Box,
  Button,
  Card,
  Collapsible,
  Flex,
  Heading,
  List,
  Spinner,
  Text,
  useDisclosure,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import type React from "react"
import { FiAlertTriangle, FiCheckCircle } from "react-icons/fi"
import { FeedbackService } from "../../client/sdk.gen"
import type { FeedbackRead } from "../../client/types.gen"

interface AIFeedbackDisplayProps {
  responseId: number
  demo?: boolean | string
}

export const AIFeedbackDisplay: React.FC<AIFeedbackDisplayProps> = ({
  responseId,
  demo = false,
}) => {
  const { open: isDetailsOpen, onToggle: toggleDetails } = useDisclosure()

  // If demo mode, use hardcoded feedback
  if (demo === "fail") {
    const failFeedback: FeedbackRead = {
      id: 2,
      response_id: responseId,
      feedback_text:
        "Incorrect. Python is a programming language. Please review the definitions of programming and markup languages.",
      error_type: ["factual", "critical"],
      confidence_score: 0.95,
      feedback_content: {
        concepts_covered: [],
        concepts_missed: [
          "Python is a programming language",
          "Difference between programming and markup languages",
        ],
      },
      ai_metadata: null,
    }
    return (
      <AIFeedbackContent
        feedback={failFeedback}
        isDetailsOpen={isDetailsOpen}
        toggleDetails={toggleDetails}
      />
    )
  }

  if (demo) {
    const dummyFeedback: FeedbackRead = {
      id: 1,
      response_id: responseId,
      feedback_text:
        "Great attempt! You covered most key concepts, but missed explaining the difference between mitosis and meiosis.",
      error_type: ["conceptual", "minor"],
      confidence_score: 0.82,
      feedback_content: {
        concepts_covered: ["Cell division", "Chromosome replication"],
        concepts_missed: ["Difference between mitosis and meiosis"],
      },
      ai_metadata: null,
    }
    return (
      <AIFeedbackContent
        feedback={dummyFeedback}
        isDetailsOpen={isDetailsOpen}
        toggleDetails={toggleDetails}
      />
    )
  }

  // Fetch feedback for this response
  const {
    data: feedback,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["feedback", "response", responseId],
    queryFn: () => FeedbackService.readFeedbackByResponse({ responseId }),
    refetchInterval: (data) => (!data ? 5000 : false), // Poll every 5 seconds if no data
  })

  if (isLoading) {
    return (
      <Box p={4} borderWidth="1px" borderRadius="md" bg="blue.50">
        <Flex align="center" gap={2}>
          <Spinner size="sm" />
          <Text>Loading AI feedback...</Text>
        </Flex>
      </Box>
    )
  }

  if (isError) {
    return (
      <Box p={4} borderWidth="1px" borderRadius="md" bg="red.50">
        <Flex align="center" gap={2}>
          <FiAlertTriangle color="red" />
          <Text>
            Error loading feedback:{" "}
            {(error as Error)?.message || "Unknown error"}
          </Text>
        </Flex>
      </Box>
    )
  }

  // If no feedback yet
  if (!feedback) {
    return (
      <Box p={4} borderWidth="1px" borderRadius="md" bg="gray.50">
        <Text>
          AI feedback not available yet. It will appear here once generated.
        </Text>
      </Box>
    )
  }

  return (
    <AIFeedbackContent
      feedback={feedback}
      isDetailsOpen={isDetailsOpen}
      toggleDetails={toggleDetails}
    />
  )
}

interface AIFeedbackContentProps {
  feedback: FeedbackRead
  isDetailsOpen: boolean
  toggleDetails: () => void
}

const AIFeedbackContent: React.FC<AIFeedbackContentProps> = ({
  feedback,
  isDetailsOpen,
  toggleDetails,
}) => {
  const content = feedback.feedback_content || {}
  const conceptsCovered = (content.concepts_covered as string[]) || []
  const conceptsMissed = (content.concepts_missed as string[]) || []

  return (
    <Card.Root variant="outline" bg="blue.50" mb={4}>
      <Card.Header pb={2}>
        <Flex justify="space-between" align="center">
          <Heading size="md">AI Feedback</Heading>
          {feedback.confidence_score && (
            <Badge colorScheme={getConfidenceColor(feedback.confidence_score)}>
              Confidence: {(feedback.confidence_score * 100).toFixed(0)}%
            </Badge>
          )}
        </Flex>
      </Card.Header>

      <Card.Body pt={0}>
        <Text mb={4}>{feedback.feedback_text}</Text>

        {feedback.error_type && feedback.error_type.length > 0 && (
          <Flex gap={2} mb={3} wrap="wrap">
            <Text fontWeight="bold">Issue types:</Text>
            {feedback.error_type.map((type, index) => (
              <Badge key={index} colorScheme={getErrorTypeColor(type)}>
                {type}
              </Badge>
            ))}
          </Flex>
        )}

        <Button size="sm" onClick={toggleDetails} variant="outline" mb={3}>
          {isDetailsOpen ? "Hide Details" : "Show Details"}
        </Button>

        <Collapsible.Root open={isDetailsOpen}>
          <Collapsible.Content>
            <Box p={3} bg="white" borderRadius="md" mb={3}>
              <Heading size="sm" mb={2}>
                Key Concepts Analysis
              </Heading>

              {conceptsCovered.length > 0 && (
                <Box mb={3}>
                  <Text fontWeight="bold">Concepts Covered:</Text>
                  <List.Root gap="1" variant="plain" align="center">
                    {conceptsCovered.map((concept: string, index: number) => (
                      <List.Item key={index}>
                        <List.Indicator asChild color="green.500">
                          <FiCheckCircle />
                        </List.Indicator>
                        <Text>{concept}</Text>
                      </List.Item>
                    ))}
                  </List.Root>
                </Box>
              )}

              {conceptsMissed.length > 0 && (
                <Box>
                  <Text fontWeight="bold">Concepts Missed:</Text>
                  <List.Root gap="1" variant="plain" align="center">
                    {conceptsMissed.map((concept: string, index: number) => (
                      <List.Item key={index}>
                        <List.Indicator asChild color="orange.500">
                          <FiAlertTriangle />
                        </List.Indicator>
                        <Text>{concept}</Text>
                      </List.Item>
                    ))}
                  </List.Root>
                </Box>
              )}

              {feedback.ai_metadata?.resources && (
                <Box mt={3}>
                  <Heading size="sm" mb={2}>
                    Recommended Resources
                  </Heading>
                  <List.Root gap="1" variant="plain">
                    {feedback.ai_metadata.resources.map(
                      (resource: any, index: number) => (
                        <List.Item key={index}>
                          <Text>• {resource.title}</Text>
                        </List.Item>
                      ),
                    )}
                  </List.Root>
                </Box>
              )}
            </Box>
          </Collapsible.Content>
        </Collapsible.Root>
      </Card.Body>
    </Card.Root>
  )
}

function getConfidenceColor(score: number): string {
  if (score >= 0.8) return "green"
  if (score >= 0.6) return "yellow"
  return "red"
}

function getErrorTypeColor(errorType: string): string {
  switch (errorType) {
    case "critical":
      return "red"
    case "factual":
      return "orange"
    case "conceptual":
      return "yellow"
    case "minor":
      return "blue"
    default:
      return "gray"
  }
}
