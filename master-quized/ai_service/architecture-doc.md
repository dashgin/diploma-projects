## AI Feedback Service Architecture Overview (Precise Technical Detail - v2 with Model Answers)

This document provides a highly precise and concrete technical architectural design for the AI Feedback Service. It is intended to serve as a direct guide for implementation within an AI-assisted development environment, detailing component interactions, data structures, and specific technical considerations. The service operates as a standalone, HTTP-based microservice, ensuring modularity, scalability, and clear separation of concerns from the main application backend.

### 1. Architectural Philosophy

The AI Feedback Service strictly adheres to a microservice architecture paradigm. This design choice facilitates independent development, deployment, and scaling of the AI capabilities, preventing computationally intensive AI processing from bottlenecking the main application's performance. All communication with the main application backend will be exclusively via a well-defined RESTful API, utilizing standard HTTP methods and JSON payloads.

### 2. Core Components & Technical Implementation Details

The AI Feedback Service will be structured into logical Python modules, each encapsulating specific functionalities.

#### 2.1. FastAPI AI Service (API Layer)

-   **Purpose:** Serves as the primary external interface for the AI Feedback Service. It handles HTTP request parsing, input validation, orchestration of calls to internal AI modules, and formatting of the final feedback response.
    
-   **Technology:**  `FastAPI` (Python 3.9+), `Pydantic` (for data validation and serialization), `Uvicorn` (ASGI server).
    
-   **Key Files:**  `main.py`, `schemas.py`
    
