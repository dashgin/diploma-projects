import { Box, Flex, Heading, Spinner, Table, Text } from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { Link } from "@tanstack/react-router"

import { AttemptsService } from "@/client"
import { Button } from "@/components/ui/button"
import { formatDate } from "@/utils/formatters"

interface QuizAttemptsListProps {
  quizId: number
}

const QuizAttemptsList = ({ quizId }: QuizAttemptsListProps) => {
  // Fetch attempts
  const {
    data: attemptsResponse,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["attempts", quizId],
    queryFn: () => AttemptsService.readAttempts({ limit: 100 }),
  })

  // Handle the pagination format with data and count fields
  const allAttempts = attemptsResponse?.data || []

  // Filter attempts by quiz ID
  const attempts = Array.isArray(allAttempts)
    ? allAttempts.filter((attempt) => attempt.quiz_id === quizId)
    : []

  if (isLoading) {
    return (
      <Flex justify="center" align="center" py={10}>
        <Spinner size="xl" />
      </Flex>
    )
  }

  if (error) {
    return (
      <Box p={5} borderRadius="md" borderWidth="1px" bg="red.50">
        <Text>Error loading attempts.</Text>
      </Box>
    )
  }

  if (attempts.length === 0) {
    return (
      <Box p={5} borderRadius="md" borderWidth="1px" textAlign="center">
        <Text mb={4}>No attempts available for this quiz.</Text>
      </Box>
    )
  }

  return (
    <Box>
      <Heading size="md" mb={4}>
        Attempts ({attempts.length})
      </Heading>

      <Table.Root size="sm" variant="outline">
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader>ID</Table.ColumnHeader>
            <Table.ColumnHeader>User</Table.ColumnHeader>
            <Table.ColumnHeader>Started</Table.ColumnHeader>
            <Table.ColumnHeader>Completed</Table.ColumnHeader>
            <Table.ColumnHeader>Score</Table.ColumnHeader>
            <Table.ColumnHeader>Status</Table.ColumnHeader>
            <Table.ColumnHeader>Action</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {attempts.map((attempt) => (
            <Table.Row key={attempt.id}>
              <Table.Cell>{attempt.id}</Table.Cell>
              <Table.Cell>{attempt.student?.email || "Unknown"}</Table.Cell>
              <Table.Cell>{formatDate(attempt.started_at)}</Table.Cell>
              <Table.Cell>
                {attempt.completed_at
                  ? formatDate(attempt.completed_at)
                  : "Not completed"}
              </Table.Cell>
              <Table.Cell>
                {attempt.score !== null ? `${attempt.score}%` : "Not scored"}
              </Table.Cell>
              <Table.Cell>
                {attempt.is_completed ? "Completed" : "In Progress"}
              </Table.Cell>
              <Table.Cell>
                <Link to={`/attempts/${attempt.id}`}>
                  <Button size="sm" variant="outline">
                    View
                  </Button>
                </Link>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
    </Box>
  )
}

export default QuizAttemptsList
