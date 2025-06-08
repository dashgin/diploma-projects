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
    <Box>
      {/* Main Feedback */}
      <Box
        p={4}
        bg="white"
        borderRadius="lg"
        border="1px solid"
        borderColor="purple.200"
        mb={4}
        shadow="sm"
      >
        <Flex justify="space-between" align="center" mb={3}>
          <Text fontWeight="bold" fontSize="md" color="purple.800">
            📝 Analysis Results
          </Text>
          {feedback.confidence_score && (
            <Badge
              colorScheme={getConfidenceColor(feedback.confidence_score)}
              variant="solid"
            >
              {(feedback.confidence_score * 100).toFixed(0)}% Confidence
            </Badge>
          )}
        </Flex>

        <Text color="gray.700" lineHeight="1.7" fontSize="md" mb={4}>
          {feedback.feedback_text}
        </Text>

        {feedback.error_type && feedback.error_type.length > 0 && (
          <Box>
            <Text fontWeight="bold" fontSize="sm" color="gray.600" mb={2}>
              Focus Areas:
            </Text>
            <Flex gap={2} wrap="wrap">
              {feedback.error_type.map((type, index) => (
                <Badge
                  key={index}
                  colorScheme={getErrorTypeColor(type)}
                  variant="outline"
                  fontSize="xs"
                >
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </Badge>
              ))}
            </Flex>
          </Box>
        )}
      </Box>

      {/* Detailed Analysis - Expandable */}
      {(conceptsCovered.length > 0 || conceptsMissed.length > 0) && (
        <Box>
          <Button
            size="sm"
            onClick={toggleDetails}
            variant="outline"
            colorScheme="purple"
            mb={3}
          >
            {isDetailsOpen
              ? "Hide Detailed Analysis ▲"
              : "Show Detailed Analysis ▼"}
          </Button>

          <Collapsible.Root open={isDetailsOpen}>
            <Collapsible.Content>
              <Box
                p={4}
                bg="white"
                borderRadius="lg"
                border="1px solid"
                borderColor="purple.200"
                shadow="sm"
              >
                <Heading size="sm" mb={4} color="purple.800">
                  🎯 Detailed Concept Analysis
                </Heading>

                {conceptsCovered.length > 0 && (
                  <Box mb={4}>
                    <Flex align="center" gap={2} mb={3}>
                      <Box
                        bg="green.500"
                        color="white"
                        borderRadius="full"
                        w="20px"
                        h="20px"
                        display="flex"
                        alignItems="center"
                        justifyContent="center"
                        fontSize="xs"
                      >
                        ✓
                      </Box>
                      <Text fontWeight="bold" color="green.700">
                        Concepts You Understood Well
                      </Text>
                    </Flex>
                    <List.Root gap="2" variant="plain">
                      {conceptsCovered.map((concept: string, index: number) => (
                        <List.Item key={index}>
                          <Box
                            p={2}
                            bg="green.50"
                            borderRadius="md"
                            border="1px solid"
                            borderColor="green.200"
                          >
                            <Flex align="center" gap={2}>
                              <List.Indicator asChild color="green.500">
                                <FiCheckCircle />
                              </List.Indicator>
                              <Text fontSize="sm" color="green.800">
                                {concept}
                              </Text>
                            </Flex>
                          </Box>
                        </List.Item>
                      ))}
                    </List.Root>
                  </Box>
                )}

                {conceptsMissed.length > 0 && (
                  <Box>
                    <Flex align="center" gap={2} mb={3}>
                      <Box
                        bg="orange.500"
                        color="white"
                        borderRadius="full"
                        w="20px"
                        h="20px"
                        display="flex"
                        alignItems="center"
                        justifyContent="center"
                        fontSize="xs"
                      >
                        !
                      </Box>
                      <Text fontWeight="bold" color="orange.700">
                        Areas for Improvement
                      </Text>
                    </Flex>
                    <List.Root gap="2" variant="plain">
                      {conceptsMissed.map((concept: string, index: number) => (
                        <List.Item key={index}>
                          <Box
                            p={2}
                            bg="orange.50"
                            borderRadius="md"
                            border="1px solid"
                            borderColor="orange.200"
                          >
                            <Flex align="center" gap={2}>
                              <List.Indicator asChild color="orange.500">
                                <FiAlertTriangle />
                              </List.Indicator>
                              <Text fontSize="sm" color="orange.800">
                                {concept}
                              </Text>
                            </Flex>
                          </Box>
                        </List.Item>
                      ))}
                    </List.Root>
                  </Box>
                )}

                {/* Study Tips */}
                <Box
                  mt={4}
                  p={3}
                  bg="blue.50"
                  borderRadius="md"
                  border="1px solid"
                  borderColor="blue.200"
                >
                  <Text fontWeight="bold" fontSize="sm" color="blue.800" mb={2}>
                    💡 Study Tips
                  </Text>
                  <Text fontSize="sm" color="blue.700">
                    {conceptsMissed.length > 0
                      ? "Focus on reviewing the concepts listed above. Try to understand the underlying principles and practice with similar questions."
                      : "Great work! Continue practicing to reinforce your understanding of these concepts."}
                  </Text>
                </Box>

                {feedback.ai_metadata?.resources && (
                  <Box mt={4}>
                    <Heading size="sm" mb={2} color="blue.800">
                      📚 Recommended Resources
                    </Heading>
                    <List.Root gap="1" variant="plain">
                      {feedback.ai_metadata.resources.map(
                        (resource: any, index: number) => (
                          <List.Item key={index}>
                            <Text fontSize="sm">• {resource.title}</Text>
                          </List.Item>
                        ),
                      )}
                    </List.Root>
                  </Box>
                )}
              </Box>
            </Collapsible.Content>
          </Collapsible.Root>
        </Box>
      )}
    </Box>
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
