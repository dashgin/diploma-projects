import {
  Badge,
  Card,
  EmptyState,
  Flex,
  Heading,
  Stack,
  Table,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import { format } from "date-fns"
import { FiSearch } from "react-icons/fi"

import {
  type ApiError,
  type AssignmentRead,
  AssignmentsService,
} from "@/client"
import { handleError } from "@/utils"
import PendingAssignments from "../Pending/PendingAssignments"

interface AssignmentsListProps {
  userAssignments?: boolean
  assignments?: AssignmentRead[]
}

export const AssignmentsList = ({
  userAssignments = false,
  assignments,
}: AssignmentsListProps) => {
  const navigate = useNavigate()

  const { data, isLoading, error } = useQuery({
    queryKey: userAssignments
      ? ["assignments", "user"]
      : ["assignments", "all"],
    queryFn: () =>
      userAssignments
        ? AssignmentsService.readUserAssignments()
        : AssignmentsService.readAssignments(),
    enabled: !assignments, // Only fetch if assignments not provided
  })

  // Use provided assignments or fetched data
  // Handle the new pagination format with data and count
  const assignmentsData = assignments || data?.data || []

  if (isLoading && !assignments) {
    return <PendingAssignments />
  }

  if (error) {
    handleError(error as ApiError)
    return null
  }

  if (!assignmentsData || assignmentsData.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>
              {userAssignments
                ? "No assignments yet"
                : "No assignments created"}
            </EmptyState.Title>
            <EmptyState.Description>
              {userAssignments
                ? "You don't have any assigned quizzes yet."
                : "Start by creating a new assignment."}
            </EmptyState.Description>
          </VStack>
        </EmptyState.Content>
      </EmptyState.Root>
    )
  }

  const handleRowClick = (assignment: AssignmentRead) => {
    navigate({ to: `/assignments/${assignment.id}` })
  }

  return (
    <Card.Root>
      <Card.Header>
        <Heading size="md">
          {userAssignments ? "My Assignments" : "All Assignments"}
        </Heading>
      </Card.Header>
      <Card.Body>
        <Table.Root size={{ base: "sm", md: "md" }}>
          <Table.Header>
            <Table.Row>
              <Table.ColumnHeader>ID</Table.ColumnHeader>
              <Table.ColumnHeader>Quiz ID</Table.ColumnHeader>
              <Table.ColumnHeader>Student ID</Table.ColumnHeader>
              <Table.ColumnHeader>Due Date</Table.ColumnHeader>
              <Table.ColumnHeader>Status</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {assignmentsData.map((assignment) => (
              <Table.Row
                key={assignment.id}
                onClick={() => handleRowClick(assignment)}
                _hover={{ bg: "gray.50", cursor: "pointer" }}
              >
                <Table.Cell>{assignment.id}</Table.Cell>
                <Table.Cell>{assignment.quiz_id}</Table.Cell>
                <Table.Cell>{assignment.student_id}</Table.Cell>
                <Table.Cell>
                  {assignment.due_date
                    ? format(new Date(assignment.due_date), "MMM dd, yyyy")
                    : "No deadline"}
                </Table.Cell>
                <Table.Cell>
                  <Badge
                    colorPalette={
                      !assignment.due_date
                        ? "blue"
                        : new Date(assignment.due_date) < new Date()
                          ? "red"
                          : "green"
                    }
                  >
                    {!assignment.due_date
                      ? "Open"
                      : new Date(assignment.due_date) < new Date()
                        ? "Overdue"
                        : "Active"}
                  </Badge>
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table.Root>
      </Card.Body>
    </Card.Root>
  )
}
