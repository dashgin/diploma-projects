#!/usr/bin/env python3
"""
Training script for the error classifier model.

This script trains a new error classifier model using the SciEntsBank dataset
and the custom pedagogical schema defined in the training module.

Usage:
    python scripts/train_model.py [--output-dir OUTPUT_DIR] [--config CONFIG_FILE]
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.modules.model_training import train_error_classifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("training.log")
    ]
)
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> dict:
    """Load training configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config from {config_path}: {e}")
        return {}


def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description="Train error classifier model")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="app/models/error_classifier",
        help="Directory to save the trained model (default: app/models/error_classifier)"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to training configuration JSON file"
    )
    parser.add_argument(
        "--no-gpu",
        action="store_true",
        help="Disable GPU usage even if available"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        help="Number of training epochs (overrides config)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        help="Training batch size (overrides config)"
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        help="Learning rate (overrides config)"
    )
    
    args = parser.parse_args()
    
    logger.info("Starting model training...")
    logger.info(f"Output directory: {args.output_dir}")
    
    # Load configuration
    config = {}
    if args.config:
        config = load_config(args.config)
        logger.info(f"Loaded configuration from {args.config}")
    
    # Override config with command line arguments
    if args.epochs:
        config["num_epochs"] = args.epochs
    if args.batch_size:
        config["batch_size"] = args.batch_size
    if args.learning_rate:
        config["learning_rate"] = args.learning_rate
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Train the model
        model_path = train_error_classifier(
            output_dir=args.output_dir,
            config=config,
            use_gpu=not args.no_gpu
        )
        
        logger.info(f"Training completed successfully!")
        logger.info(f"Model saved to: {model_path}")
        
        # Save training configuration for reference
        config_save_path = os.path.join(args.output_dir, "training_config.json")
        with open(config_save_path, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"Training configuration saved to: {config_save_path}")
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 