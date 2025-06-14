"""
Model training module for fine-tuning error classification models.

This module provides functionality to train custom error classifiers
based on the pedagogical schema defined in the notebook.
"""

import logging
import os
from typing import Any, Dict, Optional

import numpy as np
import torch
from datasets import ClassLabel, load_dataset
from sklearn.metrics import classification_report, precision_recall_fscore_support
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    EvalPrediction,
    Trainer,
    TrainingArguments,
)

from app.core.config import settings

logger = logging.getLogger(__name__)

# Custom error classification labels (from notebook)
CUSTOM_LABEL_NAMES = [
    "no_error",
    "factual_inaccuracy", 
    "conceptual_misunderstanding",
    "incomplete_explanation",
    "irrelevant_content"
]

# Training configuration
DEFAULT_TRAINING_CONFIG = {
    "model_checkpoint": "bert-base-multilingual-uncased",
    "batch_size": 16,
    "learning_rate": 2e-5,
    "num_epochs": 3,
    "max_length": 128,
    "weight_decay": 0.01,
}


def create_label_mapping() -> tuple[ClassLabel, Dict[int, int]]:
    """
    Create custom labels and mapping from SciEntsBank to our pedagogical schema.
    
    Returns:
        Tuple of (custom_labels, label_mapping)
    """
    custom_labels = ClassLabel(names=CUSTOM_LABEL_NAMES)
    
    # Mapping from original SciEntsBank labels to our custom schema
    label_map = {
        0: custom_labels.str2int('no_error'),  # correct -> no_error
        1: custom_labels.str2int('factual_inaccuracy'),  # contradictory -> factual_inaccuracy
        2: custom_labels.str2int('incomplete_explanation'),  # partially_correct_incomplete -> incomplete_explanation
        3: custom_labels.str2int('irrelevant_content'),  # irrelevant -> irrelevant_content
        4: custom_labels.str2int('conceptual_misunderstanding'),  # non_domain -> conceptual_misunderstanding
    }
    
    return custom_labels, label_map


def map_labels(example: Dict[str, Any], label_map: Dict[int, int]) -> Dict[str, Any]:
    """Apply custom label mapping to dataset example."""
    original_label_id = example['label']
    example['label'] = label_map.get(original_label_id, -1)
    return example


def preprocess_function(examples: Dict[str, Any], tokenizer: AutoTokenizer, max_length: int = 128) -> Dict[str, Any]:
    """Tokenize student answers for training."""
    return tokenizer(
        [text.lower() for text in examples['student_answer']],
        truncation=True,
        padding="max_length",
        max_length=max_length
    )


def compute_metrics(p: EvalPrediction) -> Dict[str, float]:
    """Compute evaluation metrics for training."""
    preds = np.argmax(p.predictions, axis=1)
    labels = p.label_ids
    precision, recall, fscore, _ = precision_recall_fscore_support(
        labels, preds, average='macro', zero_division=0
    )
    return {
        'f1_macro': fscore,
        'precision_macro': precision,
        'recall_macro': recall,
    }


def load_and_prepare_dataset(custom_labels: ClassLabel, label_map: Dict[int, int]) -> Any:
    """Load and prepare the SciEntsBank dataset."""
    try:
        logger.info("Loading SciEntsBank dataset...")
        dataset = load_dataset('nkazi/SciEntsBank')
        
        # Apply label mapping
        dataset = dataset.map(lambda x: map_labels(x, label_map))
        dataset = dataset.cast_column('label', custom_labels)
        
        logger.info("Dataset loaded and labels mapped successfully")
        
        # Log label distribution
        for split_name in dataset:
            logger.info(f"Split '{split_name}' has {len(dataset[split_name])} examples")
        
        return dataset
        
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        raise


