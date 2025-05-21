"""
Rule-based feedback module for deterministic checks on student responses.
Provides immediate, high-confidence feedback for clear-cut cases.
"""

import logging
from typing import Any

from . import (
    preprocessing,  # Import preprocessing module for additional preprocessing if needed
)

logger = logging.getLogger(__name__)


def apply_rules(
    student_answer_preprocessed: str,
    question_text: str,
    model_answer_preprocessed: str,
    key_concepts: list[str],
) -> dict[str, Any]:
    """
    Applies a set of predefined rules to the student's preprocessed answer.
    Returns a dictionary containing feedback information, including whether
    immediate feedback should be generated or if further ML analysis is needed.

    Args:
        student_answer_preprocessed (str): The preprocessed student's answer.
        question_text (str): The original question text.
        model_answer_preprocessed (str): The preprocessed ideal/model answer.
        key_concepts (List[str]): List of expected key concepts.

    Returns:
        Dict[str, Any]: A dictionary with feedback details.
            - "immediate_feedback" (bool): True if a rule triggered immediate feedback.
            - "feedback_text" (str): The generated feedback message.
            - "error_identified" (bool): True if an error was found.
            - "error_type" (List[str]): List of error types identified by rules.
            - "confidence_score" (float): Confidence (usually 1.0 for rule-based).
            - "concepts_covered" (List[str]): Concepts covered by rules.
            - "concepts_missed" (List[str]): Concepts missed by rules.
    """
    try:
        feedback_info = {
            "immediate_feedback": False,
            "feedback_text": "",
            "error_identified": False,
            "error_type": [],
            "confidence_score": 1.0,  # Rule-based feedback is typically high confidence
            "concepts_covered": [],
            "concepts_missed": [],
        }

        # Skip rules if empty answers
        if (
            not student_answer_preprocessed
            or not question_text
            or not model_answer_preprocessed
        ):
            logger.warning("Empty inputs detected - skipping rule-based analysis")
            return feedback_info

        # Rule 1: Answer is too short
        if len(student_answer_preprocessed.split()) < 5:
            feedback_info["immediate_feedback"] = True
            feedback_info["feedback_text"] = (
                "Your answer is very brief. Please elaborate more on your thoughts to fully address the question."
            )
            feedback_info["error_identified"] = True
            feedback_info["error_type"].append("too_short")
            logger.info("Rule: 'too_short' triggered.")
            return feedback_info  # Return immediately for critical, simple errors

        # Rule 2: Answer is identical to the question (or very similar, indicating no real answer)
        try:
            preprocessed_question = preprocessing.preprocess_text(question_text)
            if student_answer_preprocessed.strip() == preprocessed_question.strip():
                feedback_info["immediate_feedback"] = True
                feedback_info["feedback_text"] = (
                    "Your answer appears to be the same as the question. Please provide your own response."
                )
                feedback_info["error_identified"] = True
                feedback_info["error_type"].append("echo_question")
                logger.info("Rule: 'echo_question' triggered.")
                return feedback_info
        except Exception as e:
            logger.error(f"Error in rule 2 (echo question): {e}", exc_info=True)

        # Rule 3: Direct Match to Model Answer (or very close)
        try:
            similarity_threshold = 0.95  # Could be configurable
            if (
                student_answer_preprocessed == model_answer_preprocessed
                and len(model_answer_preprocessed) > 5
            ):
                feedback_info["immediate_feedback"] = True
                feedback_info["feedback_text"] = (
                    "Excellent! Your answer is spot on and covers all the key points."
                )
                feedback_info["error_identified"] = False  # No error identified
                feedback_info["concepts_covered"] = (
                    key_concepts.copy()
                )  # Assume all concepts covered if direct match
                logger.info("Rule: 'direct_model_match' triggered.")
                return feedback_info
        except Exception as e:
            logger.error(f"Error in rule 3 (direct model match): {e}", exc_info=True)

        # Rule 4: Missing critical keywords (simple check)
        try:
            identified_concepts_by_rule = []
            missed_concepts_by_rule = []

            for kc in key_concepts:
                # Check for concept presence in student's preprocessed answer
                kc_processed = preprocessing.preprocess_text(kc).lower()
                if (
                    kc.lower() in student_answer_preprocessed.lower()
                    or kc_processed in student_answer_preprocessed.lower()
                ):
                    identified_concepts_by_rule.append(kc)
                else:
                    missed_concepts_by_rule.append(kc)

            feedback_info["concepts_covered"] = identified_concepts_by_rule
            feedback_info["concepts_missed"] = missed_concepts_by_rule

            if (
                missed_concepts_by_rule
                and len(key_concepts) > 0
                and len(identified_concepts_by_rule) == 0
            ):
                # If student missed ALL key concepts and there are key concepts
                feedback_info["feedback_text"] = (
                    f"Your answer doesn't seem to cover the main points. Consider focusing on: {', '.join(missed_concepts_by_rule)}."
                )
                feedback_info["error_identified"] = True
                feedback_info["error_type"].append("all_key_concepts_missing")
                feedback_info["immediate_feedback"] = (
                    True  # Can be immediate or combined with ML
                )
                logger.info("Rule: 'all_key_concepts_missing' triggered.")
                return feedback_info
        except Exception as e:
            logger.error(f"Error in rule 4 (key concepts): {e}", exc_info=True)

        # No immediate rule-based feedback triggered, proceed to ML analysis
        logger.debug(
            "No immediate rule-based feedback triggered. Proceeding to ML analysis."
        )
        return feedback_info

    except Exception as e:
        logger.error(f"Error in rule-based analysis: {e}", exc_info=True)
        # Return empty feedback to proceed to ML analysis as fallback
        return {
            "immediate_feedback": False,
            "feedback_text": "",
            "error_identified": False,
            "error_type": [],
            "confidence_score": 0.0,
            "concepts_covered": [],
            "concepts_missed": [],
        }
