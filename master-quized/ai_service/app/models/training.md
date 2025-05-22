# AI Model Training Guide for Thesis Project

This guide provides step-by-step instructions and Python scripts for:
1.  Performing semantic similarity analysis using a pre-trained Sentence-Transformer model.
2.  Fine-tuning a DistilBERT model for custom error classification on your dataset.

This corresponds to the model training activities described in Chapter II (Section 2.4.2) of your thesis: "Online Quiz Application with AI Feedback."

## 1. Prerequisites

* **Python 3.7+**: Ensure you have Python installed.
* **pip**: Python package installer.
* **Virtual Environment (Recommended)**: To keep dependencies isolated.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

## 2. Installation of Libraries

Install the necessary Python libraries using pip:

```bash
pip install torch torchvision torchaudio
pip install transformers datasets sentence-transformers scikit-learn pandas
```

* `torch`: PyTorch, the deep learning framework.
* `transformers`: Hugging Face library for transformer models (like DistilBERT).
* `datasets`: Hugging Face library for easily loading and processing datasets.
* `sentence-transformers`: For using models like "all-MiniLM-L6-v2" for sentence embeddings.
* `scikit-learn`: For evaluation metrics (precision, recall, F1-score) and data splitting.
* `pandas`: For data manipulation, especially if your dataset is in CSV format.

## 3. Semantic Similarity Analysis

This part demonstrates using a pre-trained model for semantic similarity. No actual training is performed here by you; rather, you leverage an existing powerful model.

**File:** `semantic_similarity_example.py` (Code provided below)

**Instructions:**
1.  Save the code for `semantic_similarity_example.py`.
2.  Run the script from your terminal:
    ```bash
    python semantic_similarity_example.py
    ```
3.  The script will output similarity scores for the example sentences, demonstrating how you can compare a student's answer to a model answer. You will integrate this logic into your AI Feedback Service.

## 4. Custom Error Classifier Training (Fine-tuning DistilBERT)

This section guides you through fine-tuning a DistilBERT model for your specific error classification task.

### 4.1. Data Preparation

Your thesis mentions a custom-annotated dataset for error classification (details in Appendix C and §2.4.1). For the training script to work, you need to prepare your data in a format that the script can read, typically a CSV file.

**Expected CSV Format:**
Create a CSV file (e.g., `error_classification_data.csv`) with at least two columns:
* `text`: Containing the student's answer (or the text snippet to be classified).
* `label`: Containing the numerical label for the error category (e.g., 0 for "Factual Error", 1 for "Misinterpretation", 2 for "No Error/Correct", etc.).

**Example `error_classification_data.csv`:**
```csv
text,label
"Mitochondria is where photosyntesis happens.",0
"The question asks about plants but I will talk about animals.",1
"This answer is well-structured and covers all key points.",2
"Stomata are used by plants to absorb water from the air.",0
... (add more annotated examples)
```

**Important:**
* Ensure your labels are integers starting from 0 up to `num_classes - 1`.
* You will need to define `label_map` in the training script to map these integer labels back to your human-readable error category names.
* The more high-quality annotated data you have, the better your fine-tuned model will perform. For a Master's thesis, even a few hundred well-chosen examples per class can be a good starting point for fine-tuning.

### 4.2. Training Script

**File:** `train_error_classifier.py` (Code provided below)

**Key parts of the script to customize:**
* `DATA_FILE_PATH`: Update this to the path of your `error_classification_data.csv`.
* `NUM_LABELS`: Set this to the total number of unique error categories (including a "no error" or "correct" category if applicable).
* `LABEL_MAP`: Define this dictionary to map integer labels to your error category names.
* `TrainingArguments`: Adjust parameters like `num_train_epochs`, `per_device_train_batch_size`, `output_dir`, etc., based on your dataset size and computational resources.

### 4.3. Running the Training

1.  Save the code for `train_error_classifier.py`.
2.  Ensure your `error_classification_data.csv` is in the specified path.
3.  Run the training script from your terminal:
    ```bash
    python train_error_classifier.py
    ```
4.  The script will:
    * Load and preprocess your data.
    * Split it into training and evaluation sets.
    * Load the pre-trained DistilBERT model and tokenizer.
    * Fine-tune the model on your training data.
    * Evaluate the model on the evaluation set at the end of each epoch (if `evaluation_strategy="epoch"`).
    * Print classification reports (precision, recall, F1-score) for the evaluation set.
    * Save the best performing model and the tokenizer to the directory specified in `TrainingArguments` (e.g., `./results_error_classifier/fine_tuned_distilbert_error_classifier`).

