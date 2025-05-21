import { Container, Flex, Heading, Tabs } from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { z } from "zod"

import { type AssignmentRead, AssignmentsService } from "@/client"
import { AssignmentsList } from "@/components/Assignments"
import PendingAssignments from "@/components/Pending/PendingAssignments"
import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination.tsx"

const assignmentsSearchSchema = z.object({
  page: z.number().catch(1),
})

const PER_PAGE = 10

function getAssignmentsQueryOptions({
  page,
  userAssignments,
}: { page: number; userAssignments: boolean }) {
  return {
    queryFn: () =>
      userAssignments
        ? AssignmentsService.readUserAssignments({
            skip: (page - 1) * PER_PAGE,
            limit: PER_PAGE,
          })
        : AssignmentsService.readAssignments({
            skip: (page - 1) * PER_PAGE,
            limit: PER_PAGE,
          }),
    queryKey: ["assignments", { page, userAssignments }],
  }
}

export const Route = createFileRoute("/_layout/assignments")({
  component: Assignments,
  validateSearch: (search) => assignmentsSearchSchema.parse(search),
})

function AssignmentsTable({
  userAssignments = false,
}: { userAssignments?: boolean }) {
  const navigate = useNavigate({ from: Route.fullPath })
  const { page } = Route.useSearch()

  const { data, isLoading, isPlaceholderData } = useQuery({
    ...getAssignmentsQueryOptions({ page, userAssignments }),
    placeholderData: (prevData) => prevData,
  })

  const setPage = (page: number) =>
    navigate({
      search: (prev: { [key: string]: string }) => ({ ...prev, page }),
    })

  // Handle the new pagination format with data and count fields
  const assignments = data?.data || []
  const count = data?.count || 0

  if (isLoading) {
    return <PendingAssignments />
  }

  return (
    <>
      <AssignmentsList
        assignments={assignments}
        userAssignments={userAssignments}
      />

      {count > PER_PAGE && (
        <Flex justifyContent="flex-end" mt={4}>
          <PaginationRoot
            count={count}
            pageSize={PER_PAGE}
            onPageChange={({ page }) => setPage(page)}
            page={page}
          >
            <Flex>
              <PaginationPrevTrigger />
              <PaginationItems />
              <PaginationNextTrigger />
            </Flex>
          </PaginationRoot>
        </Flex>
      )}
    </>
  )
}

function Assignments() {
  return (
    <Container maxW="full">
      <Heading size="lg" pt={12}>
        Assignments
      </Heading>
      <Flex flexDirection="column" gap={6} mt={6}>
        <Tabs.Root defaultValue="my">
          <Tabs.List>
            <Tabs.Trigger value="my">My Assignments</Tabs.Trigger>
            <Tabs.Trigger value="all">All Assignments</Tabs.Trigger>
          </Tabs.List>
          <Tabs.Content value="my" pt={4}>
            <AssignmentsTable userAssignments={true} />
          </Tabs.Content>
          <Tabs.Content value="all" pt={4}>
            <AssignmentsTable userAssignments={false} />
          </Tabs.Content>
        </Tabs.Root>
      </Flex>
    </Container>
  )
}
