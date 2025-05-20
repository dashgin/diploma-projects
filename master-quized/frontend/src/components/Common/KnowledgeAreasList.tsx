import {
  Box,
  Card,
  CardBody,
  Container,
  Grid,
  Heading,
  Spinner,
  Text,
} from "@chakra-ui/react"
import { KnowledgeAreaRead } from "../../client"
import { useKnowledgeAreas } from "../../hooks/useKnowledgeAreas"

interface KnowledgeAreasListProps {
  areas?: KnowledgeAreaRead[]
}

export function KnowledgeAreasList({ areas: filteredAreas }: KnowledgeAreasListProps) {
  const { data: areas, isLoading, error } = useKnowledgeAreas()
  
  // Use filtered areas if provided, otherwise use all areas
  const displayAreas = filteredAreas || areas || []

  if (isLoading && !filteredAreas) {
    return (
      <Box textAlign="center" py={10}>
        <Spinner size="xl" />
      </Box>
    )
  }

  if (error && !filteredAreas) {
    return (
      <Box textAlign="center" py={10}>
        <Text color="red.500">Error loading knowledge areas</Text>
      </Box>
    )
  }

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
        {displayAreas.map((area) => (
          <Card
            key={area.id}
            bg="bg.surface"
            _hover={{ bg: "bg.muted" }}
            transition="all 0.2s"
            shadow="md"
            borderRadius="lg"
          >
            <CardBody>
              <Heading size="md" mb={2}>
                {area.name}
              </Heading>
              <Text>{area.description}</Text>
            </CardBody>
          </Card>
        ))}
        {displayAreas.length === 0 && (
          <Text>No knowledge areas found. Please add some.</Text>
        )}
      </Grid>
    </Container>
  )
} 