### 4.4. Using the Fine-tuned Model

After training, the `train_error_classifier.py` script also includes a commented-out section demonstrating how to load your fine-tuned model and tokenizer from the save directory to make predictions on new text. You will adapt this loading mechanism for your AI Feedback Service.

## 5. Next Steps for Thesis

* **Document Results:** Use the output metrics (Precision, Recall, F1-score, confusion matrix if you generate one) from `train_error_classifier.py` for section 3.2.1 of your thesis.
* **Scenario Demonstration:** Use the `get_semantic_similarity` function and the logic for loading/using your fine-tuned error classifier to build the examples for section 3.2.2.
* **Integrate into AI Service:** Adapt the core logic from these scripts for use within your FastAPI-based AI Feedback Service.

This guide should provide a practical pathway for implementing and evaluating the core AI models for your thesis. Remember that model training, especially fine-tuning, can be an iterative process involving experimentation with hyperparameters and potentially data augmentation if your dataset is very small.
```python
# semantic_similarity_example.py

# Ensure you have the library installed: pip install sentence-transformers torch
from sentence_transformers import SentenceTransformer, util
import torch

# --- Configuration ---
# Model recommended in the thesis for semantic similarity
SEMANTIC_SIMILARITY_MODEL_NAME = 'all-MiniLM-L6-v2'

# --- Core Function ---
def get_semantic_similarity(text1: str, text2: str, model_name: str = SEMANTIC_SIMILARITY_MODEL_NAME) -> float:
    """
    Computes the semantic similarity between two texts using a pre-trained
    Sentence-Transformer model.

    Args:
        text1: The first text string (e.g., student's answer).
        text2: The second text string (e.g., model answer).
        model_name: The name of the SentenceTransformer model to use.

    Returns:
        A float representing the cosine similarity score (between -1 and 1, typically 0 to 1 for positive similarity).
        Returns 0.0 if an error occurs.
    """
    try:
        # Load the pre-trained model.
        # This will download the model if it's not already cached locally.
        model = SentenceTransformer(model_name)
    except Exception as e:
        print(f"Error loading SentenceTransformer model '{model_name}': {e}")
        print("Please ensure the model name is correct and you have an internet connection if downloading for the first time.")
        return 0.0

    # Generate embeddings for both texts.
    # Embeddings are dense vector representations of the text.
    try:
        print(f"\nGenerating embedding for: '{text1}'")
        embedding1 = model.encode(text1, convert_to_tensor=True)
        print(f"Generating embedding for: '{text2}'")
        embedding2 = model.encode(text2, convert_to_tensor=True)
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return 0.0

    # Compute cosine similarity between the embeddings.
    # Cosine similarity measures the cosine of the angle between two vectors,
    # indicating how similar they are in direction (and thus, often, in meaning).
    try:
        cosine_score = util.pytorch_cos_sim(embedding1, embedding2)
        # .item() extracts the Python number from a single-element PyTorch tensor.
        similarity_value = cosine_score.item()
        return similarity_value
    except Exception as e:
        print(f"Error computing cosine similarity: {e}")
        return 0.0

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Semantic Similarity Example ---")

    student_answer_example1 = "Mitochondria are the powerhouses of the cell, responsible for generating most of the cell's supply of ATP through cellular respiration."
    model_answer_example1 = "The primary function of mitochondria is to generate the majority of the cell's supply of adenosine triphosphate (ATP), used as a source of chemical energy via cellular respiration."
    
    similarity_score1 = get_semantic_similarity(student_answer_example1, model_answer_example1)
    print(f"\nStudent Answer: '{student_answer_example1}'")
    print(f"Model Answer:   '{model_answer_example1}'")
    print(f"Semantic Similarity Score: {similarity_score1:.4f}")

    student_answer_example2 = "The nucleus controls the cell's activities and contains the genetic material."
    similarity_score2 = get_semantic_similarity(student_answer_example2, model_answer_example1)
    print(f"\nStudent Answer: '{student_answer_example2}'")
    print(f"Model Answer:   '{model_answer_example1}'")
    print(f"Semantic Similarity Score (different topic): {similarity_score2:.4f}")

    student_answer_example3 = "Plants use sunlight for photosynthesis."
    model_answer_example3 = "Photosynthesis in plants converts light energy into chemical energy."
    similarity_score3 = get_semantic_similarity(student_answer_example3, model_answer_example3)
    print(f"\nStudent Answer: '{student_answer_example3}'")
    print(f"Model Answer:   '{model_answer_example3}'")
    print(f"Semantic Similarity Score (related topic): {similarity_score3:.4f}")

    # Example with very short, potentially problematic input
    student_answer_short = "Energy."
    similarity_score_short = get_semantic_similarity(student_answer_short, model_answer_example1)
    print(f"\nStudent Answer: '{student_answer_short}'")
    print(f"Model Answer:   '{model_answer_example1}'")
    print(f"Semantic Similarity Score (short answer): {similarity_score_short:.4f}")
```python
# train_error_classifier.py

