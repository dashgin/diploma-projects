"""
Error classifier training module.
Implements fine-tuning of DistilBERT for custom error classification.
"""

import logging
import os
from pathlib import Path

import numpy as np
import pandas as pd
from datasets import Dataset, DatasetDict
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from transformers import (
    DistilBertForSequenceClassification,
    DistilBertTokenizerFast,
    Trainer,
    TrainingArguments,
)

# Configure logger
logger = logging.getLogger(__name__)

# --- Configuration ---
# Base directory is the current file's directory
BASE_DIR = Path(__file__).parent.resolve()

# Default file paths and model configuration
DATA_FILE_PATH = BASE_DIR / "training_data" / "error_classification_data.csv"
MODEL_NAME = "distilbert-base-uncased"  # Pre-trained model to fine-tune
OUTPUT_DIR = BASE_DIR / "outputs"  # Directory to save fine-tuned model
LOGGING_DIR = BASE_DIR / "logs"  # Directory for training logs

# Define error categories and map them to integer labels
LABEL_MAP = {
    0: "no_error",
    1: "factual_inaccuracy",
    2: "conceptual_misunderstanding",
    3: "incomplete_explanation",
    4: "logical_fallacy",
    5: "irrelevant_content",
}
NUM_LABELS = len(LABEL_MAP)

# Training Hyperparameters
NUM_TRAIN_EPOCHS = 3
PER_DEVICE_TRAIN_BATCH_SIZE = 8  # Adjust based on GPU memory
PER_DEVICE_EVAL_BATCH_SIZE = 16
LEARNING_RATE = 5e-5
WARMUP_STEPS = 100
WEIGHT_DECAY = 0.01
MAX_LENGTH = 128  # Max sequence length for tokenizer


