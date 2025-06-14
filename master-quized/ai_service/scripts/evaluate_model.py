#!/usr/bin/env python3
"""
Evaluation script for the error classifier model.

This script evaluates a trained error classifier model on the SciEntsBank dataset
using different splits (unseen answers, unseen questions, unseen domains).

Usage:
    python scripts/evaluate_model.py --model-path MODEL_PATH [--split SPLIT]
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.modules.model_training import evaluate_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main evaluation function."""
    parser = argparse.ArgumentParser(description="Evaluate error classifier model")
    parser.add_argument(
        "--model-path",
        type=str,
        required=True,
        help="Path to the trained model directory"
    )
    parser.add_argument(
        "--split",
        type=str,
        choices=["test_ua", "test_uq", "test_ud"],
        default="test_uq",
        help="Dataset split to evaluate on (default: test_uq for unseen questions)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to save evaluation results as JSON"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed classification report"
    )
    
    args = parser.parse_args()
    
    logger.info(f"Evaluating model: {args.model_path}")
    logger.info(f"Dataset split: {args.split}")
    
    try:
        # Evaluate the model
        results = evaluate_model(args.model_path, args.split)
        
        # Print summary metrics
        metrics = results["metrics"]
        logger.info("=== Evaluation Results ===")
        logger.info(f"F1 Score (Macro): {metrics.get('eval_f1_macro', 0):.4f}")
        logger.info(f"Precision (Macro): {metrics.get('eval_precision_macro', 0):.4f}")
        logger.info(f"Recall (Macro): {metrics.get('eval_recall_macro', 0):.4f}")
        logger.info(f"Loss: {metrics.get('eval_loss', 0):.4f}")
        
        # Show detailed classification report if requested
        if args.verbose:
            report = results["classification_report"]
            logger.info("\n=== Detailed Classification Report ===")
            
            # Print per-class metrics
            for class_name in ["no_error", "factual_inaccuracy", "conceptual_misunderstanding", 
                             "incomplete_explanation", "irrelevant_content"]:
                if class_name in report:
                    class_metrics = report[class_name]
                    logger.info(f"{class_name:25} - P: {class_metrics['precision']:.3f}, "
                              f"R: {class_metrics['recall']:.3f}, "
                              f"F1: {class_metrics['f1-score']:.3f}, "
                              f"Support: {class_metrics['support']}")
            
            # Print overall metrics
            if 'macro avg' in report:
                macro_avg = report['macro avg']
                logger.info(f"{'Macro Average':25} - P: {macro_avg['precision']:.3f}, "
                          f"R: {macro_avg['recall']:.3f}, "
                          f"F1: {macro_avg['f1-score']:.3f}")
            
            if 'weighted avg' in report:
                weighted_avg = report['weighted avg']
                logger.info(f"{'Weighted Average':25} - P: {weighted_avg['precision']:.3f}, "
                          f"R: {weighted_avg['recall']:.3f}, "
                          f"F1: {weighted_avg['f1-score']:.3f}")
        
        # Save results if output path specified
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"Results saved to: {args.output}")
        
        logger.info("Evaluation completed successfully!")
        
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 