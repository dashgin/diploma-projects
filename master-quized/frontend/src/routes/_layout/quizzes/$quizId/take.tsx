import { Container, Flex, Heading } from "@chakra-ui/react"
import { Spinner } from "@chakra-ui/react"
import {
  Link,
  MatchRoute,
  createFileRoute,
  useNavigate,
} from "@tanstack/react-router"
import { FiArrowLeft } from "react-icons/fi"

import { QuizTaker } from "@/components/Items"
import { Button } from "@/components/ui/button"

interface QuizTakerLoaderData {
  quizId: number
  assignmentId?: number
}

export const Route = createFileRoute("/_layout/quizzes/$quizId/take")({
  component: QuizTakerPage,
})

function QuizTakerPage() {
  const { quizId } = Route.useParams()
  const { assignmentId } = Route.useSearch()
  const navigate = useNavigate()

  return (
    <Container maxW="full">
      <Flex align="center" pt={8} pb={4}>
        <Link to="/quizzes" preload="intent" className="mr-4">
          <Button variant="ghost">
            <FiArrowLeft />
            Back to Quizzes
            <MatchRoute to="/quizzes" pending>
              {(isPending) => isPending && <Spinner size="sm" ml={2} />}
            </MatchRoute>
          </Button>
        </Link>

        <Heading size="lg">Take Quiz</Heading>
      </Flex>

      <QuizTaker
        quizId={Number.parseInt(quizId)}
        assignmentId={assignmentId ? Number.parseInt(assignmentId) : undefined}
      />
    </Container>
  )
}
