"""
Service for integrating with the AI feedback service.
"""

import logging
from typing import Any

import httpx
from pydantic import ValidationError

from app.core.config import settings
from app.models import StudentResponse

logger = logging.getLogger(__name__)

AI_SERVICE_URL = settings.AI_SERVICE_URL
FEEDBACK_ENDPOINT = f"{AI_SERVICE_URL}/feedback/generate"
TIMEOUT = 30.0  # seconds


async def request_ai_feedback(response: StudentResponse) -> dict[str, Any]:
    """
    Request AI feedback for a student response.

    Args:
        response: The student response to generate feedback for

    Returns:
        dict containing the AI feedback data and original request

    Raises:
        Exception: If there's an error communicating with the AI service
    """
    # Get the question and attempt data
    question = response.question
    attempt = response.attempt
    quiz = attempt.quiz

    # Prepare the request data
    request_data = {
        "quiz_id": str(quiz.id),
        "question_id": str(question.id),
        "student_id": str(attempt.student_id),
        "student_answer": response.response_text,
        "question_text": question.text,
        "model_answer": question.model_answer or "",
        "key_concepts": question.key_concepts or [],
        "context_info": {
            "topic": quiz.title,
            "difficulty": question.difficulty or "medium",
        },
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            logger.info(f"Requesting AI feedback for response {response.id}")
            ai_response = await client.post(FEEDBACK_ENDPOINT, json=request_data)
            ai_response.raise_for_status()

            feedback_data = ai_response.json()
            logger.info(f"Received AI feedback for response {response.id}")

            # Return both request and response data
            return {
                "request": request_data,
                "response": feedback_data,
                "http_status": ai_response.status_code,
                "timestamp": import_datetime().now().isoformat(),
            }
    except httpx.RequestError as e:
        logger.error(f"Error communicating with AI service: {e}")
        raise Exception(f"Failed to connect to AI service: {e}")
    except httpx.HTTPStatusError as e:
        logger.error(f"AI service returned error: {e.response.text}")
        raise Exception(f"AI service error: {e.response.status_code}")
    except ValidationError as e:
        logger.error(f"Invalid response from AI service: {e}")
        raise Exception("Invalid response from AI service")
    except Exception as e:
        logger.error(f"Unexpected error requesting AI feedback: {e}")
        raise Exception("Unexpected error requesting AI feedback")


def import_datetime():
    """Import datetime module to avoid circular imports"""
    from datetime import datetime

    return datetime


async def process_ai_feedback(feedback_data: dict[str, Any]) -> dict[str, Any]:
    """
    Process the AI feedback data and extract the relevant information.

    Args:
        feedback_data: The raw feedback data from the AI service

    Returns:
        dict containing the processed feedback data
    """
    response_data = feedback_data["response"]

    if response_data.get("status") != "success" or not response_data.get("feedback"):
        raise Exception("Invalid feedback data received from AI service")

    feedback = response_data["feedback"]

    # Extract resource recommendations if available
    resources = []
    if feedback.get("recommended_resources"):
        for resource in feedback["recommended_resources"]:
            resources.append(
                {
                    "title": resource["title"],
                    "url": resource["url"],
                    "resource_type": resource["type"],
                    "relevance_score": 1.0,  # Default score
                }
            )

    # Prepare feedback content
    feedback_content = {
        "concepts_covered": feedback.get("concepts_covered", []),
        "concepts_missed": feedback.get("concepts_missed", []),
    }

    # Prepare the feedback data for storage
    processed_feedback = {
        "feedback_text": feedback["feedback_text"],
        "error_type": feedback.get("error_type"),
        "confidence_score": feedback.get("confidence_score"),
        "feedback_content": feedback_content,
        "ai_metadata": {
            "request": feedback_data["request"],
            "response": feedback_data["response"],
            "http_status": feedback_data["http_status"],
            "timestamp": feedback_data["timestamp"],
        },
        "resources": resources,
    }

    return processed_feedback
