import { Container, Flex, Heading, Stack } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"

import { AttemptsList } from "@/components/Items"

export const Route = createFileRoute("/_layout/attempts/")({
  component: AttemptsPage,
})

function AttemptsPage() {
  return (
    <Container maxW="full" py={8}>
      <Stack spacing={8}>
        <Flex justifyContent="space-between" alignItems="center">
          <Heading size="lg">Quiz Attempts</Heading>
        </Flex>

        {/* Show user's quiz attempts */}
        <AttemptsList userAttempts={true} />

        {/* Show all attempts (for teachers/admins) */}
        <AttemptsList />
      </Stack>
    </Container>
  )
}
