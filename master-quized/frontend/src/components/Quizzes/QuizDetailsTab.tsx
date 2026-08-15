import type { QuizRead } from "@/client"
import { Box, Heading, Stack, Text } from "@chakra-ui/react"

interface QuizDetailsTabProps {
  quiz: QuizRead
}

const QuizDetailsTab = ({ quiz }: QuizDetailsTabProps) => {
  return (
    <Box>
      <Stack gap={4}>
        <Box>
          <Heading size="xs" textTransform="uppercase">
            Instructions
          </Heading>
          <Text pt={2}>{quiz.instructions || "No instructions provided"}</Text>
        </Box>
        <Box h="1px" bg="gray.200" />
        <Box>
          <Heading size="xs" textTransform="uppercase">
            Status
          </Heading>
          <Text pt={2}>{quiz.is_active ? "Active" : "Inactive"}</Text>
        </Box>
        <Box h="1px" bg="gray.200" />
        <Box>
          <Heading size="xs" textTransform="uppercase">
            Quiz ID
          </Heading>
          <Text pt={2}>{quiz.id}</Text>
        </Box>
        {quiz.created_at && (
          <>
            <Box h="1px" bg="gray.200" />
            <Box>
              <Heading size="xs" textTransform="uppercase">
                Created At
              </Heading>
              <Text pt={2}>{new Date(quiz.created_at).toLocaleString()}</Text>
            </Box>
          </>
        )}
        {quiz.updated_at && (
          <>
            <Box h="1px" bg="gray.200" />
            <Box>
              <Heading size="xs" textTransform="uppercase">
                Last Updated
              </Heading>
              <Text pt={2}>{new Date(quiz.updated_at).toLocaleString()}</Text>
            </Box>
          </>
        )}
      </Stack>
    </Box>
  )
}

export default QuizDetailsTab
