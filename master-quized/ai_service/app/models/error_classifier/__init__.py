"""
Error classifier module for the AI Feedback Service.
Provides model training and inference for error classification in student responses.
"""

from .inference import ERROR_LABELS, classify_error, load_model
from .semantic_similarity import get_semantic_similarity
