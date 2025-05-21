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
  VStack,
  useDisclosure,
  Alert,
} from "@chakra-ui/react";
import * as Dialog from "../../../../components/ui/dialog";
import { OptionsService } from "../../../../client/sdk.gen";
import { useQuizAttempt } from "../../../../hooks/useQuizAttempt";
import { useQuery } from "@tanstack/react-query";
import QuestionRenderer from "../../../../components/Quizzes/QuestionRenderer";

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
    responses,
    currentQuestionIndex,
    isSubmitting,
    isLoading,
    handleResponseChange,
    handleNext,
    handlePrevious,
    handleQuestionSelect,
    handleSubmitQuiz,
  } = useQuizAttempt(attemptId);

  // Fetch options for the current question
  const currentQuestionId = questions?.data?.[currentQuestionIndex]?.id;
  const { data: optionsData, isLoading: isLoadingOptions } = useQuery({
    queryKey: ["options", currentQuestionId],
    queryFn: () => 
      OptionsService.readOptionsByQuestion({ 
        questionId: currentQuestionId || 0, 
        limit: 20 
      }),
    enabled: !!currentQuestionId,
  });

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
    return (
      <Container maxW="container.lg" py={8}>
        <Alert status="info">
          This quiz attempt has already been completed.
        </Alert>
        <Button 
          mt={4} 
          onClick={() => navigate({ to: `/quizzes/${attempt.quiz_id}` })}
        >
          Return to Quiz
        </Button>
      </Container>
    );
  }

  // Current question
  const currentQuestion = questions?.data?.[currentQuestionIndex];
  const questionOptions = optionsData?.data || [];
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
        <Progress value={progress} size="sm" colorScheme="blue" borderRadius="md" />
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
            <VStack align="stretch" spacing={2}>
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
            </VStack>
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
                  options={questionOptions}
                  value={responses[currentQuestion.id] || ""}
                  onChange={handleResponseChange}
                />
              )}

              {/* Navigation Buttons */}
              <HStack mt={8} justifyContent="space-between">
                <Button 
                  onClick={handlePrevious} 
                  isDisabled={currentQuestionIndex === 0}
                >
                  Previous
                </Button>
                <Button 
                  onClick={handleNext} 
                  isDisabled={currentQuestionIndex === totalQuestions - 1}
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
      <Dialog.DialogRoot open={disclosure.open} onOpenChange={disclosure.setOpen}>
        <Dialog.DialogContent>
          <Dialog.DialogHeader>
            <Dialog.DialogTitle>Submit Quiz</Dialog.DialogTitle>
            <Dialog.DialogCloseTrigger />
          </Dialog.DialogHeader>
          <Dialog.DialogBody>
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
          </Dialog.DialogBody>
          <Dialog.DialogFooter>
            <Button 
              colorScheme="blue" 
              onClick={handleSubmitQuiz}
              loading={isSubmitting}
            >
              Submit Quiz
            </Button>
          </Dialog.DialogFooter>
        </Dialog.DialogContent>
      </Dialog.DialogRoot>
    </Container>
  );
} 