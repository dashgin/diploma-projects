import {
  Box,
  Flex,
  Heading,
  Spinner,
  Stack,
  Text,
} from "@chakra-ui/react"
import { QuizRead } from "../../client"
import { useQuizzes } from "../../hooks/useQuizzes"

interface QuizListProps {
  quizzes?: QuizRead[] | null
}

export function QuizList({ quizzes: filteredQuizzes }: QuizListProps) {
  const { data: quizzes, isLoading, error } = useQuizzes()
  
  // Use filtered quizzes if provided, otherwise use all quizzes
  const displayQuizzes = filteredQuizzes || quizzes || []

  if (isLoading && !filteredQuizzes) {
    return (
      <Box textAlign="center" py={10}>
        <Spinner size="xl" />
      </Box>
    )
  }

  if (error && !filteredQuizzes) {
    return (
      <Box textAlign="center" py={10}>
        <Text color="red.500">Error loading quizzes</Text>
      </Box>
    )
  }

  return (
    <Box>
      <Heading mb={6} size="lg">
        Available Quizzes
      </Heading>
      {displayQuizzes.length === 0 ? (
        <Text>No quizzes found.</Text>
      ) : (
        <Stack spacing={4}>
          {displayQuizzes.map((quiz) => (
            <Box 
              key={quiz.id} 
              p={4} 
              borderWidth="1px" 
              borderRadius="lg" 
              bg="bg.surface"
              _hover={{ bg: "bg.muted" }}
              transition="all 0.2s"
              shadow="md"
            >
              <Flex justifyContent="space-between" alignItems="center">
                <Box>
                  <Heading size="md">{quiz.title}</Heading>
                  <Text mt={2}>{quiz.description}</Text>
                  <Flex mt={2} gap={4}>
                    <Text fontSize="sm">
                      {quiz.questions?.length || 0} questions
                    </Text>
                    {quiz.time_limit && (
                      <Text fontSize="sm">
                        Time limit: {quiz.time_limit} minutes
                      </Text>
                    )}
                  </Flex>
                </Box>
              </Flex>
            </Box>
          ))}
        </Stack>
      )}
    </Box>
  )
} 