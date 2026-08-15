"""
Feedback generation module to synthesize analysis results into coherent, actionable feedback.
"""

import logging
from typing import Any

from app.schemas import FeedbackResponseData, RecommendedResource

logger = logging.getLogger(__name__)


def construct_feedback(
    rule_feedback_analysis: dict[str, Any],
    ml_analysis_results: dict[str, Any],
    skill_gaps: list[str],
    recommended_resources: list[RecommendedResource],
) -> FeedbackResponseData:
    """
    Construct a coherent feedback message from the analysis results.

    Args:
        rule_feedback_analysis (Dict[str, Any]): Results from the rule-based analysis
        ml_analysis_results (Dict[str, Any]): Results from the ML analysis
        skill_gaps (List[str]): Identified skill gaps
        recommended_resources (List[RecommendedResource]): Recommended resources

    Returns:
        FeedbackResponseData: The complete feedback data
    """
    try:
        # Start with the base feedback information
        # If rule-based feedback has an "immediate_feedback", we would have returned early
        # So here we're building feedback using both rule and ML analysis
        feedback_text = ""
        error_identified = False
        error_types = []
        confidence_score = ml_analysis_results.get("confidence_score", 0.0)
        concepts_covered = rule_feedback_analysis.get("concepts_covered", [])
        concepts_missed = rule_feedback_analysis.get("concepts_missed", [])

        # Get semantic similarity for context
        semantic_similarity = ml_analysis_results.get("semantic_similarity_score", 0.0)

        # Build a personalized feedback message based on the analysis
        if semantic_similarity > 0.8:
            feedback_text += (
                "Your answer is excellent and closely matches what we're looking for. "
            )
        elif semantic_similarity > 0.6:
            feedback_text += "Your answer is good and covers most of the key points. "
        elif semantic_similarity > 0.4:
            feedback_text += (
                "Your answer addresses some important aspects but could be improved. "
            )
        else:
            feedback_text += "Your answer needs significant improvement to fully address the question. "

        # Add specific feedback about concepts covered
        if concepts_covered:
            feedback_text += (
                f"You've successfully addressed: {', '.join(concepts_covered)}. "
            )

        # Add specific feedback about concepts missed
        if concepts_missed:
            error_identified = True
            feedback_text += f"You should also consider including information about: {', '.join(concepts_missed)}. "

        # Add specific feedback about identified errors
        identified_errors = ml_analysis_results.get("identified_errors", [])
        if identified_errors:
            error_identified = True
            error_types.extend(identified_errors)

            for error in identified_errors:
                if error == "factual_inaccuracy":
                    feedback_text += (
                        "There appear to be some factual inaccuracies in your answer. "
                    )
                elif error == "conceptual_misunderstanding":
                    feedback_text += (
                        "You seem to have a misunderstanding of some key concepts. "
                    )
                elif error == "incomplete_explanation":
                    feedback_text += "Your explanation could be more complete. "
                elif error == "logical_fallacy":
                    feedback_text += (
                        "There are some logical inconsistencies in your reasoning. "
                    )
                elif error == "irrelevant_content":
                    feedback_text += "Some parts of your answer don't seem relevant to the question. "

        # Add recommendations for improvement based on skill gaps
        if skill_gaps:
            feedback_text += "To improve, focus on developing your understanding of: "
            feedback_text += ", ".join([gap.replace("_", " ") for gap in skill_gaps])
            feedback_text += ". "

        # Add resource recommendations if available
        if recommended_resources:
            feedback_text += "Here are some resources that might help you improve: "
            resource_mentions = [
                f"{resource.title} ({resource.type})"
                for resource in recommended_resources[:2]
            ]
            feedback_text += ", ".join(resource_mentions)
            feedback_text += "."

        # Create the final feedback response data
        feedback_data = FeedbackResponseData(
            feedback_text=feedback_text,
            error_identified=error_identified,
            error_type=error_types if error_types else None,
            confidence_score=confidence_score,
            concepts_covered=concepts_covered if concepts_covered else None,
            concepts_missed=concepts_missed if concepts_missed else None,
            recommended_resources=(
                recommended_resources if recommended_resources else None
            ),
        )

        logger.debug(f"Generated feedback: {feedback_data}")
        return feedback_data

    except Exception as e:
        logger.error(f"Error generating feedback: {e}", exc_info=True)
        # Provide fallback feedback in case of error
        return FeedbackResponseData(
            feedback_text="We were unable to generate detailed feedback. Please try again later.",
            error_identified=False,
            error_type=None,
            confidence_score=0.0,
            concepts_covered=None,
            concepts_missed=None,
            recommended_resources=None,
        )
