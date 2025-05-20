import { Box } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { KnowledgeAreaSearch } from "../../components/Common/KnowledgeAreaSearch"
import { KnowledgeAreasList } from "../../components/Common/KnowledgeAreasList"
import { useKnowledgeAreas } from "../../hooks/useKnowledgeAreas"

export const Route = createFileRoute("/_layout/knowledge-areas")({
  component: KnowledgeAreasPage,
})

function KnowledgeAreasPage() {
  const { data: areas } = useKnowledgeAreas()
  const [filteredAreas, setFilteredAreas] = useState(areas || [])

  const handleSearch = (searchTerm: string) => {
    if (!areas) return

    if (!searchTerm.trim()) {
      setFilteredAreas(areas)
      return
    }

    const filtered = areas.filter(
      (area) =>
        area.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (area.description &&
          area.description.toLowerCase().includes(searchTerm.toLowerCase())),
    )
    setFilteredAreas(filtered)
  }

  return (
    <Box p={4}>
      <KnowledgeAreaSearch onSearch={handleSearch} />
      <KnowledgeAreasList areas={filteredAreas} />
    </Box>
  )
} 