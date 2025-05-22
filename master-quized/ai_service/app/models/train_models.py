"""
Main model training script for the AI Feedback Service.
This script provides an easy interface to train the error classifier model.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add the app directory to the path for imports
BASE_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(BASE_DIR))

# Import the training module
from app.core.config import settings  # Import settings for configuration values
from app.models.error_classifier.train_classifier import train as train_classifier

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(BASE_DIR, "app", "models", "training.log")),
    ],
)

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Train AI Feedback Service models")

    # General arguments
    parser.add_argument(
        "--model",
        type=str,
        choices=["error_classifier", "all"],
        default="all",
        help="Which model to train (default: all)",
    )

    # Error classifier arguments
    parser.add_argument(
        "--data_file", type=str, help="Path to the training data CSV file"
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="distilbert-base-uncased",
        help="Pre-trained model name to fine-tune (default: distilbert-base-uncased)",
    )
    parser.add_argument(
        "--output_dir", type=str, help="Directory to save the trained model"
    )
    parser.add_argument(
        "--epochs", type=int, default=3, help="Number of training epochs (default: 3)"
    )
    parser.add_argument(
        "--train_batch_size",
        type=int,
        default=8,
        help="Training batch size (default: 8)",
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=5e-5,
        help="Learning rate (default: 5e-5)",
    )
    parser.add_argument(
        "--create_dummy_data",
        action="store_true",
        help="Create dummy data for training demonstration",
    )

    return parser.parse_args()


def main():
    """Main training function."""
    args = parse_args()

    # Get default paths from settings if available
    default_classifier_path = getattr(settings, "ERROR_CLASSIFIER_MODEL_PATH", None)

    # Train the error classifier if requested
    if args.model in ["error_classifier", "all"]:
        logger.info("=== Starting Error Classifier Training ===")

        # Construct the classifier parameters
        params = {
            "data_file": Path(args.data_file) if args.data_file else None,
            "model_name": args.model_name,
            "output_dir": Path(args.output_dir) if args.output_dir else None,
            "num_epochs": args.epochs,
            "train_batch_size": args.train_batch_size,
            "learning_rate": args.learning_rate,
            "create_dummy_data": args.create_dummy_data,
        }

        # Remove None values to use defaults from the training module
        params = {k: v for k, v in params.items() if v is not None}

        # Train the model
        try:
            model_path, _ = train_classifier(**params)
            if model_path:
                logger.info(
                    f"Error classifier training completed. Model saved to: {model_path}"
                )

                # If we have a settings path, provide instructions to copy the model
                if (
                    default_classifier_path
                    and str(model_path) != default_classifier_path
                ):
                    logger.info(
                        f"To use this model in the AI service, copy the contents of {model_path} "
                        f"to {default_classifier_path}"
                    )
            else:
                logger.error("Error classifier training failed.")
        except Exception as e:
            logger.error(
                f"An error occurred during error classifier training: {e}",
                exc_info=True,
            )

    logger.info("=== Model Training Complete ===")


if __name__ == "__main__":
    main()
