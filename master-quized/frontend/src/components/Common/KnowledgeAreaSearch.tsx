import {
  Box,
  Flex,
  Input,
} from "@chakra-ui/react"
import { useState } from "react"

interface KnowledgeAreaSearchProps {
  onSearch: (searchTerm: string) => void
}

export function KnowledgeAreaSearch({ onSearch }: KnowledgeAreaSearchProps) {
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
          placeholder="Search knowledge areas..."
          value={searchTerm}
          onChange={handleSearchChange}
          borderRadius="md"
        />
      </Flex>
    </Box>
  )
} 