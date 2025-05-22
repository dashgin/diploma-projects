"""
Inference script for the error classifier model.
This script provides functions to load and use the trained error classifier.
"""

import logging
import os
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Configure logger
logger = logging.getLogger(__name__)

# Base directory is the current file's directory
BASE_DIR = Path(__file__).parent.resolve()

# Default paths
DEFAULT_MODEL_PATH = BASE_DIR / "outputs" / "fine_tuned_distilbert_error_classifier"
FALLBACK_MODEL_NAME = "distilbert-base-uncased"

# Error classification labels
ERROR_LABELS = {
    0: "no_error",
    1: "factual_inaccuracy",
    2: "conceptual_misunderstanding",
    3: "incomplete_explanation",
    4: "logical_fallacy",
    5: "irrelevant_content",
}


def load_model(model_path=DEFAULT_MODEL_PATH, fallback_model_name=FALLBACK_MODEL_NAME):
    """
    Load the error classifier model and tokenizer.

    Args:
        model_path: Path to the trained model directory
        fallback_model_name: Fallback model to use if trained model doesn't exist

    Returns:
        tuple: (model, tokenizer) or (None, None) if loading fails
    """
    try:
        logger.info(f"Loading error classifier model from {model_path}")

        # Check if model exists at path
        if os.path.exists(model_path) and os.path.isdir(model_path):
            try:
                tokenizer = AutoTokenizer.from_pretrained(model_path)
                model = AutoModelForSequenceClassification.from_pretrained(model_path)
                logger.info(
                    f"Error classifier model loaded successfully from {model_path}"
                )
                return model, tokenizer
            except Exception as e:
                logger.error(f"Failed to load model from {model_path}: {e}")
                logger.info("Attempting to load fallback model...")
        else:
            logger.warning(f"Model not found at {model_path}. Using fallback model.")

        # Load fallback model
        try:
            logger.info(f"Loading fallback model: {fallback_model_name}")
            tokenizer = AutoTokenizer.from_pretrained(fallback_model_name)
            model = AutoModelForSequenceClassification.from_pretrained(
                fallback_model_name, num_labels=len(ERROR_LABELS)
            )

            # Mock the id2label mapping
            model.config.id2label = ERROR_LABELS
            model.config.label2id = {v: k for k, v in ERROR_LABELS.items()}
            model.eval()

            logger.info("Fallback error classifier model ready")
            return model, tokenizer
        except Exception as e:
            logger.error(f"Failed to load fallback model: {e}")
            return None, None

    except Exception as e:
        logger.error(f"Error in load_model: {e}")
        return None, None


def classify_error(text, model=None, tokenizer=None, model_path=DEFAULT_MODEL_PATH):
    """
    Classify errors in the given text.

    Args:
        text (str): The text to classify
        model: Pre-loaded model (optional)
        tokenizer: Pre-loaded tokenizer (optional)
        model_path (str): Path to the model directory (if model/tokenizer not provided)

    Returns:
        tuple: (list of error types, confidence score)
    """
    if text is None or text.strip() == "":
        return ["empty_response"], 1.0

    # Load model and tokenizer if not provided
    if model is None or tokenizer is None:
        model, tokenizer = load_model(model_path)
        if model is None or tokenizer is None:
            logger.error("Failed to load model for classification")
            return [], 0.0

    try:
        # Prepare the input
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        # Run the model
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        # Get predictions
        probabilities = torch.nn.functional.softmax(logits, dim=1)
        confidence, predicted_class = torch.max(probabilities, dim=1)

        # Convert to Python values
        predicted_class_id = predicted_class.item()
        confidence_score = confidence.item()

        # Get the error label
        error_label = model.config.id2label.get(predicted_class_id, "unknown")

        # Return list of errors and confidence
        errors = [] if error_label == "no_error" else [error_label]

        logger.debug(
            f"Classified text: '{text[:50]}...' as {error_label} with confidence {confidence_score:.4f}"
        )
        return errors, confidence_score

    except Exception as e:
        logger.error(f"Error during classification: {e}")
        return [], 0.0


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Load the model
    model, tokenizer = load_model()

    if model is None or tokenizer is None:
        print("Failed to load model. Exiting.")
        exit(1)

    # Example texts to classify
    examples = [
        "Mitochondria is where photosynthesis happens in plant cells.",
        "The heart pumps blood to the lungs where oxygen is added and then to the rest of the body.",
        "I don't know the answer to this question.",
        "The question asks about plants, but I will discuss animals instead.",
        "Water boils at 50 degrees Celsius and freezes at 0 degrees.",
        "This answer is complete and addresses all the key points in the question.",
    ]

    print("\n--- Error Classification Examples ---\n")

    # Classify each example
    for i, example in enumerate(examples):
        print(f'Example {i + 1}: "{example}"')
        errors, confidence = classify_error(example, model, tokenizer)

        if errors:
            print(f"  Error detected: {errors[0]}")
        else:
            print("  No error detected")

        print(f"  Confidence: {confidence:.4f}")
        print("")
