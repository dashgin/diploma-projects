import { useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import { useMutation, useQuery } from "@tanstack/react-query";
import { 
  Button, 
  VStack, 
  Heading, 
  Text, 
  Box, 
  Card, 
  CardBody, 
  CardFooter,
  useDisclosure,
  Spinner,
  Center,
  Alert,
} from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { QuizzesService, AttemptsService } from "../../../../client/sdk.gen";
import * as Dialog from "../../../../components/ui/dialog";

export const Route = createFileRoute("/_layout/quizzes/$quizId/take")({
  component: QuizTakePage,
});

function QuizTakePage() {
  const { quizId } = Route.useParams();
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const disclosure = useDisclosure();

  // Fetch quiz details
  const { data: quiz, isLoading: isLoadingQuiz, error: quizError } = useQuery({
    queryKey: ["quiz", quizId],
    queryFn: () => QuizzesService.readQuiz({ quizId: Number(quizId) }),
  });

  // Create attempt mutation
  const createAttemptMutation = useMutation({
    mutationFn: () => {
      setIsSubmitting(true);
      return AttemptsService.createAttempt({
        requestBody: {
          quiz_id: Number(quizId),
          student_id: 0, // This will be replaced by the current user's ID on the server
          is_completed: false,
        },
      });
    },
    onSuccess: (data) => {
      setIsSubmitting(false);
      navigate({ to: `/attempts/${data.id}` });
    },
    onError: (error) => {
      setIsSubmitting(false);
      console.error("Error creating attempt:", error);
    },
  });

  // Handle start quiz
  const handleStartQuiz = () => {
    createAttemptMutation.mutate();
  };

  if (isLoadingQuiz) {
    return (
      <Center h="50vh">
        <Spinner size="xl" />
      </Center>
    );
  }

  if (quizError) {
    return (
      <Alert status="error" borderRadius="md">
        There was an error loading this quiz. Please try again later.
      </Alert>
    );
  }

  return (
    <VStack spacing={6} align="stretch" w="full" maxW="800px" mx="auto" py={8}>
      <Heading as="h1" size="xl">
        {quiz?.title}
      </Heading>

      <Card variant="outline">
        <CardBody>
          <VStack spacing={4} align="start">
            <Heading as="h2" size="md">
              Instructions
            </Heading>
            <Text>{quiz?.instructions || "No specific instructions provided for this quiz."}</Text>
            
            <Box borderTop="1px" borderColor="gray.200" pt={4} width="100%">
              <Text fontWeight="bold">Before you begin:</Text>
              <Text>• Make sure you have enough time to complete the quiz</Text>
              <Text>• Your answers will be saved automatically as you progress</Text>
              <Text>• You can navigate between questions freely</Text>
              <Text>• Submit your quiz when you're finished</Text>
            </Box>
          </VStack>
        </CardBody>
        <CardFooter justifyContent="center">
          <Button 
            colorScheme="blue" 
            onClick={disclosure.onOpen}
            size="lg"
            isLoading={isSubmitting}
          >
            Start Quiz
          </Button>
        </CardFooter>
      </Card>

      {/* Confirmation Dialog */}
      <Dialog.DialogRoot open={disclosure.open} onOpenChange={disclosure.setOpen}>
        <Dialog.DialogContent>
          <Dialog.DialogHeader>
            <Dialog.DialogTitle>Start Quiz</Dialog.DialogTitle>
            <Dialog.DialogCloseTrigger />
          </Dialog.DialogHeader>
          <Dialog.DialogBody>
            Are you ready to start this quiz? Once started, your attempt will be recorded.
          </Dialog.DialogBody>
          <Dialog.DialogFooter>
            <Button 
              colorScheme="blue" 
              onClick={handleStartQuiz}
              isLoading={isSubmitting}
            >
              Start Now
            </Button>
          </Dialog.DialogFooter>
        </Dialog.DialogContent>
      </Dialog.DialogRoot>
    </VStack>
  );
} 