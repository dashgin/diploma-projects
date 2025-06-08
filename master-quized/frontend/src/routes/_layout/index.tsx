import {
  Badge,
  Box,
  Button,
  Card,
  Link as ChakraLink,
  Container,
  Flex,
  Grid,
  GridItem,
  HStack,
  Heading,
  Icon,
  List,
  Separator,
  Stack,
  Stat,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { Link, createFileRoute } from "@tanstack/react-router"
import {
  FiActivity,
  FiAward,
  FiBook,
  FiBookOpen,
  FiClock,
  FiEye,
  FiPlus,
  FiTarget,
  FiTrendingUp,
  FiUsers,
  FiZap,
} from "react-icons/fi"

import useAuth from "@/hooks/useAuth"
import {
  AttemptsService,
  QuizzesService,
  UsersService,
} from "../../client/sdk.gen"
import { AIFeedbackDisplay } from "../../components/Feedback/AIFeedbackDisplay"
import { formatDate } from "../../utils/formatters"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const { user: currentUser } = useAuth()

  // Fetch dashboard data
  const { data: quizzes } = useQuery({
    queryKey: ["quizzes", { limit: 10 }],
    queryFn: () => QuizzesService.readQuizzes({ limit: 10 }),
  })

  const { data: userQuizzes } = useQuery({
    queryKey: ["user-quizzes", { limit: 5 }],
    queryFn: () => QuizzesService.readUserQuizzes({ limit: 5 }),
  })

  const { data: recentAttempts } = useQuery({
    queryKey: ["recent-attempts", { limit: 5 }],
    queryFn: () => AttemptsService.readUserAttempts({ limit: 5 }),
  })

  const { data: allUsers } = useQuery({
    queryKey: ["users-count"],
    queryFn: () => UsersService.readUsers({ limit: 1 }),
    enabled: currentUser?.is_superuser,
  })

  const isAdmin = currentUser?.is_superuser
  const isInstructor = currentUser?.is_staff || isAdmin

  // Calculate stats
  const totalQuizzes = quizzes?.count || 0
  const myQuizzes = userQuizzes?.count || 0
  const totalAttempts = recentAttempts?.count || 0
  const totalUsers = allUsers?.count || 0

  // Calculate completion rate from recent attempts
  const completedAttempts =
    recentAttempts?.data?.filter((attempt) => attempt.is_completed).length || 0
  const completionRate =
    totalAttempts > 0 ? (completedAttempts / totalAttempts) * 100 : 0

  return (
    <Container maxW="full" py={6}>
      {/* Header Section */}
      <Box mb={8}>
        <VStack align="start" gap={2}>
          <Heading size="xl" color="blue.600">
            Welcome back,{" "}
            {currentUser?.full_name || currentUser?.email?.split("@")[0]}! 👋
          </Heading>
          <Text fontSize="lg" color="gray.600">
            {isAdmin
              ? "System Administrator"
              : isInstructor
                ? "Instructor Dashboard"
                : "Student Dashboard"}
          </Text>
        </VStack>
      </Box>

      {/* Quick Stats Grid */}
      <Grid
        templateColumns={{
          base: "1fr",
          md: "repeat(2, 1fr)",
          lg: "repeat(4, 1fr)",
        }}
        gap={6}
        mb={8}
      >
        <Card.Root>
          <Card.Body>
            <Stat.Root>
              <HStack justify="space-between">
                <VStack align="start" gap={1}>
                  <Stat.Label>Total Quizzes</Stat.Label>
                  <Stat.ValueText
                    fontSize="3xl"
                    fontWeight="bold"
                    color="blue.500"
                  >
                    {totalQuizzes}
                  </Stat.ValueText>
                </VStack>
                <Icon size="2xl" color="blue.400">
                  <FiBook />
                </Icon>
              </HStack>
            </Stat.Root>
          </Card.Body>
        </Card.Root>

        {isInstructor && (
          <Card.Root>
            <Card.Body>
              <Stat.Root>
                <HStack justify="space-between">
                  <VStack align="start" gap={1}>
                    <Stat.Label>My Quizzes</Stat.Label>
                    <Stat.ValueText
                      fontSize="3xl"
                      fontWeight="bold"
                      color="green.500"
                    >
                      {myQuizzes}
                    </Stat.ValueText>
                  </VStack>
                  <Icon size="2xl" color="green.400">
                    <FiBookOpen />
                  </Icon>
                </HStack>
              </Stat.Root>
            </Card.Body>
          </Card.Root>
        )}

        <Card.Root>
          <Card.Body>
            <Stat.Root>
              <HStack justify="space-between">
                <VStack align="start" gap={1}>
                  <Stat.Label>Quiz Attempts</Stat.Label>
                  <Stat.ValueText
                    fontSize="3xl"
                    fontWeight="bold"
                    color="purple.500"
                  >
                    {totalAttempts}
                  </Stat.ValueText>
                </VStack>
                <Icon size="2xl" color="purple.400">
                  <FiTarget />
                </Icon>
              </HStack>
            </Stat.Root>
          </Card.Body>
        </Card.Root>
        {isAdmin && (
          <Card.Root>
            <Card.Body>
              <Stat.Root>
                <HStack justify="space-between">
                  <VStack align="start" gap={1}>
                    <Stat.Label>Total Users</Stat.Label>
                    <Stat.ValueText
                      fontSize="3xl"
                      fontWeight="bold"
                      color="teal.500"
                    >
                      {totalUsers}
                    </Stat.ValueText>
                  </VStack>
                  <Icon size="2xl" color="teal.400">
                    <FiUsers />
                  </Icon>
                </HStack>
              </Stat.Root>
            </Card.Body>
          </Card.Root>
        )}
      </Grid>

      {/* Featured Systems - Top Section */}
      <Grid templateColumns={{ base: "1fr", lg: "2fr 1fr" }} gap={8} mb={8}>
        {/* AI Feedback Demo */}
        <Card.Root
          bg="gradient-to-r"
          bgGradient="linear(to-r, blue.50, purple.50)"
        >
          <Card.Header>
            <Flex justify="space-between" align="center">
              <HStack>
                <Icon color="blue.500">
                  <FiZap />
                </Icon>
                <Heading size="md" color="blue.700">
                  AI Feedback System
                </Heading>
                <Badge colorScheme="blue" variant="outline">
                  DEMO
                </Badge>
              </HStack>
              <Button as={Link} to="/assignments" size="sm" colorScheme="blue">
                Try It Yourself
              </Button>
            </Flex>
          </Card.Header>
          <Card.Body>
            <VStack align="stretch" gap={4}>
              <Text color="blue.700" fontSize="sm">
                See our AI feedback system in action with a demo student
                response:
              </Text>

              <Box p={4} bg="white" borderRadius="md" borderWidth="1px">
                <VStack align="stretch" gap={3}>
                  <Box>
                    <Text
                      fontWeight="bold"
                      fontSize="sm"
                      color="gray.600"
                      mb={1}
                    >
                      Question: Programming Languages
                    </Text>
                    <Text fontSize="sm" mb={2}>
                      "Explain what a programming language is and give three
                      examples."
                    </Text>
                  </Box>

                  <Box
                    p={3}
                    bg="red.50"
                    borderRadius="md"
                    borderLeft="4px solid"
                    borderColor="red.400"
                  >
                    <Text
                      fontWeight="bold"
                      mb={1}
                      fontSize="sm"
                      color="red.700"
                    >
                      Student Answer (Incorrect):
                    </Text>
                    <Text fontSize="sm" fontStyle="italic" color="red.600">
                      "Python is not a programming language, it is a snake.
                      Programming languages are tools for making websites."
                    </Text>
                  </Box>

                  {/* Demo AI Feedback */}
                  <AIFeedbackDisplay responseId={28} demo="fail" />
                </VStack>
              </Box>

              <Text fontSize="xs" color="blue.600" fontStyle="italic">
                💡 This is a demo of AI feedback that would be automatically generated by analyzing the
                student's response against the model answer and key concepts.
              </Text>
            </VStack>
          </Card.Body>
        </Card.Root>

        {/* Right Column - System Status & Functionalities */}
        <VStack gap={6} align="stretch">
          {/* System Functionalities */}
          <Card.Root>
            <Card.Header>
              <Heading size="md">System Functionalities</Heading>
            </Card.Header>
            <Card.Body>
              <VStack gap={3} align="stretch">
                <Box p={3} borderRadius="md" bg="blue.50">
                  <Flex gap={2}>
                    <Icon color="blue.500" mt={0.5}>
                      <FiZap />
                    </Icon>
                    <VStack align="start" gap={1}>
                      <Text fontSize="sm" fontWeight="medium">
                        AI-Powered Feedback
                      </Text>
                      <Text fontSize="xs" color="gray.600">
                        Automated analysis and personalized feedback for text
                        responses
                      </Text>
                    </VStack>
                  </Flex>
                </Box>

                <Box p={3} borderRadius="md" bg="green.50">
                  <Flex gap={2}>
                    <Icon color="green.500" mt={0.5}>
                      <FiTarget />
                    </Icon>
                    <VStack align="start" gap={1}>
                      <Text fontSize="sm" fontWeight="medium">
                        Adaptive Learning
                      </Text>
                      <Text fontSize="xs" color="gray.600">
                        Dynamic question difficulty based on performance
                      </Text>
                    </VStack>
                  </Flex>
                </Box>

                <Box p={3} borderRadius="md" bg="purple.50">
                  <Flex gap={2}>
                    <Icon color="purple.500" mt={0.5}>
                      <FiTrendingUp />
                    </Icon>
                    <VStack align="start" gap={1}>
                      <Text fontSize="sm" fontWeight="medium">
                        Real-time Analytics
                      </Text>
                      <Text fontSize="xs" color="gray.600">
                        Live progress tracking and performance insights
                      </Text>
                    </VStack>
                  </Flex>
                </Box>

                <Box p={3} borderRadius="md" bg="orange.50">
                  <Flex gap={2}>
                    <Icon color="orange.500" mt={0.5}>
                      <FiClock />
                    </Icon>
                    <VStack align="start" gap={1}>
                      <Text fontSize="sm" fontWeight="medium">
                        Smart Scheduling
                      </Text>
                      <Text fontSize="xs" color="gray.600">
                        Automated quiz scheduling and deadline management
                      </Text>
                    </VStack>
                  </Flex>
                </Box>
              </VStack>
            </Card.Body>
          </Card.Root>
          {/* System Status */}
          <Card.Root>
            <Card.Header>
              <Heading size="md">System Status</Heading>
            </Card.Header>
            <Card.Body>
              <VStack gap={3}>
                <Flex justify="space-between" align="center" w="full">
                  <Text fontSize="sm">Quiz System</Text>
                  <Badge colorScheme="green">Online</Badge>
                </Flex>
                <Flex justify="space-between" align="center" w="full">
                  <Text fontSize="sm">AI Feedback</Text>
                  <Badge colorScheme="green">Active</Badge>
                </Flex>
                <Flex justify="space-between" align="center" w="full">
                  <Text fontSize="sm">Database</Text>
                  <Badge colorScheme="green">Connected</Badge>
                </Flex>
              </VStack>
            </Card.Body>
          </Card.Root>
        </VStack>
      </Grid>

      {/* Quick Actions */}
      <Card.Root mb={8}>
        <Card.Header>
          <Heading size="md">Quick Actions</Heading>
        </Card.Header>
        <Card.Body>
          <Grid
            templateColumns={{
              base: "1fr",
              md: "repeat(2, 1fr)",
              lg: "repeat(3, 1fr)",
            }}
            gap={4}
          >
            <Button
              as={Link}
              to="/quizzes"
              colorScheme="blue"
              variant="outline"
            >
              <FiEye />
              Browse Quizzes
            </Button>
            {isInstructor && (
              <Button
                as={Link}
                to="/quizzes"
                colorScheme="green"
                variant="outline"
              >
                <FiPlus />
                Create Quiz
              </Button>
            )}
            {isAdmin && (
              <Button
                as={Link}
                to="/admin"
                colorScheme="teal"
                variant="outline"
              >
                <FiUsers />
                User Management
              </Button>
            )}
          </Grid>
        </Card.Body>
      </Card.Root>

      {/* Main Content Grid */}
      <Grid templateColumns={{ base: "1fr", lg: "2fr 1fr" }} gap={8}>
        {/* Left Column - Recent Activity & AI Demo */}
        <VStack gap={6} align="stretch">
          {/* Recent Quiz Attempts */}
          <Card.Root>
            <Card.Header>
              <Flex justify="space-between" align="center">
                <Heading size="md">Recent Quiz Attempts</Heading>
                <Button as={Link} to="/attempts" size="sm" variant="outline">
                  View All
                </Button>
              </Flex>
            </Card.Header>
            <Card.Body>
              {recentAttempts?.data && recentAttempts.data.length > 0 ? (
                <List.Root gap={3}>
                  {recentAttempts.data.slice(0, 5).map((attempt) => (
                    <List.Item key={attempt.id}>
                      <Flex
                        justify="space-between"
                        align="center"
                        p={3}
                        borderRadius="md"
                        bg="gray.50"
                      >
                        <VStack align="start" gap={1}>
                          <Text fontWeight="medium">
                            Quiz #{attempt.quiz_id}
                          </Text>
                          <Text fontSize="sm" color="gray.600">
                            {attempt.completed_at
                              ? formatDate(attempt.completed_at)
                              : "In Progress"}
                          </Text>
                        </VStack>
                        <HStack>
                          {attempt.is_completed && (
                            <Badge
                              colorScheme={
                                attempt.score && attempt.score >= 70
                                  ? "green"
                                  : "red"
                              }
                            >
                              {attempt.score
                                ? `${Math.round(attempt.score)}%`
                                : "Not Scored"}
                            </Badge>
                          )}
                          {!attempt.is_completed && (
                            <Badge colorScheme="blue">In Progress</Badge>
                          )}
                          <Button
                            as={Link}
                            to={`/attempts/${attempt.id}`}
                            size="sm"
                            variant="outline"
                          >
                            View
                          </Button>
                        </HStack>
                      </Flex>
                    </List.Item>
                  ))}
                </List.Root>
              ) : (
                <Text color="gray.500" textAlign="center" py={6}>
                  No quiz attempts yet. Take your first quiz to get started!
                </Text>
              )}
            </Card.Body>
          </Card.Root>
        </VStack>

        {/* Right Column - Quick Info & Navigation */}
        <VStack gap={6} align="stretch">
          {/* My Quizzes (for instructors) */}
          {isInstructor && (
            <Card.Root>
              <Card.Header>
                <Flex justify="space-between" align="center">
                  <Heading size="md">My Quizzes</Heading>
                  <Button as={Link} to="/quizzes" size="sm" variant="outline">
                    Manage
                  </Button>
                </Flex>
              </Card.Header>
              <Card.Body>
                {userQuizzes?.data && userQuizzes.data.length > 0 ? (
                  <List.Root gap={2}>
                    {userQuizzes.data.slice(0, 3).map((quiz) => (
                      <List.Item key={quiz.id}>
                        <Flex
                          justify="space-between"
                          align="center"
                          p={2}
                          borderRadius="md"
                          _hover={{ bg: "gray.50" }}
                        >
                          <VStack align="start" gap={0}>
                            <Text fontWeight="medium" fontSize="sm">
                              {quiz.title}
                            </Text>
                            <Badge
                              colorScheme={quiz.is_active ? "green" : "gray"}
                              size="sm"
                            >
                              {quiz.is_active ? "Active" : "Inactive"}
                            </Badge>
                          </VStack>
                          <Button
                            as={Link}
                            to={`/quizzes/${quiz.id}`}
                            size="xs"
                            variant="outline"
                          >
                            Edit
                          </Button>
                        </Flex>
                      </List.Item>
                    ))}
                  </List.Root>
                ) : (
                  <Text
                    color="gray.500"
                    fontSize="sm"
                    textAlign="center"
                    py={4}
                  >
                    Create your first quiz to get started!
                  </Text>
                )}
              </Card.Body>
            </Card.Root>
          )}
        </VStack>
      </Grid>
    </Container>
  )
}
