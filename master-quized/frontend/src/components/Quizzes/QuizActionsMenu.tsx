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
      <MenuTrigger>
        <IconButton variant="ghost" color="inherit">
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
