# Error Classifier Model

This directory contains code for training and using the error classifier model that analyzes student responses.

## Model Details

- **Model Type**: DistilBERT-based classifier
- **Classes**: Various error types
  - `no_error`: No error detected, answer is correct
  - `factual_inaccuracy`: Contains factually incorrect information
  - `conceptual_misunderstanding`: Shows misunderstanding of core concepts
  - `incomplete_explanation`: Missing important details or explanations
  - `logical_fallacy`: Contains logical errors or inconsistencies
  - `irrelevant_content`: Content not related to the question

## Training the Model

### Prerequisites

Ensure you have the required dependencies:
```bash
pip install torch transformers datasets scikit-learn pandas
```

### Training Data

The model requires training data in CSV format with two columns:
- `text`: The student's answer (or text to classify)
- `label`: Numerical label corresponding to error type (0-5)

Place your training data in the `training_data` directory or specify a custom path.

### Running the Training

From the project root, run:
```bash
python -m app.models.train_models --model error_classifier
```

Training options:
- `--data_file`: Path to training data CSV
- `--model_name`: Pre-trained model to fine-tune (default: distilbert-base-uncased)
- `--output_dir`: Directory to save the trained model
- `--epochs`: Number of training epochs (default: 3)
- `--train_batch_size`: Training batch size (default: 8)
- `--learning_rate`: Learning rate (default: 5e-5)
- `--create_dummy_data`: Create dummy data for demonstration purposes

### Example

```bash
# Train with custom data and parameters
python -m app.models.train_models --model error_classifier --data_file data/my_training_data.csv --epochs 5 --learning_rate 3e-5

# Use demo data for testing
python -m app.models.train_models --model error_classifier --create_dummy_data
```

## Using the Trained Model

After training, the model will be saved to the specified output directory. The AI Feedback Service automatically loads this model during startup.

For development purposes, the service will fall back to a pre-trained DistilBERT model if no custom model is found.

## Model Evaluation

During training, the following metrics are calculated:
- Accuracy
- Precision, Recall, and F1-score (macro-averaged)
- Per-class metrics
- Confusion matrix

These metrics are logged and can be used to evaluate the model's performance. 