import {
  Box,
  Container,
  Flex,
  Heading,
  Spinner,
  Tabs,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import {
  Link,
  MatchRoute,
  createFileRoute,
} from "@tanstack/react-router"
import { LuInfo, LuList, LuClock } from "react-icons/lu"
import { FiArrowLeft } from "react-icons/fi"

import { QuizzesService } from "@/client"
import type { QuizRead } from "@/client"
import { CreateAssignment } from "@/components/Assignments"
import EditQuiz from "@/components/Quizzes/EditQuiz"
import QuestionsList from "@/components/Quizzes/QuestionsList"
import QuizAttemptsList from "@/components/Quizzes/QuizAttemptsList"
import QuizDetailsTab from "@/components/Quizzes/QuizDetailsTab"
import { Button } from "@/components/ui/button"

// Interface for loader data
interface QuizDetailLoaderData {
  quizId: number
  quiz?: QuizRead
}

export const Route = createFileRoute("/_layout/quizzes/$quizId/")({
  component: QuizDetail,
  loader: async ({ params }) => {
    const quizId = Number.parseInt(params.quizId)
    return { quizId }
  },
})

function QuizDetail() {
  const { quizId, quiz: initialQuiz } =
    Route.useLoaderData() as QuizDetailLoaderData

  const { data: quiz, isLoading } = useQuery({
    queryKey: ["quizzes", quizId],
    queryFn: () => QuizzesService.readQuiz({ quizId }),
    initialData: initialQuiz,
  })

  if (isLoading || !quiz) {
    return (
      <Flex justify="center" align="center" height="100vh">
        <Spinner size="xl" />
      </Flex>
    )
  }

  return (
    <Container maxW="full">
      <Flex align="center" pt={8} pb={4}>
        <Link to="/quizzes" preload="intent" className="mr-4">
          <Button variant="ghost">
            <FiArrowLeft />
            Back
            <MatchRoute to="/quizzes" pending>
              {(isPending) => isPending && <Spinner size="sm" ml={2} />}
            </MatchRoute>
          </Button>
        </Link>

        <Heading size="lg">Quiz Details</Heading>
      </Flex>

      <Box borderWidth="1px" borderRadius="lg" p={6} mb={6}>
        <Flex justify="space-between" align="center" mb={4}>
          <Heading size="md">{quiz.title}</Heading>
          <Flex gap={2}>
            <Link to={`/quizzes/${quiz.id}/take`} preload="intent">
              <Button variant="solid" colorScheme="blue">
                Take Quiz
              </Button>
            </Link>
            <CreateAssignment quizId={quiz.id} />
            <EditQuiz quiz={quiz} />
          </Flex>
        </Flex>
      </Box>

      <Box borderWidth="1px" borderRadius="lg" p={6}>
        <Tabs.Root defaultValue="details" variant="line">
          <Tabs.List>
            <Tabs.Trigger value="details">
              <LuInfo />
              Details
            </Tabs.Trigger>
            <Tabs.Trigger value="questions">
              <LuList />
              Questions
            </Tabs.Trigger>
            <Tabs.Trigger value="attempts">
              <LuClock />
              Attempts
            </Tabs.Trigger>
          </Tabs.List>
          <Tabs.Content value="details" pt={4}>
            <QuizDetailsTab quiz={quiz} />
          </Tabs.Content>
          <Tabs.Content value="questions" pt={4}>
            <QuestionsList quizId={quiz.id} />
          </Tabs.Content>
          <Tabs.Content value="attempts" pt={4}>
            <QuizAttemptsList quizId={quiz.id} />
          </Tabs.Content>
        </Tabs.Root>
      </Box>
    </Container>
  )
}
