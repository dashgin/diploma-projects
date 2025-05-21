import { Box, Container, Spinner, Text } from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { AreasService } from "../../client"
import { KnowledgeAreaSearch } from "../../components/Common/KnowledgeAreaSearch"
import { KnowledgeAreasList } from "../../components/Common/KnowledgeAreasList"

export const Route = createFileRoute("/_layout/knowledge-areas")({
  component: KnowledgeAreasPage,
})

function KnowledgeAreasPage() {
  const {
    data: areasResponse,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["knowledgeAreas"],
    queryFn: () => AreasService.readAreas(),
  })
  const [searchTerm, setSearchTerm] = useState("")

  // Handle the new pagination format with data and count fields
  const areasData = areasResponse?.data || []

  // Ensure areas is always an array
  const areas = Array.isArray(areasData) ? areasData : []

  const handleSearch = (term: string) => {
    setSearchTerm(term)
  }

  const filteredAreas = !searchTerm.trim()
    ? areas
    : areas.filter(
        (area) =>
          area.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          area.description?.toLowerCase().includes(searchTerm.toLowerCase()),
      )

  if (isLoading) {
    return (
      <Box p={4}>
        <Box textAlign="center" py={10}>
          <Spinner size="xl" />
        </Box>
      </Box>
    )
  }

  if (error) {
    return (
      <Box p={4}>
        <Box textAlign="center" py={10}>
          <Text color="red.500">Error loading knowledge areas</Text>
        </Box>
      </Box>
    )
  }

  return (
    <Box p={4}>
      <KnowledgeAreaSearch onSearch={handleSearch} />
      <KnowledgeAreasList areas={filteredAreas} />
    </Box>
  )
}
