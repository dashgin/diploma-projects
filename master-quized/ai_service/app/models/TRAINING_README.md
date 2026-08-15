# Error Classifier Model Training

This document explains how to train and evaluate custom error classifier models for the QuizEd AI Feedback Service.

## Overview

The training system uses a fine-tuned BERT-based model to classify student answers into 5 pedagogical error categories:

1. **no_error** - The answer is correct and complete
2. **factual_inaccuracy** - The answer contains incorrect factual information
3. **conceptual_misunderstanding** - The answer shows fundamental misunderstanding of concepts
4. **incomplete_explanation** - The answer is partially correct but missing key information
5. **irrelevant_content** - The answer is off-topic or irrelevant to the question

## Training Data

The system uses the [SciEntsBank dataset](https://huggingface.co/datasets/nkazi/SciEntsBank) which contains:
- **Training set**: 4,969 examples
- **Test UA (Unseen Answers)**: 540 examples
- **Test UQ (Unseen Questions)**: 733 examples  
- **Test UD (Unseen Domains)**: 4,562 examples

## Quick Start

### 1. Train a New Model

```bash
# Basic training with default settings
python scripts/train_model.py

# Train with custom output directory
python scripts/train_model.py --output-dir ./my_model

# Train with specific parameters
python scripts/train_model.py --epochs 5 --batch-size 32 --learning-rate 1e-5

# Train with configuration file
python scripts/train_model.py --config training_config.json
```

### 2. Evaluate a Trained Model

```bash
# Evaluate on unseen questions (default)
python scripts/evaluate_model.py --model-path ./my_model

# Evaluate on different splits
python scripts/evaluate_model.py --model-path ./my_model --split test_ua
python scripts/evaluate_model.py --model-path ./my_model --split test_ud

# Get detailed results
python scripts/evaluate_model.py --model-path ./my_model --verbose

# Save results to file
python scripts/evaluate_model.py --model-path ./my_model --output results.json
```

## Configuration

### Training Configuration File

Create a JSON configuration file (see `training_config.json` for example):

```json
{
  "model_checkpoint": "bert-base-multilingual-uncased",
  "batch_size": 16,
  "learning_rate": 2e-5,
  "num_epochs": 3,
  "max_length": 128,
  "weight_decay": 0.01
}
```

### Available Models

- `bert-base-multilingual-uncased` (default, recommended)
- `distilbert-base-uncased` (faster, slightly lower accuracy)
- `bert-base-uncased` (English only)

### Environment Variables

Set these in your `.env` file:

```env
# Model paths
ERROR_CLASSIFIER_MODEL_PATH=app/models/error_classifier
TRAINING_OUTPUT_DIR=app/models/error_classifier
TRAINING_CONFIG_PATH=training_config.json

# Model settings
SEMANTIC_MODEL_NAME=all-MiniLM-L6-v2
FALLBACK_MODEL_NAME=distilbert-base-uncased
SIMILARITY_THRESHOLD=0.5
```

## Training Process

### 1. Data Loading and Preprocessing
- Downloads the SciEntsBank dataset from HuggingFace
- Maps original labels to the custom pedagogical schema
- Tokenizes student answers using the selected model's tokenizer

### 2. Model Architecture
- Uses a pre-trained BERT model as the base
- Adds a classification head for 5-class prediction
- Configures label mappings for interpretable outputs

### 3. Training Strategy
- **Optimizer**: AdamW with weight decay
- **Learning Rate**: 2e-5 (adjustable)
- **Batch Size**: 16 (adjustable)
- **Epochs**: 3 (adjustable)
- **Evaluation**: After each epoch on validation split
- **Best Model**: Selected based on macro F1 score

### 4. Evaluation
- Tests on three different splits for comprehensive evaluation
- Generates detailed classification reports
- Provides per-class precision, recall, and F1 scores

## Expected Performance

Based on the training notebook results:

| Split | F1 Score | Precision | Recall |
|-------|----------|-----------|---------|
| Unseen Answers (test_ua) | 0.49 | 0.63 | 0.44 |
| Unseen Questions (test_uq) | 0.26 | 0.27 | 0.26 |
| Unseen Domains (test_ud) | 0.38 | 0.47 | 0.35 |

## Integration with AI Service

### 1. Model Loading
The trained model is automatically loaded by the AI service at startup:

```python
# In ml_analysis.py
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
```

### 2. Inference
The model classifies student answers and returns error types:

```python
# Example usage
errors, confidence = classify_errors(student_answer)
```

### 3. Error Labels
The service uses the updated error classification schema:

```python
ERROR_LABELS = {
    0: "no_error",
    1: "factual_inaccuracy", 
    2: "conceptual_misunderstanding",
    3: "incomplete_explanation",
    4: "irrelevant_content",
}
```

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   - Reduce batch size: `--batch-size 8`
   - Use CPU: `--no-gpu`

2. **Dataset Download Issues**
   - Check internet connection
   - Verify HuggingFace Hub access
   - Try running with `--verbose` for more details

3. **Model Loading Errors**
   - Ensure the model directory contains all required files
   - Check that the path is correct
   - Verify disk space availability

### Performance Optimization

1. **GPU Training**
   - Use CUDA-compatible GPU for faster training
   - Monitor GPU memory usage
   - Consider mixed precision training for larger models

2. **Hyperparameter Tuning**
   - Experiment with learning rates (1e-5 to 5e-5)
   - Try different batch sizes (8, 16, 32)
   - Adjust number of epochs based on validation performance

3. **Model Selection**
   - Use `bert-base-multilingual-uncased` for best multilingual support
   - Try `distilbert-base-uncased` for faster inference
   - Consider domain-specific models if available

## Advanced Usage

### Custom Training Loop

For more control over the training process, you can use the training module directly:

```python
from app.modules.model_training import train_error_classifier

# Custom configuration
config = {
    "model_checkpoint": "bert-base-multilingual-uncased",
    "batch_size": 32,
    "learning_rate": 1e-5,
    "num_epochs": 5,
    "max_length": 256,
    "weight_decay": 0.01,
}

# Train model
model_path = train_error_classifier(
    output_dir="./custom_model",
    config=config,
    use_gpu=True
)
```

### Batch Evaluation

For evaluating multiple models or configurations:

```python
from app.modules.model_training import evaluate_model

models = ["model1", "model2", "model3"]
splits = ["test_ua", "test_uq", "test_ud"]

for model_path in models:
    for split in splits:
        results = evaluate_model(model_path, split)
        print(f"{model_path} on {split}: F1={results['metrics']['eval_f1_macro']:.4f}")
```

## Contributing

When contributing to the training system:

1. Test your changes on a small dataset first
2. Ensure backward compatibility with existing models
3. Update documentation for any new features
4. Run the full evaluation suite before submitting

## References

- [Original Fine-Tuning Notebook](ai_service/app/models/Fine_Tuning_for_Error_Classifier.ipynb)
- [SciEntsBank Dataset](https://huggingface.co/datasets/nkazi/SciEntsBank)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)
- [BERT Paper](https://arxiv.org/abs/1810.04805) 