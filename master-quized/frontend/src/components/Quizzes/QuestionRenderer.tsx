import { Box, Input, RadioGroup, Text, Textarea } from "@chakra-ui/react"

interface QuestionRendererProps {
  questionType?: string
  questionId: number
  options?: Array<{ id: number; text: string }>
  value: string
  onChange: (questionId: number, value: string) => void
}

// Helper function to ensure value is always a string
const ensureString = (value: string | null | undefined): string => {
  return value || ""
}

export default function QuestionRenderer({
  questionType = "text",
  questionId,
  options = [],
  value,
  onChange,
}: QuestionRendererProps) {
  console.log("QuestionRenderer props:", {
    questionType,
    questionId,
    options,
    value,
  })

  // Handle rendering based on question type
  switch (questionType) {
    case "multiple_choice": {
      // Set the value correctly for radio group - it might be a number string
      const radioValue = ensureString(value)
      console.log("Multiple choice value:", radioValue)
      console.log("Options count:", options.length)

      // If no options are available, show a fallback
      if (!options || options.length === 0) {
        return (
          <Box p={4} borderWidth="1px" borderRadius="md" bg="gray.50">
            <Text color="gray.500">No options available for this question</Text>
          </Box>
        )
      }

      return (
        <RadioGroup.Root
          defaultValue={radioValue}
          onValueChange={(details) => {
            if (details?.value) {
              console.log("Selected option:", details.value)
              onChange(questionId, details.value)
            }
          }}
        >
          <Box display="flex" flexDirection="column" gap={3}>
            {options.map((option) => (
              <RadioGroup.Item key={option.id} value={option.id.toString()}>
                <RadioGroup.ItemHiddenInput />
                <RadioGroup.ItemIndicator />
                <RadioGroup.ItemText>{option.text}</RadioGroup.ItemText>
              </RadioGroup.Item>
            ))}
          </Box>
        </RadioGroup.Root>
      )
    }

    case "essay":
      return (
        <Box>
          <Text mb={2} fontWeight="medium">
            Your Answer:
          </Text>
          <Textarea
            value={value}
            onChange={(e) => onChange(questionId, e.target.value)}
            placeholder="Type your detailed answer here..."
            minHeight="200px"
          />
        </Box>
      )

    case "true_false":
      return (
        <RadioGroup.Root
          defaultValue={ensureString(value)}
          onValueChange={(details) => {
            if (details?.value) {
              onChange(questionId, details.value)
            }
          }}
        >
          <Box display="flex" flexDirection="column" gap={3}>
            <RadioGroup.Item value="true">
              <RadioGroup.ItemHiddenInput />
              <RadioGroup.ItemIndicator />
              <RadioGroup.ItemText>True</RadioGroup.ItemText>
            </RadioGroup.Item>
            <RadioGroup.Item value="false">
              <RadioGroup.ItemHiddenInput />
              <RadioGroup.ItemIndicator />
              <RadioGroup.ItemText>False</RadioGroup.ItemText>
            </RadioGroup.Item>
          </Box>
        </RadioGroup.Root>
      )

    // Default to text input
    default:
      return (
        <Box>
          <Text mb={2} fontWeight="medium">
            Your Answer:
          </Text>
          <Input
            value={value}
            onChange={(e) => onChange(questionId, e.target.value)}
            placeholder="Type your answer here..."
          />
        </Box>
      )
  }
}
