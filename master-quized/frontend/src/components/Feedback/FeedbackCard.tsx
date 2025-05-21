import {
  Badge,
  Box,
  Button,
  Card,
  CardBody,
  CardHeader,
  Flex,
  Heading,
  Text,
  useDisclosure,
} from "@chakra-ui/react"
import type React from "react"
import type { FeedbackRead } from "../../client/types.gen"
import { ResourcesList } from "../Resources/ResourcesList"

interface FeedbackCardProps {
  feedback: FeedbackRead
  showResources?: boolean
}

export const FeedbackCard: React.FC<FeedbackCardProps> = ({
  feedback,
  showResources = false,
}) => {
  const { isOpen, onToggle } = useDisclosure()

  return (
    <Card mb={4} variant="outline" borderWidth="1px" shadow="md">
      <CardHeader pb={2}>
        <Flex justifyContent="space-between" alignItems="center">
          <Heading size="md">Feedback #{feedback.id}</Heading>
          {feedback.error_type && (
            <Badge colorScheme={getErrorTypeColor(feedback.error_type)}>
              {feedback.error_type}
            </Badge>
          )}
        </Flex>
      </CardHeader>

      <CardBody pt={0}>
        <Text fontSize="md" mb={3}>
          {feedback.feedback_text}
        </Text>

        {feedback.confidence_score && (
          <Flex alignItems="center" mb={2}>
            <Text fontSize="sm" fontWeight="bold" mr={2}>
              Confidence:
            </Text>
            <Badge colorScheme={getConfidenceColor(feedback.confidence_score)}>
              {(feedback.confidence_score * 100).toFixed(0)}%
            </Badge>
          </Flex>
        )}

        {showResources && (
          <Box mt={4}>
            <Button
              size="sm"
              colorScheme="blue"
              variant="outline"
              onClick={onToggle}
            >
              {isOpen ? "Hide Resources" : "View Recommended Resources"}
            </Button>

            {isOpen && (
              <Box mt={3}>
                <ResourcesList feedbackId={feedback.id} />
              </Box>
            )}
          </Box>
        )}
      </CardBody>
    </Card>
  )
}

// Helper functions to determine colors based on values
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

function getConfidenceColor(score: number): string {
  if (score >= 0.8) return "green"
  if (score >= 0.6) return "blue"
  if (score >= 0.4) return "yellow"
  return "red"
}
