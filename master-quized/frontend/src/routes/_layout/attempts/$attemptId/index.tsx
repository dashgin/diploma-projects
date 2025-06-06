import { createFileRoute, useNavigate } from "@tanstack/react-router";
import {
  Box,
  Button,
  Center,
  Container,
  Flex,
  Grid,
  GridItem,
  Heading,
  HStack,
  Progress,
  Spinner,
  Text,
  Stack,
  useDisclosure,
  Dialog,
  Portal,
  CloseButton,
  Badge,
  Separator,
  Card
} from "@chakra-ui/react";
import { OptionsService, ResponsesService } from "../../../../client/sdk.gen";
import { useQuizAttempt } from "../../../../hooks/useQuizAttempt";
import { useQuery } from "@tanstack/react-query";
import QuestionRenderer from "../../../../components/Quizzes/QuestionRenderer";
import { formatDate } from "../../../../utils/formatters";
import { AIFeedbackButton, AIFeedbackDisplay } from "../../../../components/Feedback";

export const Route = createFileRoute("/_layout/attempts/$attemptId/")({
  component: AttemptPage,
});

function AttemptPage() {
  const { attemptId } = Route.useParams();
  const navigate = useNavigate();
  const disclosure = useDisclosure();
  
  const {
    attempt,
    questions,
    attemptResponsesData,
    currentQuestionIndex,
    isSubmitting,
    isLoading,
    handleResponseChange,
    handleNext,
    handlePrevious,
    handleQuestionSelect,
    handleSubmitQuiz,
    responses,
  } = useQuizAttempt(attemptId);

  // Fetch options for the current question
  const currentQuestionId = questions?.data?.[currentQuestionIndex]?.id;
  const currentQuestionType = questions?.data?.[currentQuestionIndex]?.question_type;
  
  const { data: optionsData, isLoading: isLoadingOptions } = useQuery({
    queryKey: ["options", currentQuestionId],
    queryFn: () => 
      OptionsService.readOptionsByQuestion({ 
        questionId: currentQuestionId || 0, 
        limit: 20 
      }),
    enabled: !!currentQuestionId && currentQuestionType === "multiple_choice",
  });

  // Debug options data
  console.log("Current question type:", currentQuestionType);
  console.log("Options data:", optionsData);

  // Loading state
  if (isLoading) {
    return (
      <Center height="50vh">
        <Spinner size="xl" />
      </Center>
    );
  }

  // Check if attempt is already completed
  if (attempt?.is_completed) {
    const isLoadingCompletedAttemptData = !attemptResponsesData;
    
    if (isLoadingCompletedAttemptData) {
      return (
        <Center height="50vh">
          <Spinner size="xl" />
        </Center>
      );
    }
    
    // Get attempt summary data
    const attemptSummary = attemptResponsesData?.attempt;
    const responseDetails = attemptResponsesData?.responses || [];
    
    // Create a map of responses by question ID for easier lookup
    const responsesByQuestionId: Record<number, any> = {};
    responseDetails.forEach(response => {
      responsesByQuestionId[response.question.id] = response;
    });
    
    return (
      <Container maxW="container.lg" py={8}>
        <Box mb={6}>
          <Flex justifyContent="space-between" alignItems="center">
            <Heading size="lg">Attempt Results</Heading>
            <Button 
              onClick={() => navigate({ to: `/quizzes/${attempt.quiz_id}` })}
              variant="outline"
            >
              Return to Quiz
            </Button>
          </Flex>
          
          <Grid templateColumns={{ base: "1fr", md: "repeat(3, 1fr)" }} gap={4} mt={6}>
            <Card.Root>
              <Card.Body>
                <Text fontWeight="bold">Score</Text>
                <Text fontSize="3xl" color={(attemptSummary?.score ?? 0) >= 70 ? "green.500" : "red.500"}>
                  {attemptSummary?.score !== undefined ? `${Math.round(attemptSummary.score)}%` : "Not scored"}
                </Text>
              </Card.Body>
            </Card.Root>
            
            <Card.Root>
              <Card.Body>
                <Text fontWeight="bold">Started</Text>
                <Text>{formatDate(attempt.started_at)}</Text>
              </Card.Body>
            </Card.Root>
            
            <Card.Root>
              <Card.Body>
                <Text fontWeight="bold">Completed</Text>
                <Text>{formatDate(attempt.completed_at)}</Text>
              </Card.Body>
            </Card.Root>
          </Grid>
          
          <Card.Root mt={6}>
            <Card.Body>
              <Flex gap={6} wrap="wrap">
                <Box>
                  <Text fontWeight="bold">Total Questions</Text>
                  <Text>{attemptSummary?.total_questions || 0}</Text>
                </Box>
                <Box>
                  <Text fontWeight="bold">Correct Answers</Text>
                  <Text>{attemptSummary?.correct_answers || 0}</Text>
                </Box>
              </Flex>
            </Card.Body>
          </Card.Root>
        </Box>
        
        <Separator my={6} />
        
        <Box>
          <Heading size="md" mb={6}>Question Results</Heading>
          
          {questions?.data.map((question, index) => {
            const responseData = responsesByQuestionId[question.id];
            const isCorrect = responseData?.answer?.is_correct;
            
            return (
              <Card.Root key={question.id} mb={6} variant="outline">
                <Card.Header>
                  <Flex justify="space-between" align="center">
                    <Text fontWeight="bold">Question {index + 1}</Text>
                    {isCorrect !== undefined && (
                      <Badge colorScheme={isCorrect ? "green" : "red"}>
                        {isCorrect ? "Correct" : "Incorrect"}
                      </Badge>
                    )}
                  </Flex>
                </Card.Header>
                <Card.Body>
                  <Text mb={4}>{question.text}</Text>
                  
                  <Box mb={4}>
                    <Text fontWeight="bold" fontSize="sm" color="gray.600">Your Answer:</Text>
                    {responseData?.answer?.type === "multiple_choice" && typeof responseData.answer.answer === "object" ? (
                      <Text>{responseData.answer.answer.text || "Not answered"}</Text>
                    ) : (
                      <Text>{responseData?.answer?.answer || "Not answered"}</Text>
                    )}
                  </Box>
                  
                  {/* Display all options for multiple choice questions */}
                  {responseData?.question?.question_type === "multiple_choice" && responseData.question.options && (
                    <Box mt={4}>
                      <Text fontWeight="bold" fontSize="sm" color="gray.600">All Options:</Text>
                      {responseData.question.options.map((option: any, idx: number) => (
                        <Flex key={idx} gap={2} mt={1}>
                          <Badge colorScheme={option.is_correct ? "green" : responseData.answer.answer.option_id === option.id ? "blue" : "gray"}>
                            {option.is_correct ? "✓" : responseData.answer.answer.option_id === option.id ? "•" : ""}
                          </Badge>
                          <Text>{option.text}</Text>
                        </Flex>
                      ))}
                    </Box>
                  )}
                  
                  {responseData?.explanation && (
                    <Box mt={4} p={3} bg="gray.50" borderRadius="md">
                      <Text fontWeight="bold" fontSize="sm">Explanation:</Text>
                      <Text>{responseData.explanation}</Text>
                    </Box>
                  )}
                  
                  {/* AI Feedback section - for text-based questions */}
                  {(responseData?.question?.question_type === "open_ended" || responseData?.question?.question_type === "text") && (
                    <Box mt={4}>
                      <Flex justifyContent="space-between" alignItems="center" mb={2}>
                        <Text fontWeight="bold" fontSize="sm" color="gray.600">AI Feedback:</Text>
                        <AIFeedbackButton responseId={responseData.id} />
                      </Flex>
                      <AIFeedbackDisplay responseId={responseData.id} />
                    </Box>
                  )}
                </Card.Body>
              </Card.Root>
            );
          })}
        </Box>
      </Container>
    );
  }

  // Current question
  const currentQuestion = questions?.data?.[currentQuestionIndex];
  // Ensure we handle the nested data structure correctly
  const questionOptions = optionsData?.data || [];
  console.log("Processed question options:", questionOptions);
  const totalQuestions = questions?.data.length || 0;
  const progress = totalQuestions ? ((currentQuestionIndex + 1) / totalQuestions) * 100 : 0;

  return (
    <Container maxW="container.xl" py={4}>
      {/* Quiz Header */}
      <Flex justifyContent="space-between" alignItems="center" mb={4}>
        <Heading size="md">Quiz Attempt</Heading>
        <Button 
          colorScheme="blue" 
          onClick={disclosure.onOpen}
        >
          Submit Quiz
        </Button>
      </Flex>

      {/* Progress Bar */}
      <Box mb={6}>
        <Progress.Root size="sm" colorScheme="blue" borderRadius="md" value={progress}>
          <Progress.Track>
            <Progress.Range />
          </Progress.Track>
        </Progress.Root>
        <Text mt={1} fontSize="sm">
          Question {currentQuestionIndex + 1} of {totalQuestions}
        </Text>
      </Box>

      {/* Main Content */}
      <Grid templateColumns={{ base: "1fr", md: "1fr 3fr" }} gap={6}>
        {/* Question Navigator */}
        <GridItem>
          <Box 
            p={4} 
            borderWidth="1px" 
            borderRadius="md" 
            height="fit-content"
            position="sticky"
            top="4"
          >
            <Heading size="sm" mb={4}>Questions</Heading>
            <Stack direction="column" gap={2}>
              {questions?.data.map((question, index) => (
                <Button
                  key={question.id}
                  variant={index === currentQuestionIndex ? "solid" : "outline"}
                  colorScheme={index === currentQuestionIndex ? "blue" : 
                    responses[question.id] ? "green" : "gray"}
                  justifyContent="flex-start"
                  size="sm"
                  onClick={() => handleQuestionSelect(index)}
                >
                  {index + 1}. {question.text.length > 20 
                    ? `${question.text.substring(0, 20)}...` 
                    : question.text}
                </Button>
              ))}
            </Stack>
          </Box>
        </GridItem>

        {/* Question Content */}
        <GridItem>
          {isLoadingOptions ? (
            <Center py={10}>
              <Spinner />
            </Center>
          ) : (
            <Box p={6} borderWidth="1px" borderRadius="md">
              <Heading size="md" mb={4}>
                {currentQuestion?.text}
              </Heading>

              {/* Question Type Renderer */}
              {currentQuestion && (
                <QuestionRenderer 
                  questionType={currentQuestion.question_type}
                  questionId={currentQuestion.id}
                  options={currentQuestion.question_type === "multiple_choice" ? questionOptions : []}
                  value={responses[currentQuestion.id] || ""}
                  onChange={handleResponseChange}
                />
              )}

              {/* Navigation Buttons */}
              <HStack mt={8} justifyContent="space-between">
                <Button 
                  onClick={handlePrevious} 
                  disabled={currentQuestionIndex === 0}
                >
                  Previous
                </Button>
                <Button 
                  onClick={handleNext} 
                  disabled={currentQuestionIndex === totalQuestions - 1}
                  colorScheme="blue"
                >
                  Next
                </Button>
              </HStack>
            </Box>
          )}
        </GridItem>
      </Grid>

      {/* Submit Confirmation Dialog */}
      <Dialog.Root open={disclosure.open} onOpenChange={(e) => disclosure.setOpen(e.open)}>
        <Portal>
          <Dialog.Backdrop />
          <Dialog.Positioner>
            <Dialog.Content>
              <Dialog.Header>
                <Dialog.Title>Submit Quiz</Dialog.Title>
                <Dialog.CloseTrigger asChild>
                  <CloseButton size="sm" />
                </Dialog.CloseTrigger>
              </Dialog.Header>
              <Dialog.Body>
                <Text>
                  Are you sure you want to submit this quiz? 
                  You won't be able to change your answers after submission.
                </Text>
                
                {/* Response status */}
                {totalQuestions > 0 && (
                  <Box mt={4}>
                    <Text fontWeight="medium">Question Status:</Text>
                    <Text>
                      {Object.keys(responses).length} of {totalQuestions} questions answered
                    </Text>
                    {Object.keys(responses).length < totalQuestions && (
                      <Text color="orange.500" mt={1}>
                        You have unanswered questions.
                      </Text>
                    )}
                  </Box>
                )}
              </Dialog.Body>
              <Dialog.Footer>
                <Button 
                  colorScheme="blue" 
                  onClick={handleSubmitQuiz}
                  loading={isSubmitting}
                >
                  Submit Quiz
                </Button>
              </Dialog.Footer>
            </Dialog.Content>
          </Dialog.Positioner>
        </Portal>
      </Dialog.Root>
    </Container>
  );
} 