import { useQuery } from "@tanstack/react-query"
import { QuizzesService } from "../client"

export function useQuizzes() {
  return useQuery({
    queryKey: ["quizzes"],
    queryFn: () => QuizzesService.readQuizzes(),
  })
} 