-   **Implementation Details:**
    
    -   **`schemas.py` (Pydantic Models):**
        
        ```
        from pydantic import BaseModel, Field
        from typing import List, Dict, Optional
        
        class FeedbackRequest(BaseModel):
            """
            Schema for the incoming request to generate AI feedback.
            """
            quiz_id: str = Field(..., description="Unique identifier for the quiz.")
            question_id: str = Field(..., description="Unique identifier for the question within the quiz.")
            student_id: str = Field(..., description="Unique identifier for the student.")
            student_answer: str = Field(..., description="The student's open-ended textual response.")
            question_text: str = Field(..., description="The full text of the question.")
            # --- Emphasizing Model Answer as a key input ---
            model_answer: str = Field(..., description="The ideal/model answer for comparison, provided by the educator.")
            # --- End emphasis ---
            key_concepts: List[str] = Field(..., description="List of key concepts expected in the answer.")
            context_info: Optional[Dict[str, str]] = Field(
                None, description="Additional contextual information for the AI, e.g., topic, difficulty."
            )
        
        class RecommendedResource(BaseModel):
            """
            Schema for a recommended learning resource.
            """
            title: str = Field(..., description="Title of the learning resource.")
            url: str = Field(..., description="URL to access the learning resource.")
            type: str = Field(..., description="Type of resource (e.g., 'video', 'article', 'practice_set').")
        
        class FeedbackResponseData(BaseModel):
            """
            Schema for the detailed AI-generated feedback content.
            """
            feedback_text: str = Field(..., description="The generated personalized feedback message.")
            error_identified: bool = Field(..., description="True if any significant error was identified.")
            error_type: Optional[List[str]] = Field(
                None, description="List of identified error types (e.g., 'factual_inaccuracy', 'conceptual_misunderstanding')."
            )
            confidence_score: Optional[float] = Field(
                None, ge=0.0, le=1.0, description="Confidence score of the AI's analysis (0.0 to 1.0)."
            )
            concepts_covered: Optional[List[str]] = Field(
                None, description="List of key concepts correctly identified/addressed by the student."
            )
            concepts_missed: Optional[List[str]] = Field(
                None, description="List of key concepts missed or partially addressed by the student."
            )
            recommended_resources: Optional[List[RecommendedResource]] = Field(
                None, description="List of recommended learning resources."
            )
        
        class FeedbackResponse(BaseModel):
            """
            Overall schema for the AI feedback service's response.
            """
            status: str = Field(..., description="Status of the request ('success' or 'error').")
            message: str = Field(..., description="General status message.")
            feedback: Optional[FeedbackResponseData] = Field(None, description="Detailed feedback data if successful.")
        
        ```
        
    -   **`main.py` (FastAPI Application):**
        
        ```
        from fastapi import FastAPI, HTTPException, status
        from schemas import FeedbackRequest, FeedbackResponse, FeedbackResponseData
        from modules import preprocessing, rule_based_feedback, ml_analysis, feedback_generation, recommendation_engine
        import logging
        from contextlib import asynccontextmanager
        from typing import Dict # Added for health_check type hint
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            """
            Context manager for application startup and shutdown events.
            Used to load AI models once when the service starts.
            """
            logger.info("AI Feedback Service starting up...")
            ml_analysis.load_models() # Load models at startup
            logger.info("AI Feedback Service startup complete.")
            yield
            logger.info("AI Feedback Service shutting down.")
        
        app = FastAPI(
            title="AI Feedback Service",
            description="Provides AI-powered feedback for open-ended quiz responses.",
            version="1.0.0",
            lifespan=lifespan # Register the lifespan context manager
        )
        
        @app.post("/feedback/generate", response_model=FeedbackResponse, status_code=status.HTTP_200_OK)
        async def generate_feedback(request: FeedbackRequest):
            """
            Receives a student's open-ended answer and question context,
            processes it through AI modules, and returns personalized feedback.
        
            The request body must conform to the FeedbackRequest schema.
            The response body will conform to the FeedbackResponse schema.
            """
            try:
                logger.info(f"Received feedback request for student {request.student_id}, question {request.question_id}")
                logger.debug(f"Request details: {request.dict()}")
        
                # 1. Preprocessing
                preprocessed_answer = preprocessing.preprocess_text(request.student_answer)
                logger.debug(f"Preprocessed student answer: '{preprocessed_answer}'")
                # --- Preprocess model answer for consistent comparison ---
                preprocessed_model_answer = preprocessing.preprocess_text(request.model_answer)
                logger.debug(f"Preprocessed model answer: '{preprocessed_model_answer}'")
        
        
                # 2. Rule-Based Check
                # This module can return immediate feedback or initial analysis for ML
                rule_feedback_analysis = rule_based_feedback.apply_rules(
                    preprocessed_answer, request.question_text, preprocessed_model_answer, request.key_concepts
                )
                if rule_feedback_analysis.get("immediate_feedback"):
                    logger.info("Rule-based immediate feedback triggered.")
                    return FeedbackResponse(
                        status="success",
                        message="Rule-based feedback generated.",
                        feedback=FeedbackResponseData(
                            feedback_text=rule_feedback_analysis["feedback_text"],
                            error_identified=rule_feedback_analysis["error_identified"],
                            error_type=rule_feedback_analysis.get("error_type"),
                            confidence_score=rule_feedback_analysis.get("confidence_score", 1.0), # High confidence for rule-based
                            concepts_covered=rule_feedback_analysis.get("concepts_covered"),
                            concepts_missed=rule_feedback_analysis.get("concepts_missed"),
                            recommended_resources=rule_feedback_analysis.get("recommended_resources")
                        )
                    )
        
                # 3. Deep AI Analysis (NLP/ML)
                # Pass context_info directly to ml_analysis for potential use (e.g., difficulty)
                ml_analysis_results = ml_analysis.analyze_response(
                    preprocessed_answer, preprocessed_model_answer, request.key_concepts, request.context_info
                )
                logger.debug(f"ML analysis results: {ml_analysis_results}")
        
                # 4. Skill Gap Identification
                skill_gaps = ml_analysis.identify_skill_gaps(ml_analysis_results, request.key_concepts)
                logger.debug(f"Identified skill gaps: {skill_gaps}")
        
                # 5. Resource Recommendation (Placeholder: In a real system, this would query a DB)
                recommended_resources = recommendation_engine.get_recommendations(
                    skill_gaps, request.context_info.get("topic") if request.context_info else None
                )
                logger.debug(f"Recommended resources: {[res.dict() for res in recommended_resources]}")
        
                # 6. Feedback Construction
                final_feedback_data = feedback_generation.construct_feedback(
                    rule_feedback_analysis, ml_analysis_results, skill_gaps, recommended_resources
                )
                logger.debug(f"Final feedback data: {final_feedback_data.dict()}")
        
                return FeedbackResponse(
                    status="success",
                    message="AI-powered feedback generated.",
                    feedback=final_feedback_data
                )
        
            except RuntimeError as re: # Specific for model loading issues
                logger.error(f"AI Model Error: {re}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE, # Service unavailable if models not loaded
                    detail=f"AI models are not loaded or accessible. Please check service status. Error: {re}"
                )
            except Exception as e:
                logger.error(f"Unhandled error during feedback generation: {e}", exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"An internal server error occurred during AI processing: {e}"
                )
        
        # Health check endpoint
        @app.get("/health", response_model=Dict[str, str])
        async def health_check():
            """
            Checks the health of the AI Feedback Service.
            Indicates if AI models are loaded.
            """
            status_msg = "ok"
            if not ml_analysis.semantic_similarity_model or not ml_analysis.error_classifier_model:
                status_msg = "degraded (AI models not loaded)"
            return {"status": status_msg}
        
        ```
        

