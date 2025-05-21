import {
  Box,
  Button,
  Dialog,
  Field,
  Input,
  Select,
  Slider,
  Textarea,
  Tooltip,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import React from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { AreasService, RecommendationsService } from "../../client/sdk.gen"
import type { ResourceCreate } from "../../client/types.gen"
import useCustomToast from "../../hooks/useCustomToast"

interface ResourceModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  feedbackId: number
}

type ResourceFormValues = Omit<ResourceCreate, "relevance_score"> & {
  relevance_score_percentage?: number
}

const RESOURCE_TYPES = [
  { value: "article", label: "Article" },
  { value: "video", label: "Video" },
  { value: "book", label: "Book" },
  { value: "exercise", label: "Exercise" },
  { value: "tutorial", label: "Tutorial" },
  { value: "course", label: "Course" },
  { value: "documentation", label: "Documentation" },
]

export const ResourceModal: React.FC<ResourceModalProps> = ({
  open,
  onOpenChange,
  feedbackId,
}) => {
  const [sliderValue, setSliderValue] = React.useState(80)
  const [showTooltip, setShowTooltip] = React.useState(false)
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const queryClient = useQueryClient()

  // Fetch knowledge areas for the dropdown
  const { data: areasData } = useQuery({
    queryKey: ["areas"],
    queryFn: () => AreasService.readAreas({ limit: 100 }),
  })

  const {
    handleSubmit,
    register,
    reset,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<ResourceFormValues>({
    defaultValues: {
      feedback_id: feedbackId,
      title: "",
      description: "",
      url: "",
      resource_type: "article",
      area_id: undefined,
      relevance_score_percentage: 80,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: ResourceCreate) => {
      return RecommendationsService.createRecommendation({ requestBody: data })
    },
    onSuccess: () => {
      reset()
      showSuccessToast("Resource added successfully")
      queryClient.invalidateQueries({ queryKey: ["resources", feedbackId] })
      onOpenChange(false)
    },
    onError: (error) => {
      showErrorToast("Failed to add resource")
      console.error("Error adding resource:", error)
    },
  })

  const onSubmit: SubmitHandler<ResourceFormValues> = (data) => {
    // Convert percentage to decimal for the API
    const resourceData: ResourceCreate = {
      ...data,
      feedback_id: feedbackId,
      relevance_score: data.relevance_score_percentage
        ? data.relevance_score_percentage / 100
        : undefined,
    }
    ;(resourceData as any).relevance_score_percentage = undefined
    mutation.mutate(resourceData)
  }

  const handleSliderChange = (value: number) => {
    setSliderValue(value)
    setValue("relevance_score_percentage", value)
  }

  const handleClose = () => {
    reset()
    onOpenChange(false)
  }

  return (
    <Dialog.Root open={open} onOpenChange={handleClose}>
      <Dialog.Backdrop />
      <Dialog.Positioner>
        <Dialog.Content size="lg">
          <Dialog.Header>Add Learning Resource</Dialog.Header>
          <Dialog.CloseButton />

          <Dialog.Body>
            <Box as="form" id="resource-form" onSubmit={handleSubmit(onSubmit)}>
              <VStack gap={4} align="flex-start">
                <Field.Root invalid={!!errors.title} required>
                  <Field.Label htmlFor="title">Title</Field.Label>
                  <Input
                    id="title"
                    placeholder="Resource title"
                    {...register("title", {
                      required: "Title is required",
                      minLength: {
                        value: 3,
                        message: "Title must be at least 3 characters",
                      },
                    })}
                  />
                  <Field.ErrorText>{errors.title?.message}</Field.ErrorText>
                </Field.Root>

                <Field.Root invalid={!!errors.description}>
                  <Field.Label htmlFor="description">Description</Field.Label>
                  <Textarea
                    id="description"
                    placeholder="Brief description of the resource"
                    {...register("description")}
                  />
                  <Field.ErrorText>
                    {errors.description?.message}
                  </Field.ErrorText>
                </Field.Root>

                <Field.Root invalid={!!errors.url}>
                  <Field.Label htmlFor="url">URL</Field.Label>
                  <Input
                    id="url"
                    placeholder="https://example.com/resource"
                    {...register("url")}
                  />
                  <Field.ErrorText>{errors.url?.message}</Field.ErrorText>
                </Field.Root>

                <Field.Root invalid={!!errors.resource_type} required>
                  <Field.Label htmlFor="resource_type">
                    Resource Type
                  </Field.Label>
                  <Select.Root
                    id="resource_type"
                    {...register("resource_type", {
                      required: "Resource type is required",
                    })}
                  >
                    {RESOURCE_TYPES.map((type) => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </Select.Root>
                  <Field.ErrorText>
                    {errors.resource_type?.message}
                  </Field.ErrorText>
                </Field.Root>

                <Field.Root invalid={!!errors.area_id}>
                  <Field.Label htmlFor="area_id">Knowledge Area</Field.Label>
                  <Select.Root
                    id="area_id"
                    placeholder="Select knowledge area (optional)"
                    {...register("area_id", {
                      valueAsNumber: true,
                    })}
                  >
                    {areasData?.data.map((area) => (
                      <option key={area.id} value={area.id}>
                        {area.name}
                      </option>
                    ))}
                  </Select.Root>
                  <Field.ErrorText>{errors.area_id?.message}</Field.ErrorText>
                </Field.Root>

                <Field.Root>
                  <Field.Label htmlFor="relevance_score">
                    Relevance Score: {sliderValue}%
                  </Field.Label>
                  <Slider.Root
                    id="relevance_score"
                    min={0}
                    max={100}
                    step={5}
                    value={sliderValue}
                    onValueChange={handleSliderChange}
                    onMouseEnter={() => setShowTooltip(true)}
                    onMouseLeave={() => setShowTooltip(false)}
                    mt={2}
                  >
                    <Slider.Track>
                      <Slider.FilledTrack />
                    </Slider.Track>
                    <Tooltip.Root open={showTooltip}>
                      <Tooltip.Trigger asChild>
                        <Slider.Thumb index={0} />
                      </Tooltip.Trigger>
                      <Tooltip.Content
                        hasArrow
                        bg="blue.500"
                        color="white"
                        placement="top"
                      >
                        {`${sliderValue}%`}
                      </Tooltip.Content>
                    </Tooltip.Root>
                  </Slider.Root>
                </Field.Root>
              </VStack>
            </Box>
          </Dialog.Body>

          <Dialog.Footer>
            <Button variant="ghost" mr={3} onClick={handleClose}>
              Cancel
            </Button>
            <Button
              type="submit"
              form="resource-form"
              colorScheme="blue"
              loading={isSubmitting}
              loadingText="Saving"
            >
              Save Resource
            </Button>
          </Dialog.Footer>
        </Dialog.Content>
      </Dialog.Positioner>
    </Dialog.Root>
  )
}
