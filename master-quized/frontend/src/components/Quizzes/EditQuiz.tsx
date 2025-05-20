import {
  Button,
  DialogActionTrigger,
  Input,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FiEdit } from "react-icons/fi"

import { type ApiError, type QuizRead, QuizzesService } from "@/client"
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
import { Field } from "../ui/field"
import { Checkbox } from "../ui/checkbox"

interface EditQuizProps {
  quiz: QuizRead
}

interface QuizUpdateForm {
  title?: string
  instructions?: string
  is_active?: boolean
}

const EditQuiz = ({ quiz }: EditQuizProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<QuizUpdateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      title: quiz.title,
      instructions: quiz.instructions ?? undefined,
      is_active: quiz.is_active,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: QuizUpdateForm) =>
      QuizzesService.updateQuiz({ quizId: quiz.id, requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Quiz updated successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["quizzes"] })
    },
  })

  const onSubmit: SubmitHandler<QuizUpdateForm> = async (data) => {
    mutation.mutate(data)
  }

  return (
    <DialogRoot
      size={{ base: "xs", md: "md" }}
      placement="center"
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger>
        <Button variant="ghost" size="sm">
          <FiEdit fontSize="16px" />
          Edit Quiz
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Quiz</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Update the quiz details.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.title}
                errorText={errors.title?.message}
                label="Title"
              >
                <Input
                  id="title"
                  {...register("title", {
                    required: "Title is required.",
                  })}
                  placeholder="Quiz Title"
                  type="text"
                />
              </Field>

              <Field
                invalid={!!errors.instructions}
                errorText={errors.instructions?.message}
                label="Instructions"
              >
                <Input
                  id="instructions"
                  {...register("instructions")}
                  placeholder="Quiz Instructions"
                  type="text"
                />
              </Field>

              <Field
                invalid={!!errors.is_active}
                errorText={errors.is_active?.message}
                label="Active Status"
              >
                <Checkbox
                  id="is_active"
                  {...register("is_active")}
                >
                  Make quiz active
                </Checkbox>
              </Field>
            </VStack>
          </DialogBody>

          <DialogFooter gap={2}>
            <DialogActionTrigger>
              <Button
                variant="subtle"
                colorPalette="gray"
                disabled={isSubmitting}
              >
                Cancel
              </Button>
            </DialogActionTrigger>
            <Button
              variant="solid"
              type="submit"
              loading={isSubmitting}
            >
              Save
            </Button>
          </DialogFooter>
        </form>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default EditQuiz 