#### 2.2. Input Preprocessing Module

-   **Purpose:** Standardize and clean raw student textual responses and **model answers** for consistent input to downstream AI models.
    
-   **Technology:**  `nltk` (for tokenization, stemming/lemmatization, stopwords), `re` (regular expressions).
    
-   **Key File:**  `modules/preprocessing.py`
    
-   **Implementation Details:** (No code change in `preprocessing.py` itself, as `preprocess_text` is generic, but its application in `main.py` is updated).
    

#### 2.3. Rule-Based Feedback Module

-   **Purpose:** Implement initial, deterministic checks for common, predictable errors or patterns in student responses, often by comparing them against the `model_answer` or `key_concepts`. This provides immediate, high-confidence feedback for clear-cut cases.
    
-   **Technology:** Python. Rules can be defined directly in code for a prototype or loaded from a configuration file/database in a production environment.
    
-   **Key File:**  `modules/rule_based_feedback.py`
    
-   **Implementation Details:**
    
    ```
    from typing import Dict, List, Any
    import logging
    
    logger = logging.getLogger(__name__)
    
    def apply_rules(student_answer_preprocessed: str, question_text: str, model_answer_preprocessed: str, key_concepts: List[str]) -> Dict[str, Any]:
        """
        Applies a set of predefined rules to the student's preprocessed answer.
        Returns a dictionary containing feedback information, including whether
        immediate feedback should be generated or if further ML analysis is needed.
    
        Args:
            student_answer_preprocessed (str): The preprocessed student's answer.
            question_text (str): The original question text.
            model_answer_preprocessed (str): The preprocessed ideal/model answer. # Updated
            key_concepts (List[str]): List of expected key concepts.
    
        Returns:
            Dict[str, Any]: A dictionary with feedback details.
                - "immediate_feedback" (bool): True if a rule triggered immediate feedback.
                - "feedback_text" (str): The generated feedback message.
                - "error_identified" (bool): True if an error was found.
                - "error_type" (List[str]): List of error types identified by rules.
                - "confidence_score" (float): Confidence (usually 1.0 for rule-based).
                - "concepts_covered" (List[str]): Concepts covered by rules.
                - "concepts_missed" (List[str]): Concepts missed by rules.
        """
        feedback_info = {
            "immediate_feedback": False,
            "feedback_text": "",
            "error_identified": False,
            "error_type": [],
            "confidence_score": 1.0, # Rule-based feedback is typically high confidence
            "concepts_covered": [],
            "concepts_missed": []
        }
    
        # Rule 1: Answer is too short
        if len(student_answer_preprocessed.split()) < 5:
            feedback_info["immediate_feedback"] = True
            feedback_info["feedback_text"] = "Your answer is very brief. Please elaborate more on your thoughts to fully address the question."
            feedback_info["error_identified"] = True
            feedback_info["error_type"].append("too_short")
            logger.info("Rule: 'too_short' triggered.")
            return feedback_info # Return immediately for critical, simple errors
    
        # Rule 2: Answer is identical to the question (or very similar, indicating no real answer)
        if len(student_answer_preprocessed) > 0 and len(question_text) > 0:
            # Simple check, can be enhanced with semantic similarity if needed
            if student_answer_preprocessed.strip() == question_text.lower().strip():
                feedback_info["immediate_feedback"] = True
                feedback_info["feedback_text"] = "Your answer appears to be the same as the question. Please provide your own response."
                feedback_info["error_identified"] = True
                feedback_info["error_type"].append("echo_question")
                logger.info("Rule: 'echo_question' triggered.")
                return feedback_info
    
        # --- Rule 3: Direct Match to Model Answer (or very close) ---
        if student_answer_preprocessed == model_answer_preprocessed and len(model_answer_preprocessed) > 5:
             feedback_info["immediate_feedback"] = True
             feedback_info["feedback_text"] = "Excellent! Your answer is spot on and covers all the key points."
             feedback_info["error_identified"] = False # No error identified
             feedback_info["concepts_covered"] = key_concepts # Assume all concepts covered if direct match
             logger.info("Rule: 'direct_model_match' triggered.")
             return feedback_info
    
    
        # Rule 4: Missing critical keywords (simple check, can be expanded with more sophisticated NLP)
        identified_concepts_by_rule = []
        missed_concepts_by_rule = []
        for kc in key_concepts:
            # Check for concept presence in student's preprocessed answer
            if kc.lower() in student_answer_preprocessed or preprocessing.preprocess_text(kc).lower() in student_answer_preprocessed:
                identified_concepts_by_rule.append(kc)
            else:
                missed_concepts_by_rule.append(kc)
    
        feedback_info["concepts_covered"] = identified_concepts_by_rule
        feedback_info["concepts_missed"] = missed_concepts_by_rule
    
        if missed_concepts_by_rule and len(key_concepts) > 0 and len(identified_concepts_by_rule) == 0:
            # If student missed ALL key concepts and there are key concepts
            feedback_info["feedback_text"] += f" Your answer doesn't seem to cover the main points. Consider focusing on: {', '.join(missed_concepts_by_rule)}."
            feedback_info["error_identified"] = True
            feedback_info["error_type"].append("all_key_concepts_missing")
            feedback_info["immediate_feedback"] = True # Can be immediate or combined with ML
            logger.info("Rule: 'all_key_concepts_missing' triggered.")
            return feedback_info
    
        # Add more rules as needed (e.g., for specific factual errors, common misspellings of scientific terms)
        # These rules would typically be loaded from a configuration or database for easy management.
    
        logger.debug("No immediate rule-based feedback triggered. Proceeding to ML analysis.")
        return feedback_info # If no immediate feedback, pass initial analysis for ML
    
    ```
    

