import { Box, Container } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { useEffect, useState } from "react"
import { QuizList } from "../../components/Common/QuizList"
import { QuizSearch } from "../../components/Common/QuizSearch"
import { useQuizzes } from "../../hooks/useQuizzes"

export const Route = createFileRoute("/_layout/quizzes")({
  component: QuizzesPage,
})

function QuizzesPage() {
  const { data: quizzes } = useQuizzes()
  const [filteredQuizzes, setFilteredQuizzes] = useState<typeof quizzes>([])

  // Update filtered quizzes when data loads
  useEffect(() => {
    if (quizzes) {
      setFilteredQuizzes(quizzes)
    }
  }, [quizzes])

  const handleSearch = (searchTerm: string) => {
    if (!quizzes) return

    if (!searchTerm.trim()) {
      setFilteredQuizzes(quizzes)
      return
    }

    const filtered = quizzes.filter(
      (quiz) =>
        quiz.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (quiz.description &&
          quiz.description.toLowerCase().includes(searchTerm.toLowerCase())),
    )
    setFilteredQuizzes(filtered)
  }

  return (
    <Container maxW="container.xl" py={8}>
      <QuizSearch onSearch={handleSearch} />
      <QuizList quizzes={filteredQuizzes} />
    </Container>
  )
} 