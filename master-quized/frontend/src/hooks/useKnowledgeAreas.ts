import { useQuery } from "@tanstack/react-query"
import { AreasService } from "../client"

export function useKnowledgeAreas() {
  return useQuery({
    queryKey: ["knowledgeAreas"],
    queryFn: () => AreasService.readAreas(),
  })
} 