#### 2.4. NLP/ML Analysis Models (Core AI)

-   **Purpose:** Perform deep semantic understanding, error classification, and concept identification using trained machine learning models. This module is responsible for nuanced analysis beyond simple rules, critically leveraging the `model_answer` as a reference.
    
-   **Technology:**  `transformers` (Hugging Face for pre-trained models and fine-tuning), `torch` (PyTorch for model inference), `sentence-transformers` (for efficient semantic similarity).
    
-   **Key File:**  `modules/ml_analysis.py`, `models/` directory for saved model weights and configurations.
    
-   **Implementation Details:**
    
    ```
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from sentence_transformers import SentenceTransformer, util
    import torch
    from typing import Dict, List, Any, Optional
    import logging
    # Import preprocessing for internal use if needed, but main.py handles it
    # from . import preprocessing # Uncomment if needed for additional internal preprocessing
    
    logger = logging.getLogger(__name__)
    
    # Global variables to hold loaded models
    semantic_similarity_model: Optional[SentenceTransformer] = None
    error_classifier_tokenizer: Optional[AutoTokenizer] = None
    error_classifier_model: Optional[AutoModelForSequenceClassification] = None
    
    def load_models():
        """
        Loads all necessary NLP/ML models into memory.
        This function should be called once at service startup (e.g., via FastAPI's lifespan event).
        Paths should point to your fine-tuned and saved models.
        """
        global semantic_similarity_model, error_classifier_tokenizer, error_classifier_model
        try:
            logger.info("Loading AI models...")
            # Load SentenceTransformer for semantic similarity
            # Use a specific version or a fine-tuned local path for production
            semantic_similarity_model = SentenceTransformer('all-MiniLM-L6-v2') 
            logger.info("Semantic similarity model loaded.")
    
            # Load fine-tuned error classifier model and tokenizer
            # Ensure these paths are correct and models are saved after training
            error_classifier_path = "./models/error_classifier" # Example path
            error_classifier_tokenizer = AutoTokenizer.from_pretrained(error_classifier_path)
            error_classifier_model = AutoModelForSequenceClassification.from_pretrained(error_classifier_path)
            error_classifier_model.eval() # Set model to evaluation mode
            logger.info("Error classifier model and tokenizer loaded.")
    
            logger.info("All AI models loaded successfully.")
        except Exception as e:
            logger.critical(f"CRITICAL ERROR: Failed to load AI models. Service will be degraded. Error: {e}", exc_info=True)
            semantic_similarity_model = None
            error_classifier_tokenizer = None
            error_classifier_model = None
    
    def analyze_response(
        student_answer_preprocessed: str,
        model_answer_preprocessed: str, # Updated to accept preprocessed model answer
        key_concepts: List[str],
        context_info: Optional[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Performs deep NLP/ML analysis on the student's response.
    
        Args:
            student_answer_preprocessed (str): Preprocessed student's answer.
            model_answer_preprocessed (str): The preprocessed ideal/model answer. # Updated
            key_concepts (List[str]): List of expected key concepts.
            context_info (Optional[Dict[str, str]]): Additional context (e.g., {"difficulty": "hard"}).
    
        Returns:
            Dict[str, Any]: Analysis results including semantic similarity, identified errors,
                            identified concepts, and a confidence score.
        """
        if not semantic_similarity_model or not error_classifier_model:
            logger.error("Attempted to analyze response, but AI models are not loaded.")
            raise RuntimeError("AI models are not loaded. Cannot perform analysis.")
    
        results = {
            "semantic_similarity_score": 0.0,
            "identified_errors": [],
            "identified_concepts": [],
            "confidence_score": 0.0 # Initialize confidence score
        }
    
        # --- Semantic Similarity Calculation (comparing student answer to model answer) ---
        try:
            student_embedding = semantic_similarity_model.encode(student_answer_preprocessed, convert_to_tensor=True)
            model_embedding = semantic_similarity_model.encode(model_answer_preprocessed, convert_to_tensor=True) # Used preprocessed model answer
            cosine_similarity = util.cos_sim(student_embedding, model_embedding).item()
            results["semantic_similarity_score"] = cosine_similarity
            logger.debug(f"Semantic similarity to model answer: {cosine_similarity:.4f}")
        except Exception as e:
            logger.error(f"Error during semantic similarity calculation: {e}", exc_info=True)
    
        # --- Error Classification using Fine-tuned Transformer Model ---
        try:
            inputs = error_classifier_tokenizer(
                student_answer_preprocessed,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )
    
            with torch.no_grad():
                outputs = error_classifier_model(**inputs)
    
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            predicted_class_id = torch.argmax(probabilities, dim=1).item()
    
            confidence = probabilities[0, predicted_class_id].item()
            results["confidence_score"] = confidence
    
            error_label = error_classifier_model.config.id2label.get(predicted_class_id, "unknown_error")
    
            if error_label != "no_error":
                results["identified_errors"].append(error_label)
    
            logger.debug(f"Error classification: {error_label} (Confidence: {confidence:.4f})")
    
        except Exception as e:
            logger.error(f"Error during error classification: {e}", exc_info=True)
    
        # --- Concept Identification (can be enhanced with NER or more sophisticated methods) ---
        # This can compare against `key_concepts` provided or infer from semantic similarity.
        # For now, it remains as keyword matching against student_answer
        identified_concepts_ml = []
        for concept in key_concepts:
            # Check for concept presence in student's preprocessed answer
            # Use preprocessing.preprocess_text(concept) for consistency
            if preprocessing.preprocess_text(concept) in student_answer_preprocessed: # Assuming preprocessed_text converts to lower and handles stopwords, etc.
                identified_concepts_ml.append(concept)
        results["identified_concepts"] = identified_concepts_ml
        logger.debug(f"Identified concepts (ML): {identified_concepts_ml}")
    
        return results
    
    ```
    

