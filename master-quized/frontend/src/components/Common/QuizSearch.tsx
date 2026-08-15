import { Box, Flex, Input } from "@chakra-ui/react"
import { useState } from "react"

interface QuizSearchProps {
  onSearch: (searchTerm: string) => void
}

export function QuizSearch({ onSearch }: QuizSearchProps) {
  const [searchTerm, setSearchTerm] = useState("")

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setSearchTerm(value)
    onSearch(value)
  }

  return (
    <Box mb={6}>
      <Flex>
        <Input
          placeholder="Search quizzes..."
          value={searchTerm}
          onChange={handleSearchChange}
          borderRadius="md"
        />
      </Flex>
    </Box>
  )
}
