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
} from "@tanstack/react-router"
import { FiArrowLeft } from "react-icons/fi"

import { QuizzesService } from "@/client"
import type { QuizRead } from "@/client"
import { CreateAssignment } from "@/components/Assignments"
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
            <CreateAssignment quizId={quiz.id} />
            <EditQuiz quiz={quiz} />
          </Flex>
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