#### 2.5. Feedback Generation Module

-   **Purpose:** Synthesize the analysis results from rule-based checks, ML models, and recommendations into a coherent, pedagogically sound, and actionable textual feedback message.
    
-   **Technology:** Python, string formatting, conditional logic.
    
-   **Key File:**  `modules/feedback_generation.py`
    
-   **Implementation Details:** (No code change in `feedback_generation.py` for this specific functionality, as it already consumes `ml_analysis_results` which contains `semantic_similarity_score` derived from `model_answer`).
    

#### 2.6. Recommendation Engine Module

-   **Purpose:** Provide targeted learning resource suggestions based on identified skill gaps and contextual information.
    
-   **Technology:** Python. For the prototype, a simple in-memory dictionary (`RECOMMENDATION_DB`) is used.
    
-   **Key File:**  `modules/recommendation_engine.py`
    
-   **Implementation Details:** (No code change needed here for this specific functionality).
    

### 3. Data Flow within the AI Feedback Service (Technical Flow - Refined for Model Answers)

1.  **Request Reception (`main.py`):**
    
    -   The `main.py` FastAPI application receives an HTTP `POST` request at `/feedback/generate`.
        
    -   The request body, a JSON payload, is validated against the `FeedbackRequest` Pydantic model. **Crucially, `request.model_answer` is received here.**
        
    -   Logging captures initial request details.
        
