import {
  Button,
  DialogActionTrigger,
  Input,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm, Controller } from "react-hook-form"
import { FiEdit } from "react-icons/fi"

import {
  type ApiError,
  type OptionRead,
  type OptionUpdate,
  OptionsService,
} from "@/client"
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

interface EditOptionProps {
  option: OptionRead
}

interface OptionUpdateForm {
  text?: string
  is_correct?: boolean
  order_position?: number
}

const EditOption = ({ option }: EditOptionProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    control,
    formState: { errors, isSubmitting },
  } = useForm<OptionUpdateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      text: option.text,
      is_correct: option.is_correct,
      order_position: option.order_position ?? undefined,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: OptionUpdate) =>
      OptionsService.partiallyUpdateOption({
        optionId: option.id,
        requestBody: data,
      }),
    onSuccess: () => {
      showSuccessToast("Option updated successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: ["options", option.question_id],
      })
    },
  })

  const onSubmit: SubmitHandler<OptionUpdateForm> = async (data) => {
    mutation.mutate(data as OptionUpdate)
  }

  return (
    <DialogRoot
      size={{ base: "xs", md: "sm" }}
      placement="center"
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger>
        <Button variant="ghost" size="sm">
          <FiEdit />
          Edit
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Option</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Update the option details.</Text>
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
                <Controller
                  control={control}
                  name="is_correct"
                  render={({ field }) => (
                    <Checkbox
                      checked={field.value}
                      onCheckedChange={(val) => field.onChange(val)}
                    >
                      This is the correct answer
                    </Checkbox>
                  )}
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
              Save
            </Button>
          </DialogFooter>
        </form>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default EditOption
