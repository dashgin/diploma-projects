import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"

import type { QuizRead } from "@/client"
import DeleteQuiz from "./DeleteQuiz"
import EditQuiz from "./EditQuiz"

interface QuizActionsMenuProps {
  quiz: QuizRead
}

export const QuizActionsMenu = ({ quiz }: QuizActionsMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton
          aria-label="Quiz actions"
          variant="ghost"
          color="inherit"
          size="sm"
        >
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <EditQuiz quiz={quiz} />
        <DeleteQuiz id={quiz.id} />
      </MenuContent>
    </MenuRoot>
  )
}