# --- Helper Functions ---
def load_and_prepare_data(file_path, tokenizer_name, test_size=0.2):
    """Loads data from CSV, tokenizes, and splits into train/eval sets."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded data with {len(df)} samples.")
        if "text" not in df.columns or "label" not in df.columns:
            raise ValueError("CSV must contain 'text' and 'label' columns.")
    except FileNotFoundError:
        logger.error(f"Error: Data file not found at {file_path}")
        logger.error("Please create CSV with 'text' and 'label' columns.")
        return None

    texts = df["text"].tolist()
    labels = df["label"].tolist()

    # Check if we have enough samples for stratified splitting
    n_samples = len(texts)
    n_classes = len(set(labels))
    min_test_samples = n_classes  # Need at least one sample per class in test set

    # Calculate test size ensuring minimum samples per class
    actual_test_size = max(test_size, min_test_samples / n_samples)

    # If dataset is too small for proper stratification, just do a regular split
    use_stratify = (n_samples >= n_classes * 3) and (len(set(labels)) > 1)

    logger.info(f"Dataset has {n_samples} samples across {n_classes} classes")
    logger.info(
        f"Using stratification: {use_stratify}, test size: {actual_test_size:.2f}"
    )

    # Split data
    train_texts, eval_texts, train_labels, eval_labels = train_test_split(
        texts,
        labels,
        test_size=actual_test_size,
        random_state=42,
        stratify=labels if use_stratify else None,
    )

    # Tokenize
    logger.info("Tokenizing texts...")
    tokenizer = DistilBertTokenizerFast.from_pretrained(tokenizer_name)
    train_encodings = tokenizer(
        train_texts, truncation=True, padding=True, max_length=MAX_LENGTH
    )
    eval_encodings = tokenizer(
        eval_texts, truncation=True, padding=True, max_length=MAX_LENGTH
    )

    # Create Hugging Face Dataset objects
    train_dataset = Dataset.from_dict(
        {
            "input_ids": train_encodings["input_ids"],
            "attention_mask": train_encodings["attention_mask"],
            "labels": train_labels,
        }
    )

    eval_dataset = Dataset.from_dict(
        {
            "input_ids": eval_encodings["input_ids"],
            "attention_mask": eval_encodings["attention_mask"],
            "labels": eval_labels,
        }
    )

    logger.info(f"Created train dataset with {len(train_dataset)} samples")
    logger.info(f"Created evaluation dataset with {len(eval_dataset)} samples")

    return DatasetDict({"train": train_dataset, "eval": eval_dataset}), tokenizer


def compute_metrics(pred):
    """Computes evaluation metrics."""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="macro", zero_division=0
    )
    acc = accuracy_score(labels, preds)

    # For per-class metrics
    class_precision, class_recall, class_f1, _ = precision_recall_fscore_support(
        labels, preds, average=None, labels=list(LABEL_MAP.keys()), zero_division=0
    )

    # Log per-class metrics
    for i, label_name in LABEL_MAP.items():
        if i < len(class_precision):
            logger.info(
                f"Class: {label_name} (ID: {i}) - "
                f"Precision: {class_precision[i]:.4f}, "
                f"Recall: {class_recall[i]:.4f}, "
                f"F1: {class_f1[i]:.4f}"
            )

    return {
        "accuracy": acc,
        "f1_macro": f1,
        "precision_macro": precision,
        "recall_macro": recall,
    }


# --- Main Training Logic ---
def train(
    data_file=DATA_FILE_PATH,
    model_name=MODEL_NAME,
    output_dir=OUTPUT_DIR,
    logging_dir=LOGGING_DIR,
    num_epochs=NUM_TRAIN_EPOCHS,
    train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
    eval_batch_size=PER_DEVICE_EVAL_BATCH_SIZE,
    learning_rate=LEARNING_RATE,
    create_dummy_data=False,
):
    """Train the error classifier model with the given parameters."""

    # Ensure directories exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(logging_dir, exist_ok=True)

    if data_file.parent != BASE_DIR:
        os.makedirs(data_file.parent, exist_ok=True)

    logger.info("--- Starting Custom Error Classifier Training ---")

    # Create dummy data if requested or if file doesn't exist
    if create_dummy_data or not os.path.exists(data_file):
        logger.info(f"Creating a dummy dataset for demonstration at {data_file}")
        _create_dummy_dataset(data_file)

    # 1. Load and Prepare Data
    logger.info(f"Loading data from: {data_file}")
    tokenized_datasets, tokenizer = load_and_prepare_data(data_file, model_name)
    if tokenized_datasets is None:
        logger.error("Failed to load data. Exiting.")
        return None, None

    # 2. Load Pre-trained Model
    logger.info(f"Loading pre-trained model: {model_name}")
    try:
        model = DistilBertForSequenceClassification.from_pretrained(
            model_name, num_labels=NUM_LABELS
        )
        # Set the label map in the model config
        model.config.id2label = LABEL_MAP
        model.config.label2id = {v: k for k, v in LABEL_MAP.items()}
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None, None

    # 3. Define Training Arguments
    logger.info("Defining training arguments...")
    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=num_epochs,
        per_device_train_batch_size=train_batch_size,
        per_device_eval_batch_size=eval_batch_size,
        learning_rate=learning_rate,
        warmup_steps=WARMUP_STEPS,
        weight_decay=WEIGHT_DECAY,
        logging_dir=str(logging_dir),
        logging_steps=max(
            1, int(len(tokenized_datasets["train"]) / train_batch_size / 10)
        ),
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        greater_is_better=True,
        report_to="none",  # Disables wandb/tensorboard reporting for simplicity
    )

    # 4. Initialize Trainer
    logger.info("Initializing Trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["eval"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    # 5. Start Fine-tuning
    logger.info("Starting model fine-tuning...")
    try:
        trainer.train()
    except Exception as e:
        logger.error(f"An error occurred during training: {e}")
        return None, None

    logger.info("Fine-tuning finished.")

    # 6. Evaluate the Best Model
    logger.info("\nEvaluating the best model on the evaluation set:")
    eval_results = trainer.evaluate()
    logger.info(f"Evaluation results: {eval_results}")

    # 7. Save the Best Model and Tokenizer
    final_model_path = output_dir / "fine_tuned_distilbert_error_classifier"
    logger.info(f"Saving the best model to: {final_model_path}")
    trainer.save_model(str(final_model_path))
    tokenizer.save_pretrained(str(final_model_path))
    logger.info("Model and tokenizer saved.")

    # Display confusion matrix for more detailed analysis
    logger.info("Generating confusion matrix...")
    predictions, labels, _ = trainer.predict(tokenized_datasets["eval"])
    preds = np.argmax(predictions, axis=1)
    cm = confusion_matrix(labels, preds, labels=list(LABEL_MAP.keys()))
    logger.info("\nConfusion Matrix (Rows: True Labels, Columns: Predicted Labels):")
    logger.info(f"Labels: {LABEL_MAP}")
    logger.info(f"Matrix:\n{cm}")

    logger.info("\n--- Custom Error Classifier Training Complete ---")

    return final_model_path, tokenizer


def _create_dummy_dataset(file_path):
    """Creates a dummy dataset for demonstration purposes."""
    # Create more samples per class to ensure proper stratification
    dummy_data = {
        "text": [
            # Factual inaccuracy (class 1)
            "The earth revolves around the moon.",
            "Water boils at 50 degrees Celsius.",
            "Humans have three lungs.",
            "The capital of France is London.",
            "Photosynthesis occurs in animal cells.",
            # Conceptual misunderstanding (class 2)
            "I was asked for causes, but I listed effects.",
            "I think the question is about something else.",
            "The formula calculates volume but I need area.",
            "I confused correlation with causation.",
            "Nuclear fusion is the splitting of atoms.",
            # Incomplete explanation (class 3)
            "My explanation is not complete.",
            "The argument lacks supporting details.",
            "I only covered part of the topic.",
            "I did not explain the second part.",
            "My answer lacks examples to illustrate.",
            # Logical fallacy (class 4)
            "All birds can fly, penguins are birds, so penguins can fly.",
            "If it's raining, the ground is wet. The ground is wet, so it must be raining.",
            "Everyone in that country is poor because I met a poor person from there.",
            "The medicine worked because I got better after taking it.",
            "Scientists were wrong before, so they must be wrong now too.",
            # Irrelevant content (class 5)
            "This topic is not related to the question.",
            "I don't know.",
            "I would like to discuss something else instead.",
            "The weather was nice yesterday.",
            "I prefer to study history instead of science.",
            # No error (class 0)
            "The answer is correct and well explained.",
            "This is a perfect response.",
            "My explanation covers all key points accurately.",
            "I've addressed the question comprehensively.",
            "The response is both accurate and thorough.",
        ],
        "label": [
            # 5 samples per class
            1,
            1,
            1,
            1,
            1,  # Factual inaccuracy
            2,
            2,
            2,
            2,
            2,  # Conceptual misunderstanding
            3,
            3,
            3,
            3,
            3,  # Incomplete explanation
            4,
            4,
            4,
            4,
            4,  # Logical fallacy
            5,
            5,
            5,
            5,
            5,  # Irrelevant content
            0,
            0,
            0,
            0,
            0,  # No error
        ],
    }

    # Ensure NUM_LABELS matches the number of unique labels
    unique_labels = set(dummy_data["label"])
    if NUM_LABELS != len(unique_labels):
        logger.warning(
            f"Warning: NUM_LABELS ({NUM_LABELS}) does not match unique labels "
            f"in dummy data ({len(unique_labels)}). Adjust NUM_LABELS."
        )

    df_dummy = pd.DataFrame(dummy_data)
    # Make sure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df_dummy.to_csv(file_path, index=False)
    logger.info(
        f"Dummy dataset created at {file_path} with {len(df_dummy)} samples. "
        f"Replace with real data for production."
    )


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(BASE_DIR, "training.log")),
        ],
    )

    # Run the training
    train(create_dummy_data=True)
