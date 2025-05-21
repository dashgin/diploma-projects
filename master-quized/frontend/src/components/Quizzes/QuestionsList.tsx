import {
  Accordion,
  Box,
  Flex,
  Heading,
  HStack,
  Spinner,
  Stack,
  Text,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { FiEdit, FiPlus, FiTrash } from "react-icons/fi"

import { QuestionsService, OptionsService, type QuestionRead, type OptionRead } from "@/client"
import AddOption from "./AddOption"
import AddQuestion from "./AddQuestion"
import DeleteOption from "./DeleteOption"
import DeleteQuestion from "./DeleteQuestion"
import EditOption from "./EditOption"
import EditQuestion from "./EditQuestion"

interface QuestionsListProps {
  quizId: number
}

const QuestionsList = ({ quizId }: QuestionsListProps) => {
  // Fetch questions
  const {
    data: questions,
    isLoading: isQuestionsLoading,
    error: questionsError,
  } = useQuery({
    queryKey: ["questions", quizId],
    queryFn: () => QuestionsService.readQuestionsByQuiz({ quizId }),
  })

  if (isQuestionsLoading) {
    return (
      <Flex justify="center" align="center" py={10}>
        <Spinner size="xl" />
      </Flex>
    )
  }

  if (questionsError || !questions) {
    return (
      <Box p={5} borderRadius="md" borderWidth="1px" bg="red.50">
        <Text>Error loading questions.</Text>
      </Box>
    )
  }

  if (questions.length === 0) {
    return (
      <Box>
        <Flex justify="space-between" align="center" mb={4}>
          <Heading size="md">Questions</Heading>
          <AddQuestion quizId={quizId} />
        </Flex>
        <Box p={5} borderRadius="md" borderWidth="1px" textAlign="center">
          <Text mb={4}>No questions available for this quiz.</Text>
          <AddQuestion quizId={quizId} />
        </Box>
      </Box>
    )
  }

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={4}>
        <Heading size="md">Questions ({questions.length})</Heading>
        <AddQuestion quizId={quizId} />
      </Flex>

      <Accordion.Root defaultValue={["0"]}>
        {questions.map((question: QuestionRead, index: number) => (
          <QuestionItem 
            key={question.id} 
            question={question} 
            index={index} 
          />
        ))}
      </Accordion.Root>
    </Box>
  )
}

// Component for a single question item with options
const QuestionItem = ({ question, index }: { question: QuestionRead; index: number }) => {
  // Fetch options if question is multiple choice
  const {
    data: options,
    isLoading: isOptionsLoading,
  } = useQuery({
    queryKey: ["options", question.id],
    queryFn: () => OptionsService.readOptionsByQuestion({ questionId: question.id }),
    enabled: question.question_type === "multiple_choice",
  })

  return (
    <Accordion.Item value={index.toString()}>
      <Box borderWidth="1px" mb={3} overflow="hidden" borderRadius="md">
        <Accordion.ItemTrigger p={4}>
          <Flex justify="space-between" align="center">
            <Box>
              <Heading size="sm">Question {index + 1}</Heading>
              <Text fontSize="sm" color="gray.600" mt={1}>
                {question.question_type === "multiple_choice"
                  ? "Multiple Choice"
                  : question.question_type === "short_answer"
                  ? "Short Answer"
                  : "Long Answer"}
              </Text>
            </Box>
          </Flex>
        </Accordion.ItemTrigger>

        <Accordion.ItemContent>
          <Box px={4} pb={4}>
            <Box p={3} bg="gray.50" borderRadius="md" mb={3}>
              <Text>{question.text}</Text>
            </Box>

            <Flex justify="flex-end" mb={3}>
              <HStack>
                <EditQuestion question={question} />
                <DeleteQuestion question={question} />
              </HStack>
            </Flex>

            {question.question_type === "multiple_choice" && (
              <Box mt={4}>
                <Flex justify="space-between" align="center" mb={2}>
                  <Heading size="xs">Options</Heading>
                  <AddOption questionId={question.id} />
                </Flex>

                {isOptionsLoading ? (
                  <Flex justify="center" py={4}>
                    <Spinner size="sm" />
                  </Flex>
                ) : !options || options.length === 0 ? (
                  <Text fontSize="sm" color="gray.600">
                    No options added yet
                  </Text>
                ) : (
                  <Stack gap={2} mt={2}>
                    {options.map((option: OptionRead) => (
                      <Flex
                        key={option.id}
                        p={2}
                        borderWidth="1px"
                        borderRadius="md"
                        justify="space-between"
                        align="center"
                        bg={option.is_correct ? "green.50" : "white"}
                        borderColor={option.is_correct ? "green.200" : "gray.200"}
                      >
                        <Text>{option.text}</Text>
                        <HStack>
                          <EditOption option={option} />
                          <DeleteOption option={option} />
                        </HStack>
                      </Flex>
                    ))}
                  </Stack>
                )}
              </Box>
            )}

            {question.correct_answer && (
              <Box mt={4}>
                <Heading size="xs" mb={2}>
                  Correct Answer
                </Heading>
                <Box p={3} bg="green.50" borderRadius="md">
                  <Text>{question.correct_answer}</Text>
                </Box>
              </Box>
            )}

            {question.model_answer && (
              <Box mt={4}>
                <Heading size="xs" mb={2}>
                  Model Answer
                </Heading>
                <Box p={3} bg="blue.50" borderRadius="md">
                  <Text>{question.model_answer}</Text>
                </Box>
              </Box>
            )}
          </Box>
        </Accordion.ItemContent>
      </Box>
    </Accordion.Item>
  )
}

export default QuestionsList 