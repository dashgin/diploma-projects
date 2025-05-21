import {
  Accordion,
  Box,
  Flex,
  HStack,
  Heading,
  Spinner,
  Text,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"

import {
  OptionsService,
  type QuestionRead,
  QuestionsService,
} from "@/client"
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
    data: questionsResponse,
    isLoading: isQuestionsLoading,
    error: questionsError,
  } = useQuery({
    queryKey: ["questions", quizId],
    queryFn: () => QuestionsService.readQuestionsByQuiz({ quizId }),
  })

  // Handle the new pagination format with data and count fields
  const questionsData = questionsResponse?.data || []

  // Ensure questions is always an array
  const questions = Array.isArray(questionsData) ? questionsData : []

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
          <QuestionItem key={question.id} question={question} index={index} />
        ))}
      </Accordion.Root>
    </Box>
  )
}

// Component for a single question item with options
const QuestionItem = ({
  question,
  index,
}: { question: QuestionRead; index: number }) => {
  // Fetch options if question is multiple choice
  const { data: optionsResponse, isLoading: isOptionsLoading } = useQuery({
    queryKey: ["options", question.id],
    queryFn: () =>
      OptionsService.readOptionsByQuestion({ questionId: question.id }),
    enabled: question.question_type === "multiple_choice",
  })

  // Handle the new pagination format with data and count fields
  const optionsData = optionsResponse?.data || []

  // Ensure options is always an array
  const options = Array.isArray(optionsData) ? optionsData : []

  return (
    <Accordion.Item value={index.toString()}>
      <Box borderWidth="1px" mb={3} overflow="hidden" borderRadius="md">
        <Accordion.ItemTrigger p={4}>
          <Flex justify="space-between" align="center" width="100%">
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
            <HStack gap={2}>
              <EditQuestion question={question} />
              <DeleteQuestion question={question} />
            </HStack>
          </Flex>
        </Accordion.ItemTrigger>
        <Accordion.ItemContent>
          <Box p={4} borderTopWidth="1px">
            <Text fontWeight="bold" mb={2}>
              Question:
            </Text>
            <Text mb={4}>{question.text}</Text>

            {question.question_type === "multiple_choice" && (
              <>
                <Flex justify="space-between" align="center" mb={2}>
                  <Text fontWeight="bold">Options:</Text>
                  <AddOption questionId={question.id} />
                </Flex>
                {isOptionsLoading ? (
                  <Spinner size="sm" />
                ) : (
                  <Box>
                    {options.map((option) => (
                      <Box
                        key={option.id}
                        p={2}
                        mb={1}
                        borderRadius="md"
                        borderWidth="1px"
                        display="flex"
                        alignItems="center"
                        justifyContent="space-between"
                        bg={option.is_correct ? "green.50" : "gray.50"}
                      >
                        <Text>
                          {option.is_correct && "✓ "}
                          {option.text}
                        </Text>
                        <HStack gap={2}>
                          <EditOption option={option} />
                          <DeleteOption option={option} />
                        </HStack>
                      </Box>
                    ))}
                    {options.length === 0 && (
                      <Text color="gray.500">No options defined</Text>
                    )}
                  </Box>
                )}
              </>
            )}

            {question.model_answer && (
              <>
                <Text fontWeight="bold" mt={4} mb={2}>
                  Model Answer:
                </Text>
                <Text>{question.model_answer}</Text>
              </>
            )}
          </Box>
        </Accordion.ItemContent>
      </Box>
    </Accordion.Item>
  )
}

export default QuestionsList