2.  **Preprocessing (`main.py` -> `modules.preprocessing`):**
    
    -   `request.student_answer` is passed to `preprocessing.preprocess_text()` to get `preprocessed_answer`.
        
    -   **NEW:**  `request.model_answer` is also passed to `preprocessing.preprocess_text()` to get `preprocessed_model_answer`. This ensures consistent cleaning before comparison.
        
3.  **Initial Rule-Based Check (`main.py` -> `modules.rule_based_feedback`):**
    
    -   `preprocessed_answer`, `question_text`, **`preprocessed_model_answer`**, and `key_concepts` are passed to `rule_based_feedback.apply_rules()`.
        
    -   The rule-based module can now include specific rules for direct comparison or near-match with the `model_answer` (e.g., to give "perfect score" feedback very quickly).
        
    -   If a critical rule triggers (`immediate_feedback` is `True`), `main.py` returns immediately.
        
4.  **Deep AI Analysis (`main.py` -> `modules.ml_analysis`):**
    
    -   If no immediate rule-based feedback, `preprocessed_answer`, **`preprocessed_model_answer`**, `key_concepts`, and `context_info` (including `difficulty`) are passed to `ml_analysis.analyze_response()`.
        
    -   **Core Functionality:** The `semantic_similarity_model` explicitly calculates the similarity between the student's response and the `preprocessed_model_answer`. This comparison forms a foundational part of assessing the student's understanding.
        
    -   The `error_classifier_model` and concept identification also work on the student's preprocessed answer, assessing errors relative to the expected content (implied by `model_answer` and `key_concepts`).
        
    -   Results (`semantic_similarity_score`, `identified_errors`, `identified_concepts`, `confidence_score`) are returned.
        
5.  **Skill Gap Identification (`main.py` -> `modules.ml_analysis`):**
    
    -   `ml_analysis.identify_skill_gaps()` uses the analysis results, which includes the semantic similarity to the model answer, to infer broader skill deficiencies.
        
6.  **Resource Recommendation (`main.py` -> `modules.recommendation_engine`):**
    
    -   (No direct change needed, as it consumes skill gaps which are derived from the overall analysis, including model answer comparison).
        
7.  **Feedback Construction (`main.py` -> `modules.feedback_generation`):**
    
    -   `feedback_generation.construct_feedback()` receives all analysis results. It leverages the `semantic_similarity_score` (derived from the model answer comparison) to craft appropriate feedback, noting when the student's answer is close or far from the ideal.
        
8.  **Response Transmission (`main.py`):**
    
    -   `main.py` returns the final `FeedbackResponse` as JSON.
        

### 4. Technology Stack Summary

(No changes needed here as the tools already support this functionality).

### 5. Project Directory Structure

(No changes needed here as the file structure already accommodates this).
