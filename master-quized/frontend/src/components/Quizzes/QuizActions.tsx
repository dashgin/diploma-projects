import type { QuizRead } from "@/client"
import { CreateAssignment } from "@/components/Assignments"
import { Flex } from "@chakra-ui/react"
import EditQuiz from "./EditQuiz"

interface QuizActionsProps {
  quiz: QuizRead
}

export const QuizActions = ({ quiz }: QuizActionsProps) => {
  return (
    <Flex gap={2}>
      <CreateAssignment quizId={quiz.id} />
      <EditQuiz quiz={quiz} />
    </Flex>
  )
}
