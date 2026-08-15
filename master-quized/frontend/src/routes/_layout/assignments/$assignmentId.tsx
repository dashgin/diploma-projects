import { Container } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"

import { AssignmentDetails } from "@/components/Assignments"

export const Route = createFileRoute("/_layout/assignments/$assignmentId")({
  component: AssignmentDetailsPage,
})

function AssignmentDetailsPage() {
  const { assignmentId } = Route.useParams()
  return (
    <Container maxW="full" py={8}>
      <AssignmentDetails assignmentId={Number.parseInt(assignmentId, 10)} />
    </Container>
  )
}
