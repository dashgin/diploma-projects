import {
  Button,
  DialogActionTrigger,
  Flex,
  IconButton,
  Text,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { FiTrash } from "react-icons/fi"

import { type ApiError, type QuestionRead, QuestionsService } from "@/client"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"
import {
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog"

interface DeleteQuestionProps {
  question: QuestionRead
  useIcon?: boolean
}

const DeleteQuestion = ({ question, useIcon = false }: DeleteQuestionProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()

  const mutation = useMutation({
    mutationFn: () =>
      QuestionsService.deleteQuestion({
        questionId: question.id,
      }),
    onSuccess: () => {
      showSuccessToast("Question deleted successfully.")
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: ["questions", question.quiz_id],
      })
    },
  })

  const handleDelete = () => {
    mutation.mutate()
  }

  return (
    <DialogRoot
      size={{ base: "xs", md: "sm" }}
      placement="center"
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger asChild>
        {useIcon ? (
          <Flex
            as="span"
            role="button"
            aria-label="Delete Question"
            display="inline-flex"
            alignItems="center"
            justifyContent="center"
            fontSize="sm"
            color="red.500"
            _hover={{ color: "red.700" }}
            cursor="pointer"
          >
            <FiTrash />
          </Flex>
        ) : (
          <Flex
            as="span"
            align="center"
            gap={1}
            cursor="pointer"
            px={2}
            py={1}
            color="red.500"
          >
            <FiTrash />
            Delete
          </Flex>
        )}
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Delete Question</DialogTitle>
        </DialogHeader>
        <DialogBody>
          <Text>
            Are you sure you want to delete this question? This action cannot be
            undone.
          </Text>
        </DialogBody>
        <DialogFooter gap={2}>
          <DialogActionTrigger asChild>
            <Button variant="subtle" colorPalette="gray">
              Cancel
            </Button>
          </DialogActionTrigger>
          <Button
            variant="solid"
            colorPalette="red"
            onClick={handleDelete}
            loading={mutation.isPending}
          >
            Delete
          </Button>
        </DialogFooter>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default DeleteQuestion
