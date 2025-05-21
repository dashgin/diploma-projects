"""
NLP/ML analysis module for deep semantic understanding and error classification.
Uses modern transformer-based models for text analysis.
"""

import logging
import os
from functools import lru_cache
from typing import Any

import torch

# For sentence embeddings and semantic similarity
try:
    from sentence_transformers import SentenceTransformer
    from sentence_transformers import util as st_util
except ImportError:
    SentenceTransformer = None
    st_util = None

# For advanced transformer models
try:
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
except ImportError:
    AutoTokenizer = None
    AutoModelForSequenceClassification = None

# Local modules
from app.core.config import settings

from . import preprocessing

# Configure logger
logger = logging.getLogger(__name__)

# Global variables to hold loaded models
semantic_similarity_model: Any | None = None
error_classifier_tokenizer: Any | None = None
error_classifier_model: Any | None = None

# Error classification labels
ERROR_LABELS = {
    0: "no_error",
    1: "factual_inaccuracy",
    2: "conceptual_misunderstanding",
    3: "incomplete_explanation",
    4: "logical_fallacy",
    5: "irrelevant_content",
}


def models_loaded() -> bool:
    """Check if the ML models are loaded."""
    # Return True if at least the semantic similarity model is loaded
    # This allows the service to run even if the error classifier fails
    return semantic_similarity_model is not None


def load_models() -> None:
    """
    Load all necessary NLP/ML models into memory.
    This should be called at application startup.
    """
    global semantic_similarity_model, error_classifier_tokenizer, error_classifier_model

    # Load semantic similarity model
    load_semantic_model()

    # Load error classifier model
    load_error_classifier()


def load_semantic_model() -> None:
    """Load the semantic similarity model."""
    global semantic_similarity_model

    try:
        logger.info("Loading semantic similarity model...")

        if SentenceTransformer:
            # Use the model name from configuration
            semantic_similarity_model = SentenceTransformer(
                settings.SEMANTIC_MODEL_NAME
            )
            logger.info(
                f"Semantic similarity model '{settings.SEMANTIC_MODEL_NAME}' loaded successfully."
            )
        else:
            logger.warning(
                "SentenceTransformer library not available. Semantic similarity will be disabled."
            )
    except Exception as e:
        logger.error(f"Failed to load semantic similarity model: {e}", exc_info=True)
        semantic_similarity_model = None


def load_error_classifier() -> None:
    """Load the error classifier model."""
    global error_classifier_tokenizer, error_classifier_model

    try:
        logger.info("Loading error classifier model...")

        if not AutoTokenizer or not AutoModelForSequenceClassification:
            logger.warning(
                "Transformers library not available. Error classification will be disabled."
            )
            return

        model_path = settings.ERROR_CLASSIFIER_MODEL_PATH

        # Check if model exists at path
        if os.path.exists(model_path) and os.path.isdir(model_path):
            try:
                error_classifier_tokenizer = AutoTokenizer.from_pretrained(model_path)
                error_classifier_model = (
                    AutoModelForSequenceClassification.from_pretrained(model_path)
                )
                logger.info(f"Error classifier model loaded from {model_path}")
            except Exception as e:
                logger.error(
                    f"Failed to load model from {model_path}: {e}", exc_info=True
                )
                # Fall back to default model
                load_fallback_model()
        else:
            logger.warning(
                f"Model not found at {model_path}. Using fallback model for development."
            )
            load_fallback_model()

    except Exception as e:
        logger.error(f"Failed to load error classifier model: {e}", exc_info=True)
        error_classifier_tokenizer = None
        error_classifier_model = None


def load_fallback_model() -> None:
    """Load a fallback model when the custom model is not available."""
    global error_classifier_tokenizer, error_classifier_model

    try:
        model_name = settings.FALLBACK_MODEL_NAME
        logger.info(f"Loading fallback model: {model_name}")

        error_classifier_tokenizer = AutoTokenizer.from_pretrained(model_name)
        error_classifier_model = AutoModelForSequenceClassification.from_pretrained(
            model_name, num_labels=len(ERROR_LABELS)
        )

        # Mock the id2label mapping
        error_classifier_model.config.id2label = ERROR_LABELS
        error_classifier_model.eval()

        logger.info("Fallback error classifier model ready.")
    except Exception as e:
        logger.error(f"Failed to load fallback model: {e}", exc_info=True)
        error_classifier_tokenizer = None
        error_classifier_model = None