def train_error_classifier(
    output_dir: str,
    config: Optional[Dict[str, Any]] = None,
    use_gpu: bool = True
) -> str:
    """
    Train the error classifier model.
    
    Args:
        output_dir: Directory to save the trained model
        config: Training configuration (uses defaults if None)
        use_gpu: Whether to use GPU if available
        
    Returns:
        Path to the saved model
    """
    # Use provided config or defaults
    training_config = {**DEFAULT_TRAINING_CONFIG, **(config or {})}
    
    # Setup device
    device = "cuda" if torch.cuda.is_available() and use_gpu else "cpu"
    logger.info(f"Using device: {device}")
    
    # Create custom labels and mapping
    custom_labels, label_map = create_label_mapping()
    num_labels = custom_labels.num_classes
    
    # Load and prepare dataset
    dataset = load_and_prepare_dataset(custom_labels, label_map)
    
    # Load tokenizer
    logger.info(f"Loading tokenizer: {training_config['model_checkpoint']}")
    tokenizer = AutoTokenizer.from_pretrained(training_config['model_checkpoint'])
    
    # Tokenize dataset
    logger.info("Tokenizing dataset...")
    tokenized_dataset = dataset.map(
        lambda x: preprocess_function(x, tokenizer, training_config['max_length']),
        batched=True
    )
    tokenized_dataset = tokenized_dataset.remove_columns(['student_answer', 'id', 'question', 'reference_answer'])
    
    # Create label mappings for model
    id2label = {i: label for i, label in enumerate(custom_labels.names)}
    label2id = {label: i for i, label in id2label.items()}
    
    # Load model
    logger.info(f"Loading model: {training_config['model_checkpoint']}")
    model = AutoModelForSequenceClassification.from_pretrained(
        training_config['model_checkpoint'],
        num_labels=num_labels,
        id2label=id2label,
        label2id=label2id
    ).to(device)
    
    # Create validation split from training data
    train_splits = tokenized_dataset["train"].train_test_split(test_size=0.1, seed=42)
    train_dataset = train_splits['train']
    eval_dataset = train_splits['test']
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        learning_rate=training_config['learning_rate'],
        per_device_train_batch_size=training_config['batch_size'],
        per_device_eval_batch_size=training_config['batch_size'],
        num_train_epochs=training_config['num_epochs'],
        weight_decay=training_config['weight_decay'],
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        push_to_hub=False,
        logging_dir=f"{output_dir}/logs",
        logging_steps=50,
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
        compute_metrics=compute_metrics,
    )
    
    # Train model
    logger.info("Starting training...")
    trainer.train()
    
    # Save final model
    logger.info(f"Saving model to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Evaluate on test sets
    logger.info("Evaluating on test sets...")
    test_sets = {
        "Unseen Answers": tokenized_dataset['test_ua'],
        "Unseen Questions": tokenized_dataset['test_uq'], 
        "Unseen Domains": tokenized_dataset['test_ud'],
    }
    
    for name, test_data in test_sets.items():
        logger.info(f"Evaluating on {name}...")
        results = trainer.evaluate(test_data)
        logger.info(f"{name} - F1: {results['eval_f1_macro']:.4f}, "
                   f"Precision: {results['eval_precision_macro']:.4f}, "
                   f"Recall: {results['eval_recall_macro']:.4f}")
    
    # Generate detailed classification report for unseen questions
    logger.info("Generating detailed classification report...")
    predictions = trainer.predict(tokenized_dataset['test_uq'])
    predicted_labels = np.argmax(predictions.predictions, axis=1)
    true_labels = predictions.label_ids
    
    report = classification_report(
        true_labels,
        predicted_labels,
        labels=list(range(len(custom_labels.names))),
        target_names=custom_labels.names,
        zero_division=0
    )
    logger.info("Classification Report for Unseen Questions:")
    logger.info(f"\n{report}")
    
    logger.info("Training completed successfully!")
    return output_dir


def evaluate_model(model_path: str, dataset_split: str = "test_uq") -> Dict[str, Any]:
    """
    Evaluate a trained model on a specific dataset split.
    
    Args:
        model_path: Path to the saved model
        dataset_split: Which split to evaluate on
        
    Returns:
        Evaluation results
    """
    try:
        # Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        
        # Load dataset
        custom_labels, label_map = create_label_mapping()
        dataset = load_and_prepare_dataset(custom_labels, label_map)
        
        # Tokenize evaluation dataset
        eval_dataset = dataset[dataset_split].map(
            lambda x: preprocess_function(x, tokenizer),
            batched=True
        )
        eval_dataset = eval_dataset.remove_columns(['student_answer', 'id', 'question', 'reference_answer'])
        
        # Create trainer for evaluation
        trainer = Trainer(
            model=model,
            processing_class=tokenizer,
            compute_metrics=compute_metrics,
        )
        
        # Evaluate
        results = trainer.evaluate(eval_dataset)
        
        # Generate predictions for detailed analysis
        predictions = trainer.predict(eval_dataset)
        predicted_labels = np.argmax(predictions.predictions, axis=1)
        true_labels = predictions.label_ids
        
        # Classification report
        report = classification_report(
            true_labels,
            predicted_labels,
            labels=list(range(len(custom_labels.names))),
            target_names=custom_labels.names,
            zero_division=0,
            output_dict=True
        )
        
        return {
            "metrics": results,
            "classification_report": report,
            "predictions": predicted_labels.tolist(),
            "true_labels": true_labels.tolist(),
        }
        
    except Exception as e:
        logger.error(f"Error evaluating model: {e}")
        raise 