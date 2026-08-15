import {
  Badge,
  Button,
  Card,
  Flex,
  Heading,
  Spinner,
  Stack,
  Text,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import { format } from "date-fns"
import { FiArrowLeft } from "react-icons/fi"

import {
  type ApiError,
  AssignmentsService,
  QuestionsService,
  QuizzesService,
  UsersService,
} from "@/client"
import { handleError } from "@/utils"

interface AssignmentDetailsProps {
  assignmentId: number
}

export const AssignmentDetails = ({ assignmentId }: AssignmentDetailsProps) => {
  const navigate = useNavigate()

  const { data: assignment, isLoading: isLoadingAssignment } = useQuery({
    queryKey: ["assignments", assignmentId],
    queryFn: () => AssignmentsService.readAssignment({ assignmentId }),
  })

  const { data: quiz, isLoading: isLoadingQuiz } = useQuery({
    queryKey: ["quizzes", assignment?.quiz_id],
    queryFn: () =>
      QuizzesService.readQuiz({ quizId: assignment?.quiz_id ?? 0 }),
    enabled: !!assignment?.quiz_id,
  })

  const { data: student, isLoading: isLoadingStudent } = useQuery({
    queryKey: ["users", assignment?.student_id],
    queryFn: () =>
      UsersService.readUserById({ userId: assignment?.student_id ?? 0 }),
    enabled: !!assignment?.student_id,
  })

  const { data: questionsData, isLoading: isLoadingQuestions } = useQuery({
    queryKey: ["questions", assignment?.quiz_id],
    queryFn: () =>
      QuestionsService.readQuestionsByQuiz({
        quizId: assignment?.quiz_id ?? 0,
      }),
    enabled: !!assignment?.quiz_id,
  })

  // Extract questions data from the new pagination format
  const questions = questionsData?.data || []

  if (
    isLoadingAssignment ||
    isLoadingQuiz ||
    isLoadingStudent ||
    isLoadingQuestions
  ) {
    return (
      <Flex justify="center" align="center" py={10}>
        <Spinner size="xl" />
      </Flex>
    )
  }

  if (!assignment || !quiz || !student) {
    return (
      <Card.Root>
        <Card.Body>
          <Text>
            Assignment not found or you don't have permission to view it.
          </Text>
        </Card.Body>
      </Card.Root>
    )
  }

  const handleBack = () => {
    navigate({ to: "/assignments" })
  }

  const dueDate = assignment.due_date ? new Date(assignment.due_date) : null
  const isOverdue = dueDate ? dueDate < new Date() : false
  const statusColor = !dueDate ? "blue" : isOverdue ? "red" : "green"
  const statusText = !dueDate ? "Open" : isOverdue ? "Overdue" : "Active"

  return (
    <Stack gap={4}>
      <Flex justifyContent="space-between" alignItems="center">
        <Button variant="ghost" onClick={handleBack}>
          <FiArrowLeft />
          Back to Assignments
        </Button>
        <Badge colorPalette={statusColor} size="lg">
          {statusText}
        </Badge>
      </Flex>

      <Card.Root>
        <Card.Header>
          <Heading size="md">{quiz.title}</Heading>
          <Text color="gray.600" mt={1}>
            {quiz.instructions}
          </Text>
        </Card.Header>
        <Card.Body>
          <Stack
            direction={{ base: "column", md: "row" }}
            gap={8}
            justifyContent="space-between"
          >
            <Stack>
              <Text fontWeight="bold">Student</Text>
              <Text fontSize="xl">{student.full_name || student.email}</Text>
              <Text fontSize="sm">{student.email}</Text>
            </Stack>

            <Stack>
              <Text fontWeight="bold">Questions</Text>
              <Text fontSize="xl">{questions?.length || 0}</Text>
            </Stack>

            <Stack>
              <Text fontWeight="bold">Due Date</Text>
              <Text fontSize="xl">
                {dueDate ? format(dueDate, "MMM dd, yyyy") : "No deadline"}
              </Text>
              {dueDate && (
                <Text fontSize="sm">{format(dueDate, "h:mm a")}</Text>
              )}
            </Stack>
          </Stack>
        </Card.Body>
      </Card.Root>
    </Stack>
  )
}