def analyze_response(
    student_answer_preprocessed: str,
    model_answer_preprocessed: str,
    key_concepts: list[str],
    context_info: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Performs deep NLP/ML analysis on the student's response.

    Args:
        student_answer_preprocessed (str): Preprocessed student's answer.
        model_answer_preprocessed (str): The preprocessed ideal/model answer.
        key_concepts (List[str]): List of expected key concepts.
        context_info (Optional[Dict[str, str]]): Additional context (e.g., {"difficulty": "hard"}).

    Returns:
        Dict[str, Any]: Analysis results including semantic similarity, identified errors,
                        identified concepts, and a confidence score.
    """
    # Check if models are loaded
    if not models_loaded():
        logger.error("Attempted to analyze response, but AI models are not loaded.")
        raise RuntimeError("AI models are not loaded. Cannot perform analysis.")

    results = {
        "semantic_similarity_score": 0.0,
        "identified_errors": [],
        "identified_concepts": [],
        "confidence_score": 0.0,
    }

    # Calculate semantic similarity between student answer and model answer
    similarity_score = calculate_semantic_similarity(
        student_answer_preprocessed, model_answer_preprocessed
    )
    results["semantic_similarity_score"] = similarity_score

    # Identify errors using the error classifier (if available)
    errors, confidence = classify_errors(student_answer_preprocessed)
    if errors:
        results["identified_errors"] = errors
    results["confidence_score"] = confidence

    # Identify concepts covered in the student's answer
    results["identified_concepts"] = identify_concepts(
        student_answer_preprocessed, tuple(key_concepts)
    )

    return results


@lru_cache(maxsize=128)
def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts using sentence embeddings.
    Results are cached for better performance.

    Args:
        text1 (str): First text
        text2 (str): Second text

    Returns:
        float: Similarity score between 0 and 1
    """
    if not semantic_similarity_model or not text1 or not text2:
        return 0.0

    try:
        # Encode texts to get embeddings
        embedding1 = semantic_similarity_model.encode(text1, convert_to_tensor=True)
        embedding2 = semantic_similarity_model.encode(text2, convert_to_tensor=True)

        # Calculate cosine similarity
        similarity = float(st_util.cos_sim(embedding1, embedding2).item())
        logger.debug(f"Semantic similarity: {similarity:.4f}")
        return similarity

    except Exception as e:
        logger.error(f"Error calculating semantic similarity: {e}", exc_info=True)
        return 0.0


@lru_cache(maxsize=128)
def classify_errors(text: str) -> tuple[list[str], float]:
    """
    Classify errors in the student's answer using a transformer model.
    Results are cached for better performance.

    Args:
        text (str): The text to classify

    Returns:
        Tuple[List[str], float]: List of error types and confidence score
    """
    if not error_classifier_model or not error_classifier_tokenizer or not text:
        return [], 0.0

    try:
        # Tokenize input
        inputs = error_classifier_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=512
        )

        # Get predictions
        with torch.no_grad():
            outputs = error_classifier_model(**inputs)

        # Get probabilities
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)

        # Get predicted class and confidence
        predicted_class_id = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0, predicted_class_id].item()

        # Get error label
        error_label = error_classifier_model.config.id2label.get(
            predicted_class_id, "unknown_error"
        )

        # Only return error if not "no_error"
        if error_label != "no_error":
            return [error_label], confidence
        else:
            return [], confidence

    except Exception as e:
        logger.error(f"Error classifying text: {e}", exc_info=True)
        return [], 0.0


@lru_cache(maxsize=256)
def identify_concepts(text: str, key_concepts_tuple: tuple[str, ...]) -> list[str]:
    """
    Identify which key concepts are present in the text.
    Results are cached for better performance.

    Args:
        text (str): The text to analyze
        key_concepts_tuple (Tuple[str, ...]): Tuple of key concepts to check for

    Returns:
        List[str]: List of identified concepts
    """
    # Convert tuple back to list for processing
    key_concepts = list(key_concepts_tuple)
    identified = []

    # Simple keyword matching for now
    # In a production system, this would use more sophisticated NLP
    for concept in key_concepts:
        concept_processed = preprocessing.preprocess_text(concept).lower()
        if concept.lower() in text.lower() or concept_processed in text.lower():
            identified.append(concept)

    return identified


def identify_skill_gaps(
    ml_analysis_results: dict[str, Any], key_concepts: list[str]
) -> list[str]:
    """
    Identify skill gaps based on ML analysis results.

    Args:
        ml_analysis_results (Dict[str, Any]): Results from analyze_response
        key_concepts (List[str]): List of key concepts expected in the answer

    Returns:
        List[str]: List of skill gaps
    """
    skill_gaps = []

    # Convert identified errors to skill gaps
    for error in ml_analysis_results.get("identified_errors", []):
        if error == "factual_inaccuracy":
            skill_gaps.append("factual_knowledge")
        elif error == "conceptual_misunderstanding":
            skill_gaps.append("conceptual_understanding")
        elif error == "incomplete_explanation":
            skill_gaps.append("comprehensive_explanation")
        elif error == "logical_fallacy":
            skill_gaps.append("logical_reasoning")
        elif error == "irrelevant_content":
            skill_gaps.append("topic_relevance")

    # Check for missing concepts
    identified_concepts = set(ml_analysis_results.get("identified_concepts", []))
    for concept in key_concepts:
        if concept not in identified_concepts:
            skill_gaps.append(f"knowledge_of_{concept.lower().replace(' ', '_')}")

    # Check semantic similarity for general understanding
    similarity_score = ml_analysis_results.get("semantic_similarity_score", 0.0)
    if similarity_score < settings.SIMILARITY_THRESHOLD:
        skill_gaps.append("general_understanding")

    return list(set(skill_gaps))  # Remove duplicates
