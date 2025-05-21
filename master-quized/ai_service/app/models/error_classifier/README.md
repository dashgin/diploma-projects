# Error Classifier Model

This directory will contain the trained model for classifying errors in student responses.

## Model Details

- Model Type: DistilBERT-based classifier
- Classes: Various error types (factual_inaccuracy, conceptual_misunderstanding, etc.)
- Format: PyTorch model saved with Hugging Face Transformers

## Usage

The model is loaded automatically by the AI Feedback Service during startup.

## Training

The actual trained model files should be placed in this directory. For development purposes, 
the service will fall back to a pre-trained DistilBERT if no custom model is found here. 