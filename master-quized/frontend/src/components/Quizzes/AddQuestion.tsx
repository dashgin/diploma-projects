import {
  Button,
  createListCollection,
  DialogActionTrigger,
  Input,
  Select,
  Text,
  Textarea,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FiPlus } from "react-icons/fi"

import { type ApiError, type QuestionCreate, QuestionsService } from "@/client"
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

interface AddQuestionProps {
  quizId: number
}

interface QuestionCreateForm {
  text: string
  question_type: string
  order_position?: number
  correct_answer?: string
  model_answer?: string
}

const QUESTION_TYPES = [
  { value: "multiple_choice", label: "Multiple Choice" },
  { value: "short_answer", label: "Short Answer" },
  { value: "long_answer", label: "Long Answer" },
]

const questionTypeCollection = createListCollection({
  items: QUESTION_TYPES,
})


const AddQuestion = ({ quizId }: AddQuestionProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<QuestionCreateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      question_type: "multiple_choice",
    },
  })

  const questionType = watch("question_type")

  const mutation = useMutation({
    mutationFn: (data: QuestionCreate) =>
      QuestionsService.createQuestion({ requestBody: { ...data, quiz_id: quizId } }),
    onSuccess: () => {
      showSuccessToast("Question created successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["questions", quizId] })
    },
  })

  const onSubmit: SubmitHandler<QuestionCreateForm> = async (data) => {
    mutation.mutate(data as QuestionCreate)
  }

  return (
    <DialogRoot
      size={{ base: "xs", md: "md" }}
      placement="center"
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger>
        <Button variant="solid" size="sm">
          <FiPlus />
          Add Question
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Add New Question</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Create a new question for this quiz.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.text}
                errorText={errors.text?.message}
                label="Question Text"
              >
                <Textarea
                  id="text"
                  {...register("text", {
                    required: "Question text is required.",
                  })}
                  placeholder="Enter your question"
                />
              </Field>

              <Field
                required
                invalid={!!errors.question_type}
                errorText={errors.question_type?.message}
                label="Question Type"
              >
                <Select.Root collection={questionTypeCollection} id="question_type">
                  <Select.HiddenSelect {...register("question_type", { required: "Question type is required." })} />
                  <Select.Control>
                    <Select.Trigger>
                      <Select.ValueText />
                    </Select.Trigger>
                    <Select.IndicatorGroup>
                      <Select.Indicator />
                    </Select.IndicatorGroup>
                  </Select.Control>
                  <Select.Positioner>
                    <Select.Content>
                      {QUESTION_TYPES.map((type) => (
                        <Select.Item item={type} key={type.value}>
                          {type.label}
                          <Select.ItemIndicator />
                        </Select.Item>
                      ))}
                    </Select.Content>
                  </Select.Positioner>
                </Select.Root>
              </Field>

              <Field
                invalid={!!errors.order_position}
                errorText={errors.order_position?.message}
                label="Order Position"
              >
                <Input
                  id="order_position"
                  {...register("order_position", {
                    valueAsNumber: true,
                    min: { value: 1, message: "Order must be at least 1" },
                  })}
                  placeholder="Order position (optional)"
                  type="number"
                />
              </Field>

              {questionType !== "multiple_choice" && (
                <Field
                  invalid={!!errors.correct_answer}
                  errorText={errors.correct_answer?.message}
                  label="Correct Answer"
                  helperText="Provide the correct answer for auto-grading"
                >
                  <Textarea
                    id="correct_answer"
                    {...register("correct_answer")}
                    placeholder="Correct answer (optional)"
                  />
                </Field>
              )}

              <Field
                invalid={!!errors.model_answer}
                errorText={errors.model_answer?.message}
                label="Model Answer"
                helperText="Provide a model answer for reference"
              >
                <Textarea
                  id="model_answer"
                  {...register("model_answer")}
                  placeholder="Model answer (optional)"
                />
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
            <Button variant="solid" type="submit" loading={isSubmitting}>
              Create
            </Button>
          </DialogFooter>
        </form>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default AddQuestion 