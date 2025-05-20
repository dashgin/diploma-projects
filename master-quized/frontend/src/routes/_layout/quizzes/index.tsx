import {
  Container,
  EmptyState,
  Flex,
  Heading,
  Table,
  VStack,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { Link, createFileRoute, useNavigate } from "@tanstack/react-router"
import { FiSearch } from "react-icons/fi"
import { z } from "zod"

import { QuizzesService } from "@/client"
import PendingQuizzes from "@/components/Pending/PendingQuizzes"
import AddQuiz from "@/components/Quizzes/AddQuiz"
import { QuizActionsMenu } from "@/components/Quizzes/QuizActionsMenu"
import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination.tsx"

const quizzesSearchSchema = z.object({
  page: z.number().catch(1),
})

const PER_PAGE = 5

function getQuizzesQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      QuizzesService.readQuizzes({
        skip: (page - 1) * PER_PAGE,
        limit: PER_PAGE,
      }),
    queryKey: ["quizzes", { page }],
  }
}

export const Route = createFileRoute("/_layout/quizzes/")({
  component: Quizzes,
  validateSearch: (search) => quizzesSearchSchema.parse(search),
})

function QuizzesTable() {
  const navigate = useNavigate({ from: Route.fullPath })
  const { page } = Route.useSearch()

  const { data, isLoading, isPlaceholderData } = useQuery({
    ...getQuizzesQueryOptions({ page }),
    placeholderData: (prevData) => prevData,
  })

  const setPage = (page: number) =>
    navigate({
      search: (prev: { [key: string]: string }) => ({ ...prev, page }),
    })

  const quizzes = data ?? []
  const count = data?.length ?? 0

  if (isLoading) {
    return <PendingQuizzes />
  }

  if (quizzes.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>You don't have any quizzes yet</EmptyState.Title>
            <EmptyState.Description>
              Add a new quiz to get started
            </EmptyState.Description>
          </VStack>
        </EmptyState.Content>
      </EmptyState.Root>
    )
  }

  return (
    <>
      <Table.Root size={{ base: "sm", md: "md" }}>
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader w="sm">ID</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Title</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Instructions</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Status</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {quizzes?.map((quiz) => (
            <Table.Row key={quiz.id} opacity={isPlaceholderData ? 0.5 : 1}>
              <Table.Cell truncate maxW="sm">
                {quiz.id}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                <Link
                  to="/quizzes/$quizId"
                  params={{ quizId: quiz.id }}
                  className="text-blue-600 hover:underline"
                  preload="intent"
                >
                  {quiz.title}
                </Link>
              </Table.Cell>
              <Table.Cell
                color={!quiz.instructions ? "gray" : "inherit"}
                truncate
                maxW="30%"
              >
                {quiz.instructions || "N/A"}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {quiz.is_active ? "Active" : "Inactive"}
              </Table.Cell>
              <Table.Cell>
                <QuizActionsMenu quiz={quiz} />
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
      <Flex justifyContent="flex-end" mt={4}>
        <PaginationRoot
          count={count}
          pageSize={PER_PAGE}
          onPageChange={({ page }) => setPage(page)}
        >
          <Flex>
            <PaginationPrevTrigger />
            <PaginationItems />
            <PaginationNextTrigger />
          </Flex>
        </PaginationRoot>
      </Flex>
    </>
  )
}

function Quizzes() {
  return (
    <Container maxW="full">
      <Heading size="lg" pt={12}>
        Quizzes Management
      </Heading>
      <AddQuiz />
      <QuizzesTable />
    </Container>
  )
}
