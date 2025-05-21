import { Box, Container, Flex, Heading } from "@chakra-ui/react"
import { Spinner } from "@chakra-ui/react"
import {
  Link,
  MatchRoute,
  createFileRoute,
  useNavigate,
} from "@tanstack/react-router"
import { FiArrowLeft } from "react-icons/fi"

import { AttemptDetails } from "@/components/Items"
import { Button } from "@/components/ui/button"

interface AttemptDetailLoaderData {
  attemptId: number
}

export const Route = createFileRoute("/_layout/attempts/$attemptId")({
  component: AttemptDetailPage,
})

function AttemptDetailPage() {
  const { attemptId } = Route.useParams()
  const navigate = useNavigate()

  return (
    <Container maxW="full">
      <Flex align="center" pt={8} pb={4}>
        <Link to="/attempts" preload="intent" className="mr-4">
          <Button variant="ghost">
            <FiArrowLeft />
            Back
            <MatchRoute to="/attempts" pending>
              {(isPending) => isPending && <Spinner size="sm" ml={2} />}
            </MatchRoute>
          </Button>
        </Link>

        <Heading size="lg">Attempt Details</Heading>
      </Flex>

      <AttemptDetails attemptId={Number.parseInt(attemptId)} />
    </Container>
  )
}
