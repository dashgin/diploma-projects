import { Container, Flex, Heading, Stack } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"

import { AssignmentsList } from "@/components/Assignments"

export const Route = createFileRoute("/_layout/assignments/")({
  component: AssignmentsPage,
})

function AssignmentsPage() {
  return (
    <Container maxW="full" py={8}>
      <Stack spacing={8}>
        <Flex justifyContent="space-between" alignItems="center">
          <Heading size="lg">Assignments</Heading>
        </Flex>

        {/* Show user's assigned quizzes */}
        <AssignmentsList userAssignments={true} />

        {/* Show all assignments (for teachers/admins) */}
        <AssignmentsList />
      </Stack>
    </Container>
  )
}
