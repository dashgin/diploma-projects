import {
  Badge,
  Box,
  Flex,
  Heading,
  Spinner,
  Table,
  Text,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"
import { FiEye } from "react-icons/fi"

import { type AttemptRead, AttemptsService } from "@/client"
import { Button } from "@/components/ui/button"
import { formatDate } from "@/utils/formatters"

interface AttemptsListProps {
  userAttempts?: boolean
  quizId?: number
}

export function AttemptsList({
  userAttempts = false,
  quizId,
}: AttemptsListProps) {
  const { data: attemptsResponse, isLoading } = useQuery({
    queryKey: ["attempts", userAttempts ? "my" : "all", quizId],
    queryFn: () => {
      if (userAttempts) {
        return AttemptsService.readUserAttempts()
      }
      return AttemptsService.readAttempts()
    },
  })

  // Extract attempts from the paginated response
  const attempts = attemptsResponse?.data || []
  const totalCount = attemptsResponse?.count || 0

  if (isLoading) {
    return (
      <Flex justify="center" align="center" py={10}>
        <Spinner size="xl" />
      </Flex>
    )
  }

  if (!attempts || attempts.length === 0) {
    return (
      <Box>
        <Heading size="md" mb={4}>
          {userAttempts ? "My Quiz Attempts" : "All Quiz Attempts"}
        </Heading>
        <Box p={5} borderRadius="md" borderWidth="1px" textAlign="center">
          <Text>No quiz attempts found.</Text>
        </Box>
      </Box>
    )
  }

  return (
    <Box>
      <Heading size="md" mb={4}>
        {userAttempts ? "My Quiz Attempts" : "All Quiz Attempts"} ({totalCount})
      </Heading>
      <Box overflowX="auto">
        <Table.Root variant="line">
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeader>ID</Table.ColumnHeader>
              <Table.ColumnHeader>Quiz</Table.ColumnHeader>
              <Table.ColumnHeader>Status</Table.ColumnHeader>
              <Table.ColumnHeader>Score</Table.ColumnHeader>
              <Table.ColumnHeader>Date</Table.ColumnHeader>
              <Table.ColumnHeader>Actions</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {attempts.map((attempt: AttemptRead) => (
              <Table.Row key={attempt.id}>
                <Table.Cell>{attempt.id}</Table.Cell>
                <Table.Cell>{attempt.quiz_id}</Table.Cell>
                <Table.Cell>
                  <Badge
                    colorScheme={attempt.is_completed ? "green" : "yellow"}
                    borderRadius="full"
                    px={2}
                  >
                    {attempt.is_completed ? "Completed" : "In Progress"}
                  </Badge>
                </Table.Cell>
                <Table.Cell>
                  {attempt.score !== null && attempt.is_completed
                    ? `${attempt.score}%`
                    : "-"}
                </Table.Cell>
                <Table.Cell>
                  {attempt.completed_at
                    ? formatDate(attempt.completed_at)
                    : "Not completed"}
                </Table.Cell>
                <Table.Cell>
                  <Link to={`/attempts/${attempt.id}`}>
                    <Button size="sm" variant="ghost">
                      <FiEye />
                      &nbsp;View
                    </Button>
                  </Link>
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      </Box>
    </Box>
  )
}
