import {
  Badge,
  Box,
  Card,
  CardBody,
  Flex,
  Heading,
  Icon,
  Link,
  Text,
  Tooltip,
} from "@chakra-ui/react"
import type React from "react"
import { FaExternalLinkAlt } from "react-icons/fa"
import type { ResourceRead } from "../../client/types.gen"

interface ResourceCardProps {
  resource: ResourceRead
}

export const ResourceCard: React.FC<ResourceCardProps> = ({ resource }) => {
  const getResourceTypeColor = (type: string): string => {
    const typeColors: Record<string, string> = {
      article: "blue",
      video: "red",
      book: "purple",
      exercise: "green",
      tutorial: "orange",
      course: "teal",
      documentation: "gray",
    }

    return typeColors[type.toLowerCase()] || "gray"
  }

  const getRelevanceColor = (score?: number | null): string => {
    if (!score) return "gray"
    if (score >= 0.8) return "green"
    if (score >= 0.6) return "blue"
    if (score >= 0.4) return "yellow"
    return "red"
  }

  return (
    <Card variant="outline" size="sm" borderWidth="1px" shadow="sm">
      <CardBody p={3}>
        <Flex justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Heading size="xs" noOfLines={1} flex="1">
            {resource.title}
          </Heading>

          <Badge
            colorScheme={getResourceTypeColor(resource.resource_type)}
            ml={2}
            fontSize="xs"
          >
            {resource.resource_type}
          </Badge>
        </Flex>

        {resource.description && (
          <Text fontSize="sm" color="gray.600" noOfLines={2} mb={2}>
            {resource.description}
          </Text>
        )}

        <Flex justifyContent="space-between" alignItems="center">
          {resource.url ? (
            <Link
              href={resource.url}
              isExternal
              color="blue.500"
              fontSize="sm"
              display="flex"
              alignItems="center"
            >
              View Resource <FaExternalLinkAlt />
            </Link>
          ) : (
            <Box />
          )}

          {resource.relevance_score && (
            <Tooltip
              label={`Relevance Score: ${(resource.relevance_score * 100).toFixed(0)}%`}
              placement="top"
            >
              <Badge colorScheme={getRelevanceColor(resource.relevance_score)}>
                {(resource.relevance_score * 100).toFixed(0)}%
              </Badge>
            </Tooltip>
          )}
        </Flex>
      </CardBody>
    </Card>
  )
}
