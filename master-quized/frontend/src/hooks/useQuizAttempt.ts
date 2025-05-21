import { useState, useEffect } from 'react';
import { useNavigate } from '@tanstack/react-router';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { 
  AttemptsService, 
  QuestionsService, 
  ResponsesService 
} from '../client/sdk.gen';
import useCustomToast from './useCustomToast';

export function useQuizAttempt(attemptId: number | string) {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { showSuccessToast, showErrorToast } = useCustomToast();
  
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [responses, setResponses] = useState<Record<number, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Convert attemptId to number if it's a string
  const attemptIdNumber = typeof attemptId === 'string' ? Number(attemptId) : attemptId;

  // Fetch attempt data
  const { data: attempt, isLoading: isLoadingAttempt } = useQuery({
    queryKey: ["attempt", attemptIdNumber],
    queryFn: () => AttemptsService.readAttempt({ attemptId: attemptIdNumber }),
  });

  // Fetch questions for this quiz
  const { data: questions, isLoading: isLoadingQuestions } = useQuery({
    queryKey: ["questions", attempt?.quiz_id],
    queryFn: () => QuestionsService.readQuestionsByQuiz({ 
      quizId: attempt?.quiz_id || 0,
      limit: 100,
    }),
    enabled: !!attempt?.quiz_id,
  });

  // Fetch existing responses
  const { data: existingResponses, isLoading: isLoadingResponses } = useQuery({
    queryKey: ["responses", attemptIdNumber],
    queryFn: () => ResponsesService.readResponsesByAttempt({
      attemptId: attemptIdNumber,
      limit: 100,
    }),
    enabled: !!attemptIdNumber,
  });

  // Submit response mutation
  const submitResponseMutation = useMutation({
    mutationFn: (data: { questionId: number; answer: string }) => {
      return ResponsesService.createResponse({
        requestBody: {
          attempt_id: attemptIdNumber,
          question_id: data.questionId,
          answer_text: data.answer,
          selected_option_id: null, // This would be set for multiple-choice questions
        },
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["responses", attemptIdNumber] });
    },
    onError: (error) => {
      console.error("Error saving response:", error);
      showErrorToast("Failed to save response");
    },
  });

  // Complete attempt mutation
  const completeAttemptMutation = useMutation({
    mutationFn: () => {
      setIsSubmitting(true);
      return AttemptsService.completeAttempt({
        attemptId: attemptIdNumber,
        score: null, // Score will be calculated on the server
      });
    },
    onSuccess: (data) => {
      setIsSubmitting(false);
      showSuccessToast("Quiz submitted successfully");
      navigate({ to: `/quizzes/${data.quiz_id}` });
    },
    onError: (error) => {
      setIsSubmitting(false);
      console.error("Error completing attempt:", error);
      showErrorToast("Failed to submit quiz");
    },
  });

  // Initialize responses from existing data
  useEffect(() => {
    if (existingResponses && existingResponses.length > 0) {
      const savedResponses: Record<number, string> = {};
      existingResponses.forEach((response) => {
        savedResponses[response.question_id] = response.answer_text;
      });
      setResponses(savedResponses);
    }
  }, [existingResponses]);

  // Handle response change
  const handleResponseChange = (questionId: number, answer: string) => {
    setResponses((prev) => ({ ...prev, [questionId]: answer }));
  };

  // Save current response
  const saveCurrentResponse = (questionId: number) => {
    const answer = responses[questionId] || "";
    
    if (answer.trim()) {
      submitResponseMutation.mutate({ questionId, answer });
    }
  };

  // Navigate to next question
  const handleNext = () => {
    if (!questions?.data?.[currentQuestionIndex]) return;
    
    saveCurrentResponse(questions.data[currentQuestionIndex].id);
    if (questions && currentQuestionIndex < questions.data.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  // Navigate to previous question
  const handlePrevious = () => {
    if (!questions?.data?.[currentQuestionIndex]) return;
    
    saveCurrentResponse(questions.data[currentQuestionIndex].id);
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  // Navigate to specific question
  const handleQuestionSelect = (index: number) => {
    if (!questions?.data?.[currentQuestionIndex]) return;
    
    saveCurrentResponse(questions.data[currentQuestionIndex].id);
    setCurrentQuestionIndex(index);
  };

  // Submit quiz
  const handleSubmitQuiz = () => {
    if (questions?.data?.[currentQuestionIndex]) {
      saveCurrentResponse(questions.data[currentQuestionIndex].id);
    }
    completeAttemptMutation.mutate();
  };

  return {
    attempt,
    questions,
    existingResponses,
    currentQuestionIndex,
    responses,
    isSubmitting,
    isLoading: isLoadingAttempt || isLoadingQuestions || isLoadingResponses,
    handleResponseChange,
    saveCurrentResponse,
    handleNext,
    handlePrevious,
    handleQuestionSelect,
    handleSubmitQuiz,
  };
} 