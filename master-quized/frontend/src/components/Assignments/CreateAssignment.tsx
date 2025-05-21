import {
  Button,
  DialogActionTrigger,
  Flex,
  Input,
  Select,
  Spinner,
  Text,
  VStack,
  createListCollection,
} from "@chakra-ui/react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FiPlus } from "react-icons/fi"

import {
  type ApiError,
  type AssignmentCreate,
  AssignmentsService,
  UsersService,
} from "@/client"
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

interface CreateAssignmentProps {
  quizId: number
}

interface AssignmentCreateForm {
  student_id: number
  quiz_id: number
  due_date?: string
  class_id?: number
}

const CreateAssignment = ({ quizId }: CreateAssignmentProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()

  const { data: studentsData, isLoading: isLoadingStudents } = useQuery({
    queryKey: ["users", "students"],
    queryFn: () => UsersService.readUsers({ limit: 100 }),
  })

  // Extract student users from the pagination format
  const students =
    studentsData?.data.filter(
      (user) => user.role === "student" || !user.role,
    ) || []

  const studentCollection = createListCollection({
    items: students
      ? students.map((student) => ({
          value: student.id.toString(),
          label: student.full_name || student.email,
        }))
      : [],
  })

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<AssignmentCreateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      quiz_id: quizId,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: AssignmentCreate) =>
      AssignmentsService.createAssignment({ requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Assignment created successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["assignments"] })
    },
  })

  const onSubmit: SubmitHandler<AssignmentCreateForm> = async (data) => {
    // Convert string to number for student_id if necessary
    const studentId =
      typeof data.student_id === "string"
        ? Number.parseInt(data.student_id, 10)
        : data.student_id

    mutation.mutate({
      ...data,
      student_id: studentId,
      quiz_id: quizId,
    } as AssignmentCreate)
  }

  if (isLoadingStudents) {
    return (
      <Flex justify="center" align="center" py={4}>
        <Spinner size="md" />
      </Flex>
    )
  }

  return (
    <DialogRoot
      size={{ base: "xs", md: "md" }}
      placement="center"
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger asChild>
        <Button variant="solid" size="sm">
          <FiPlus />
          Assign Quiz
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Assign Quiz</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Assign this quiz to a student.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.student_id}
                errorText={errors.student_id?.message}
                label="Student"
              >
                <Select.Root collection={studentCollection} id="student_id">
                  <Select.HiddenSelect
                    {...register("student_id", {
                      required: "Student is required.",
                    })}
                  />
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
                      {students?.map((student) => (
                        <Select.Item
                          item={{
                            value: student.id.toString(),
                            label: student.full_name || student.email,
                          }}
                          key={student.id}
                        >
                          {student.full_name || student.email}
                          <Select.ItemIndicator />
                        </Select.Item>
                      ))}
                    </Select.Content>
                  </Select.Positioner>
                </Select.Root>
              </Field>

              <Field
                invalid={!!errors.due_date}
                errorText={errors.due_date?.message}
                label="Due Date"
                helperText="Leave empty for no deadline"
              >
                <Input
                  id="due_date"
                  {...register("due_date")}
                  placeholder="Due date (optional)"
                  type="datetime-local"
                />
              </Field>
            </VStack>
          </DialogBody>

          <DialogFooter gap={2}>
            <DialogActionTrigger asChild>
              <Button
                variant="subtle"
                colorPalette="gray"
                disabled={isSubmitting}
              >
                Cancel
              </Button>
            </DialogActionTrigger>
            <Button variant="solid" type="submit" loading={isSubmitting}>
              Assign
            </Button>
          </DialogFooter>
        </form>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default CreateAssignment
