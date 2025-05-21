"use client"

import React from "react"
import {
  Box,
  Spinner,
  Text,
  Flex,
  Badge,
  Heading,
  Collapsible,
  Button,
  useDisclosure,
  List,
  Card,
  CardBody,
  CardHeader,
} from "@chakra-ui/react"
import { FeedbackService } from "../../client/sdk.gen"
import { useQuery } from "@tanstack/react-query"
import { FeedbackRead } from "../../client/types.gen"
import { FiCheckCircle, FiAlertTriangle } from "react-icons/fi"

interface AIFeedbackDisplayProps {
  responseId: number
}

export const AIFeedbackDisplay: React.FC<AIFeedbackDisplayProps> = ({
  responseId,
}) => {
  const { open: isDetailsOpen, onToggle: toggleDetails } = useDisclosure()
  
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
            Error loading feedback: {(error as Error)?.message || "Unknown error"}
          </Text>
        </Flex>
      </Box>
    )
  }

  // If no feedback yet
  if (!feedback) {
    return (
      <Box p={4} borderWidth="1px" borderRadius="md" bg="gray.50">
        <Text>AI feedback not available yet. It will appear here once generated.</Text>
      </Box>
    )
  }

  return <AIFeedbackContent feedback={feedback} isDetailsOpen={isDetailsOpen} toggleDetails={toggleDetails} />
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
      <CardHeader pb={2}>
        <Flex justify="space-between" align="center">
          <Heading size="md">AI Feedback</Heading>
          {feedback.confidence_score && (
            <Badge colorScheme={getConfidenceColor(feedback.confidence_score)}>
              Confidence: {(feedback.confidence_score * 100).toFixed(0)}%
            </Badge>
          )}
        </Flex>
      </CardHeader>
      
      <CardBody pt={0}>
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
            </Box>
          </Collapsible.Content>
        </Collapsible.Root>
      </CardBody>
    </Card.Root>
  )
}

// Helper functions for color coding
function getConfidenceColor(score: number): string {
  if (score >= 0.8) return "green"
  if (score >= 0.6) return "blue"
  if (score >= 0.4) return "yellow"
  return "red"
}

function getErrorTypeColor(errorType: string): string {
  const errorColors: Record<string, string> = {
    conceptual: "red",
    procedural: "orange",
    factual: "yellow",
    minor: "green",
    critical: "purple",
  }

  return errorColors[errorType.toLowerCase()] || "gray"
} 