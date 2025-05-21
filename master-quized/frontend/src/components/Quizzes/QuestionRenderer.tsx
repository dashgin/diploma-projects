import { Box, Text, Input, Textarea, RadioGroup } from "@chakra-ui/react";

interface QuestionRendererProps {
  questionType?: string;
  questionId: number;
  options?: Array<{ id: number; text: string }>;
  value: string;
  onChange: (questionId: number, value: string) => void;
}

// Helper function to ensure value is always a string
const ensureString = (value: string | null | undefined): string => {
  return value || "";
};

export default function QuestionRenderer({
  questionType = "text",
  questionId,
  options = [],
  value,
  onChange,
}: QuestionRendererProps) {
  // Handle rendering based on question type
  switch (questionType) {
    case "multiple_choice":
      return (
        <RadioGroup.Root 
          defaultValue={ensureString(value)}
          onValueChange={(details) => {
            if (details && details.value) {
              onChange(questionId, details.value);
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
      );
    
    case "essay":
      return (
        <Box>
          <Text mb={2} fontWeight="medium">Your Answer:</Text>
          <Textarea
            value={value}
            onChange={(e) => onChange(questionId, e.target.value)}
            placeholder="Type your detailed answer here..."
            minHeight="200px"
          />
        </Box>
      );
    
    case "true_false":
      return (
        <RadioGroup.Root 
          defaultValue={ensureString(value)}
          onValueChange={(details) => {
            if (details && details.value) {
              onChange(questionId, details.value);
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
      );
    
    // Default to text input
    default:
      return (
        <Box>
          <Text mb={2} fontWeight="medium">Your Answer:</Text>
          <Input
            value={value}
            onChange={(e) => onChange(questionId, e.target.value)}
            placeholder="Type your answer here..."
          />
        </Box>
      );
  }
} 