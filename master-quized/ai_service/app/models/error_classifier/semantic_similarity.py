"""
Semantic similarity analysis module for comparing text responses.
Uses pre-trained Sentence-Transformer models for generating embeddings and calculating similarity.
"""

from sentence_transformers import SentenceTransformer, util
import logging
from functools import lru_cache

# Configure logger
logger = logging.getLogger(__name__)

# Recommended model for semantic similarity as described in the thesis
SEMANTIC_SIMILARITY_MODEL_NAME = 'all-MiniLM-L6-v2'


@lru_cache(maxsize=128)
def get_semantic_similarity(text1: str, text2: str, model_name: str = SEMANTIC_SIMILARITY_MODEL_NAME) -> float:
    """
    Computes the semantic similarity between two texts using a pre-trained
    Sentence-Transformer model. Results are cached for better performance.

    Args:
        text1: The first text string (e.g., student's answer).
        text2: The second text string (e.g., model answer).
        model_name: The name of the SentenceTransformer model to use.

    Returns:
        A float representing the cosine similarity score (between 0 and 1 for positive similarity).
        Returns 0.0 if an error occurs.
    """
    try:
        # Load the pre-trained model.
        # This will download the model if it's not already cached locally.
        model = SentenceTransformer(model_name)
    except Exception as e:
        logger.error(f"Error loading SentenceTransformer model '{model_name}': {e}")
        return 0.0

    # Generate embeddings for both texts
    try:
        logger.debug(f"Generating embedding for text1: '{text1[:50]}...'")
        embedding1 = model.encode(text1, convert_to_tensor=True)
        logger.debug(f"Generating embedding for text2: '{text2[:50]}...'")
        embedding2 = model.encode(text2, convert_to_tensor=True)
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        return 0.0

    # Compute cosine similarity between the embeddings
    try:
        cosine_score = util.pytorch_cos_sim(embedding1, embedding2)
        # .item() extracts the Python number from a single-element PyTorch tensor
        similarity_value = float(cosine_score.item())
        logger.debug(f"Semantic similarity score: {similarity_value:.4f}")
        return similarity_value
    except Exception as e:
        logger.error(f"Error computing cosine similarity: {e}")
        return 0.0


if __name__ == "__main__":
    # Configure logging for standalone testing
    logging.basicConfig(level=logging.INFO, 
                      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    print("--- Semantic Similarity Test ---")

    student_answer_example = "Mitochondria are the powerhouses of the cell, responsible for generating most of the cell's supply of ATP through cellular respiration."
    model_answer_example = "The primary function of mitochondria is to generate the majority of the cell's supply of adenosine triphosphate (ATP), used as a source of chemical energy via cellular respiration."
    
    similarity_score = get_semantic_similarity(student_answer_example, model_answer_example)
    print(f"\nStudent Answer: '{student_answer_example}'")
    print(f"Model Answer:   '{model_answer_example}'")
    print(f"Semantic Similarity Score: {similarity_score:.4f}")

    # Different topic example
    student_answer_different = "The nucleus controls the cell's activities and contains the genetic material."
    similarity_score_different = get_semantic_similarity(student_answer_different, model_answer_example)
    print(f"\nDifferent Topic Score: {similarity_score_different:.4f}") 