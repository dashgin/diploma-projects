"""
Recommendation engine module for suggesting learning resources based on skill gaps.
"""

import logging

from app.schemas import RecommendedResource

logger = logging.getLogger(__name__)

# Mock resource database - in a real system, this would be a database query
# Organized by topic and skill gap
RECOMMENDATION_DB = {
    "default": {
        "factual_knowledge": [
            RecommendedResource(
                title="Understanding Key Facts",
                url="https://example.com/resources/key-facts",
                type="article",
            ),
            RecommendedResource(
                title="Fact Mastery",
                url="https://example.com/courses/fact-mastery",
                type="course",
            ),
        ],
        "conceptual_understanding": [
            RecommendedResource(
                title="Core Concepts Explained",
                url="https://example.com/resources/core-concepts",
                type="video",
            ),
            RecommendedResource(
                title="Concept Mapping Exercise",
                url="https://example.com/exercises/concept-mapping",
                type="practice_set",
            ),
        ],
        "comprehensive_explanation": [
            RecommendedResource(
                title="How to Write Comprehensive Explanations",
                url="https://example.com/resources/comprehensive-writing",
                type="article",
            ),
            RecommendedResource(
                title="Explanation Building Workshop",
                url="https://example.com/workshops/explanation-building",
                type="workshop",
            ),
        ],
        "logical_reasoning": [
            RecommendedResource(
                title="Critical Thinking and Logic",
                url="https://example.com/resources/critical-thinking",
                type="course",
            ),
            RecommendedResource(
                title="Logical Fallacies Guide",
                url="https://example.com/guides/logical-fallacies",
                type="reference",
            ),
        ],
        "topic_relevance": [
            RecommendedResource(
                title="Staying On Topic: A Guide",
                url="https://example.com/resources/staying-on-topic",
                type="article",
            ),
            RecommendedResource(
                title="Relevance Assessment Practice",
                url="https://example.com/practice/relevance-assessment",
                type="practice_set",
            ),
        ],
        "general_understanding": [
            RecommendedResource(
                title="Study Skills Master Class",
                url="https://example.com/courses/study-skills",
                type="course",
            ),
            RecommendedResource(
                title="Learning Strategies for Success",
                url="https://example.com/resources/learning-strategies",
                type="video",
            ),
        ],
    },
    "Environmental Science": {
        "factual_knowledge": [
            RecommendedResource(
                title="Environmental Science Facts Database",
                url="https://example.com/env-science/facts",
                type="reference",
            ),
            RecommendedResource(
                title="Environmental Processes and Systems",
                url="https://example.com/env-science/processes",
                type="course",
            ),
        ],
        "knowledge_of_biogeochemical_cycle": [
            RecommendedResource(
                title="Biogeochemical Cycles Explained",
                url="https://example.com/env-science/biogeochemical-cycles",
                type="video",
            ),
            RecommendedResource(
                title="Interactive Biogeochemical Cycle Simulator",
                url="https://example.com/env-science/cycle-simulator",
                type="interactive",
            ),
        ],
        "knowledge_of_carbon_exchange": [
            RecommendedResource(
                title="Carbon Cycle Deep Dive",
                url="https://example.com/env-science/carbon-cycle",
                type="article",
            ),
            RecommendedResource(
                title="Carbon Exchange in Ecosystems",
                url="https://example.com/env-science/carbon-exchange",
                type="video",
            ),
        ],
    },
    # Add more topics as needed
}


def get_recommendations(
    skill_gaps: list[str], topic: str | None = None
) -> list[RecommendedResource]:
    """
    Get recommended learning resources based on identified skill gaps.

    Args:
        skill_gaps (List[str]): List of identified skill gaps
        topic (Optional[str]): Topic context, if available

    Returns:
        List[RecommendedResource]: List of recommended resources
    """
    try:
        recommendations = []

        if not skill_gaps:
            return recommendations

        # Use topic-specific resources if available, otherwise use default
        topic_resources = (
            RECOMMENDATION_DB.get(topic, RECOMMENDATION_DB["default"])
            if topic
            else RECOMMENDATION_DB["default"]
        )

        for gap in skill_gaps:
            # Look for resources specifically for this gap
            if gap in topic_resources:
                recommendations.extend(topic_resources[gap])
            # Fall back to default resources if topic-specific not available
            elif gap in RECOMMENDATION_DB["default"]:
                recommendations.extend(RECOMMENDATION_DB["default"][gap])

        # Deduplicate resources (in case multiple skill gaps lead to the same resource)
        unique_resources = {}
        for resource in recommendations:
            if resource.url not in unique_resources:
                unique_resources[resource.url] = resource

        # Limit to top 3 most relevant recommendations
        result = list(unique_resources.values())[:3]

        logger.debug(
            f"Generated {len(result)} recommendations for skill gaps: {skill_gaps}"
        )
        return result

    except Exception as e:
        logger.error(f"Error generating recommendations: {e}", exc_info=True)
        # Return fallback recommendation in case of error
        return [
            RecommendedResource(
                title="General Learning Resources",
                url="https://example.com/resources/general",
                type="reference",
            )
        ]
