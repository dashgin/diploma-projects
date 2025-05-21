import {
  Box,
  Container,
  Flex,
  Heading,
  Spinner,
  Stack,
  Text,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import {
  Link,
  MatchRoute,
  createFileRoute,
  useNavigate,
} from "@tanstack/react-router"
import { FiArrowLeft } from "react-icons/fi"

import { QuizzesService } from "@/client"
import type { QuizRead } from "@/client"
import EditQuiz from "@/components/Quizzes/EditQuiz"
import QuestionsList from "@/components/Quizzes/QuestionsList"
import { Button } from "@/components/ui/button"

// Interface for loader data
interface QuizDetailLoaderData {
  quizId: number
  quiz?: QuizRead
}

export const Route = createFileRoute("/_layout/quizzes/$quizId")({
  component: QuizDetail,
  loader: ({ params }): { quizId: number } => {
    return {
      quizId: Number.parseInt(params.quizId, 10),
    }
  },
})

function QuizDetail() {
  const {
    quizId,
    quiz: initialQuiz,
  } = Route.useLoaderData() as QuizDetailLoaderData
  const navigate = useNavigate({ from: Route.fullPath })

  // Fetch quiz details - initialized with data from the loader
  const {
    data: quiz,
    isLoading: isQuizLoading,
    error: quizError,
  } = useQuery({
    queryKey: ["quiz", quizId],
    queryFn: () => QuizzesService.readQuiz({ quizId }),
    initialData: initialQuiz,
  })

  if (isQuizLoading) {
    return (
      <Flex justify="center" align="center" height="50vh">
        <Spinner size="xl" />
      </Flex>
    )
  }

  if (quizError || !quiz) {
    return (
      <Box p={5} textAlign="center">
        <Heading as="h3" size="md" mb={4}>
          Error loading quiz
        </Heading>
        <Text>
          Unable to load the requested quiz. It may not exist or you may not
          have permission to view it.
        </Text>
        <Button mt={4} onClick={() => navigate({ to: "/_layout/quizzes" })}>
          <FiArrowLeft />
          Back to Quizzes
        </Button>
      </Box>
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
          <EditQuiz quiz={quiz} />
        </Flex>
        <Box h="1px" bg="gray.200" my={4} />
        <Stack gap={4}>
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Instructions
            </Heading>
            <Text pt={2}>
              {quiz.instructions || "No instructions provided"}
            </Text>
          </Box>
          <Box h="1px" bg="gray.200" />
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Status
            </Heading>
            <Text pt={2}>{quiz.is_active ? "Active" : "Inactive"}</Text>
          </Box>
          <Box h="1px" bg="gray.200" />
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Quiz ID
            </Heading>
            <Text pt={2}>{quiz.id}</Text>
          </Box>
        </Stack>
      </Box>

      <Box borderWidth="1px" borderRadius="lg" p={6}>
        <QuestionsList quizId={quiz.id} />
      </Box>
    </Container>
  )
}
