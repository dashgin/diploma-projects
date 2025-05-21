import {
  Alert,
  Box,
  Button,
  Heading,
  Spinner,
  Stack,
  Text,
  useDisclosure,
} from "@chakra-ui/react"
import { FiAlertCircle } from "react-icons/fi";
import { useQuery } from "@tanstack/react-query"
import type React from "react"
import { RecommendationsService } from "../../client/sdk.gen"
import { ResourceCard } from "./ResourceCard"
import { ResourceModal } from "./ResourceModal"

interface ResourcesListProps {
  feedbackId: number
}

export const ResourcesList: React.FC<ResourcesListProps> = ({ feedbackId }) => {
  const { isOpen, onOpen, onClose } = useDisclosure()

  const {
    data: resources,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["resources", feedbackId],
    queryFn: () =>
      RecommendationsService.readRecommendationsByFeedback({
        feedbackId,
        limit: 10,
      }),
  })

  if (isLoading) {
    return (
      <Box textAlign="center" py={4}>
        <Spinner size="sm" />
        <Text mt={2} fontSize="sm" color="gray.600">
          Loading resources...
        </Text>
      </Box>
    )
  }

  if (error) {
    return (
      <Alert.Root status="error" borderRadius="md" size="sm">
        <Alert.Indicator />
        An error occurred while loading resources.
      </Alert.Root>
    )
  }

  if (!resources || resources.length === 0) {
    return (
      <Box>
        <Alert.Root status="info" borderRadius="md" mb={4} size="sm">
          <Alert.Indicator>
            <FiAlertCircle />
          </Alert.Indicator>
          No resources are currently available for this feedback.
        </Alert.Root>

        <Button size="sm" colorScheme="blue" onClick={onOpen}>
          Add Resource
        </Button>

        <ResourceModal
          isOpen={isOpen}
          onClose={onClose}
          feedbackId={feedbackId}
        />
      </Box>
    )
  }

  return (
    <Box>
      <Heading size="sm" mb={3}>
        Recommended Resources
      </Heading>

      <Stack spacing={3}>
        {resources.map((resource) => (
          <ResourceCard key={resource.id} resource={resource} />
        ))}
      </Stack>

      <Button
        size="sm"
        colorScheme="blue"
        variant="outline"
        mt={4}
        onClick={onOpen}
      >
        Add Resource
      </Button>

      <ResourceModal
        isOpen={isOpen}
        onClose={onClose}
        feedbackId={feedbackId}
      />
    </Box>
  )
}