# Ensure you have the libraries installed:
# pip install torch torchvision torchaudio
# pip install transformers datasets scikit-learn pandas

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from datasets import Dataset, DatasetDict
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
import torch
import numpy as np # For confusion matrix processing if needed

# --- Configuration ---
# IMPORTANT: Update these paths and parameters according to your setup
DATA_FILE_PATH = "error_classification_data.csv"  # Path to your CSV data file
MODEL_NAME = "distilbert-base-uncased"           # Pre-trained model to fine-tune
OUTPUT_DIR = "./results_error_classifier"        # Directory to save fine-tuned model and logs
LOGGING_DIR = "./logs_error_classifier"          # Directory for training logs

# Define your error categories and map them to integer labels
# Example:
LABEL_MAP = {
    0: "Factual Error",
    1: "Misinterpretation",
    2: "Incomplete Argument",
    3: "Off-Topic",
    4: "No Error/Correct" # It's good practice to have a "correct" or "no specific error" class
}
NUM_LABELS = len(LABEL_MAP)

# Training Hyperparameters (adjust as needed)
NUM_TRAIN_EPOCHS = 3
PER_DEVICE_TRAIN_BATCH_SIZE = 8 # Adjust based on your GPU memory
PER_DEVICE_EVAL_BATCH_SIZE = 16
LEARNING_RATE = 5e-5
WARMUP_STEPS = 100
WEIGHT_DECAY = 0.01
MAX_LENGTH = 128 # Max sequence length for tokenizer

# --- Helper Functions ---
def load_and_prepare_data(file_path: str, tokenizer_name: str, test_size: float = 0.2):
    """Loads data from CSV, tokenizes, and splits into train/eval sets."""
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded data with {len(df)} samples.")
        if 'text' not in df.columns or 'label' not in df.columns:
            raise ValueError("CSV must contain 'text' and 'label' columns.")
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}")
        print("Please create 'error_classification_data.csv' with 'text' and 'label' columns.")
        return None

    texts = df['text'].tolist()
    labels = df['label'].tolist()

    # Split data
    train_texts, eval_texts, train_labels, eval_labels = train_test_split(
        texts, labels, test_size=test_size, random_state=42, stratify=labels if len(set(labels)) > 1 else None
    )

    # Tokenize
    tokenizer = DistilBertTokenizerFast.from_pretrained(tokenizer_name)
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=MAX_LENGTH)
    eval_encodings = tokenizer(eval_texts, truncation=True, padding=True, max_length=MAX_LENGTH)

    # Create Hugging Face Dataset objects
    train_dataset = Dataset.from_dict({'input_ids': train_encodings['input_ids'],
                                       'attention_mask': train_encodings['attention_mask'],
                                       'labels': train_labels})
    eval_dataset = Dataset.from_dict({'input_ids': eval_encodings['input_ids'],
                                      'attention_mask': eval_encodings['attention_mask'],
                                      'labels': eval_labels})
    
    return DatasetDict({'train': train_dataset, 'eval': eval_dataset}), tokenizer

def compute_metrics(pred):
    """Computes evaluation metrics."""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='macro', zero_division=0)
    acc = accuracy_score(labels, preds)
    
    # For per-class metrics (optional, but good for thesis)
    # class_precision, class_recall, class_f1, _ = precision_recall_fscore_support(labels, preds, average=None, labels=list(LABEL_MAP.keys()), zero_division=0)
    # for i, label_name in LABEL_MAP.items():
    #     print(f"Class: {label_name} (ID: {i}) - Precision: {class_precision[i]:.4f}, Recall: {class_recall[i]:.4f}, F1: {class_f1[i]:.4f}")

    return {
        'accuracy': acc,
        'f1_macro': f1,
        'precision_macro': precision,
        'recall_macro': recall,
    }

