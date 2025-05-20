import React from "react"

import { Box, Flex, Heading, Stack, Text } from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { type QuizRead, QuizzesService } from "../../client"

interface QuizListProps {
  quizzes?: QuizRead[] | null
}

export function QuizList({ quizzes: filteredQuizzes }: QuizListProps) {
  const { data: quizzes } = useQuery({
    queryKey: ["quizzes"],
    queryFn: () => QuizzesService.readQuizzes(),
  })

  // Use filtered quizzes if provided, otherwise use all quizzes
  const displayQuizzes = filteredQuizzes || quizzes || []

  return (
    <Box>
      <Heading mb={6} size="lg">
        Available Quizzes
      </Heading>
      {displayQuizzes.length === 0 ? (
        <Text>No quizzes found.</Text>
      ) : (
        <Stack gap={4}>
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
                  {quiz.instructions && <Text mt={2}>{quiz.instructions}</Text>}
                  <Flex mt={2} gap={4}>
                    <Text fontSize="sm">
                      {/* Optional info about questions count */}
                    </Text>
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
