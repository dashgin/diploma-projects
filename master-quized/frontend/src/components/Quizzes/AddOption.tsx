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
import { FiPlus } from "react-icons/fi"

import { type ApiError, type OptionCreate, OptionsService } from "@/client"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"
import { Checkbox } from "../ui/checkbox"
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

interface AddOptionProps {
  questionId: number
}

interface OptionCreateForm {
  text: string
  is_correct?: boolean
  order_position?: number
}

const AddOption = ({ questionId }: AddOptionProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<OptionCreateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      is_correct: false,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: OptionCreate) =>
      OptionsService.createOption({
        requestBody: { ...data, question_id: questionId },
      }),
    onSuccess: () => {
      showSuccessToast("Option created successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["options", questionId] })
    },
  })

  const onSubmit: SubmitHandler<OptionCreateForm> = async (data) => {
    mutation.mutate(data as OptionCreate)
  }

  return (
    <DialogRoot
      size={{ base: "xs", md: "sm" }}
      placement="center"
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger>
        <Button variant="outline" size="sm">
          <FiPlus />
          Add Option
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Add Option</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Create a new option for this question.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.text}
                errorText={errors.text?.message}
                label="Option Text"
              >
                <Input
                  id="text"
                  {...register("text", {
                    required: "Option text is required.",
                  })}
                  placeholder="Enter the option text"
                />
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

              <Field
                invalid={!!errors.is_correct}
                errorText={errors.is_correct?.message}
                label="Correct Answer"
              >
                <Checkbox id="is_correct" {...register("is_correct")}>
                  This is the correct answer
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

export default AddOption 