# --- Main Training Logic ---
def main():
    print("--- Starting Custom Error Classifier Training ---")

    # 1. Load and Prepare Data
    print(f"Loading data from: {DATA_FILE_PATH}")
    tokenized_datasets, tokenizer = load_and_prepare_data(DATA_FILE_PATH, MODEL_NAME)
    if tokenized_datasets is None:
        return

    # 2. Load Pre-trained Model
    print(f"Loading pre-trained model: {MODEL_NAME}")
    try:
        model = DistilBertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_LABELS)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # 3. Define Training Arguments
    print("Defining training arguments...")
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=NUM_TRAIN_EPOCHS,
        per_device_train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
        per_device_eval_batch_size=PER_DEVICE_EVAL_BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        warmup_steps=WARMUP_STEPS,
        weight_decay=WEIGHT_DECAY,
        logging_dir=LOGGING_DIR,
        logging_steps=max(1, int(len(tokenized_datasets['train']) / PER_DEVICE_TRAIN_BATCH_SIZE / 10)), # Log 10 times per epoch
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro", # Ensure this matches a key in compute_metrics output
        greater_is_better=True,
        report_to="none" # Disables wandb/tensorboard reporting for simplicity in this script
    )

    # 4. Initialize Trainer
    print("Initializing Trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['eval'],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    # 5. Start Fine-tuning
    print("Starting model fine-tuning...")
    try:
        trainer.train()
    except Exception as e:
        print(f"An error occurred during training: {e}")
        return

    print("Fine-tuning finished.")

    # 6. Evaluate the Best Model
    print("\nEvaluating the best model on the evaluation set:")
    eval_results = trainer.evaluate()
    print(f"Evaluation results: {eval_results}")

    # 7. Save the Best Model and Tokenizer
    fine_tuned_model_path = f"{OUTPUT_DIR}/fine_tuned_model"
    print(f"Saving the best model to: {fine_tuned_model_path}")
    trainer.save_model(fine_tuned_model_path)
    tokenizer.save_pretrained(fine_tuned_model_path)
    print("Model and tokenizer saved.")

    # (Optional) Display confusion matrix for more detailed analysis
    # This part requires predictions on the eval set after training
    # predictions, labels, _ = trainer.predict(tokenized_datasets["eval"])
    # preds = np.argmax(predictions, axis=1)
    # cm = confusion_matrix(labels, preds, labels=list(LABEL_MAP.keys()))
    # print("\nConfusion Matrix (Rows: True Labels, Columns: Predicted Labels):")
    # print(LABEL_MAP) # To help interpret axis
    # print(cm)
    # You might want to use a library like seaborn or matplotlib to plot this for your thesis.

    print("\n--- Custom Error Classifier Training Complete ---")


if __name__ == "__main__":
    # Ensure the script is runnable
    # You would need to create the dummy 'error_classification_data.csv' for this to run
    # For example:
    # text,label
    # "This is a factual error about history.",0
    # "The question was about biology, not chemistry.",1
    # "I explained it well.",4
    # "The sun is a planet.",0
    # "I did not understand what to write.",1
    # "This answer is okay.",4
    # "My answer is very short.",2
    # "The earth is flat.",0
    
    # Create a dummy CSV for testing if it doesn't exist
    try:
        pd.read_csv(DATA_FILE_PATH)
    except FileNotFoundError:
        print(f"Creating a dummy '{DATA_FILE_PATH}' for demonstration purposes.")
        dummy_data = {
            'text': [
                "The earth revolves around the moon.",
                "I was asked for causes, but I listed effects.",
                "My explanation is not complete.",
                "This topic is not related to the question.",
                "The answer is correct and well explained.",
                "Water boils at 50 degrees Celsius.",
                "I think the question is about something else.",
                "The argument lacks supporting details.",
                "I don't know.",
                "This is a perfect response."
            ],
            'label': [0, 1, 2, 3, 4, 0, 1, 2, 3, 4] # Example labels for 5 classes
        }
        # Ensure NUM_LABELS matches the number of unique labels here if using this dummy data
        if NUM_LABELS != len(set(dummy_data['label'])):
             print(f"Warning: NUM_LABELS ({NUM_LABELS}) in script does not match unique labels in dummy data ({len(set(dummy_data['label']))}). Adjust NUM_LABELS.")
        else:
            df_dummy = pd.DataFrame(dummy_data)
            df_dummy.to_csv(DATA_FILE_PATH, index=False)
            print(f"Dummy '{DATA_FILE_PATH}' created. Please replace it with your actual annotated data.")

    main()
