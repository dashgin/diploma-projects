import { Box, Container, Grid, Heading, Text } from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { AreasService, type KnowledgeAreaRead } from "../../client"

interface KnowledgeAreasListProps {
  areas?: KnowledgeAreaRead[] | null
}

export function KnowledgeAreasList({
  areas: filteredAreas,
}: KnowledgeAreasListProps) {
  const { data: areasResponse } = useQuery({
    queryKey: ["knowledgeAreas"],
    queryFn: () => AreasService.readAreas(),
  })

  // Handle the new pagination format with data and count fields
  const areasData = areasResponse?.data || []

  // Use filtered areas if provided, otherwise use all areas
  const displayAreas = filteredAreas || areasData

  // Ensure displayAreas is always an array
  const areasList = Array.isArray(displayAreas) ? displayAreas : []

  return (
    <Container maxW="container.xl" py={8}>
      <Heading mb={6} size="lg">
        Knowledge Areas
      </Heading>
      <Grid
        templateColumns={{
          base: "1fr",
          md: "repeat(2, 1fr)",
          lg: "repeat(3, 1fr)",
        }}
        gap={6}
      >
        {areasList.length === 0 ? (
          <Text>No knowledge areas found. Please add some.</Text>
        ) : (
          areasList.map((area) => (
            <Box
              key={area.id}
              p={4}
              bg="bg.surface"
              borderWidth="1px"
              borderRadius="lg"
              _hover={{ bg: "bg.muted" }}
              transition="all 0.2s"
              shadow="md"
            >
              <Heading size="md" mb={2}>
                {area.name}
              </Heading>
              <Text>{area.description}</Text>
            </Box>
          ))
        )}
      </Grid>
    </Container>
  )
}
