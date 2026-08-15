"""
Text preprocessing module to standardize student answers and model answers
for consistent input to downstream AI models.
"""

import logging
import re
from functools import lru_cache

# Import nltk components if they will be used
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize

    # Download required nltk data if not already present
    try:
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        nltk.download("wordnet", quiet=True)

        STOPWORDS = set(stopwords.words("english"))
        lemmatizer = WordNetLemmatizer()
        NLTK_AVAILABLE = True
    except Exception:
        NLTK_AVAILABLE = False
        STOPWORDS = set()

except ImportError:
    NLTK_AVAILABLE = False
    STOPWORDS = set()

logger = logging.getLogger(__name__)


@lru_cache(maxsize=512)
def preprocess_text(
    text: str, remove_stopwords: bool = False, lemmatize: bool = False
) -> str:
    """
    Standardize and clean text for consistent input to downstream AI models.
    Results are cached for better performance.

    Args:
        text (str): The text to preprocess
        remove_stopwords (bool, optional): Whether to remove stopwords. Defaults to False.
        lemmatize (bool, optional): Whether to lemmatize words. Defaults to False.

    Returns:
        str: The preprocessed text
    """
    try:
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove special characters and extra whitespace
        text = re.sub(r"[^\w\s]", " ", text)  # Replace special chars with space
        text = re.sub(r"\s+", " ", text).strip()  # Remove extra whitespace

        # Only perform more advanced NLP if nltk is available and requested
        if NLTK_AVAILABLE:
            if remove_stopwords or lemmatize:
                try:
                    # Tokenize
                    tokens = word_tokenize(text)

                    # Remove stopwords if requested
                    if remove_stopwords:
                        tokens = [t for t in tokens if t not in STOPWORDS]

                    # Lemmatize if requested
                    if lemmatize:
                        tokens = [lemmatizer.lemmatize(t) for t in tokens]

                    # Rejoin the tokens
                    text = " ".join(tokens)
                except Exception as e:
                    logger.error(f"Error in NLTK processing: {e}", exc_info=True)
        elif remove_stopwords or lemmatize:
            logger.warning("NLTK functionality requested but NLTK is not available")

        return text
    except Exception as e:
        logger.error(f"Error preprocessing text: {e}", exc_info=True)
        # Return original text in case of error
        if text:
            return text.lower().strip()
        return ""
