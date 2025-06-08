"""
Main FastAPI application for the AI Feedback Service.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.modules import (
    feedback_generation,
    ml_analysis,
    preprocessing,
    recommendation_engine,
    rule_based_feedback,
)
from app.schemas import FeedbackRequest, FeedbackResponse, FeedbackResponseData

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Context manager for application startup and shutdown events.
    Used to load AI models once when the service starts.
    """
    logger.info("AI Feedback Service starting up...")
    try:
        ml_analysis.load_models()  # Load models at startup
        logger.info("AI Feedback Service startup complete.")
    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        logger.warning("Service will continue with limited functionality.")
    yield
    logger.info("AI Feedback Service shutting down.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Provides AI-powered feedback for open-ended quiz responses.",
    version="1.0.0",
    lifespan=lifespan,  # Register the lifespan context manager
    docs_url="/ai-api/docs",
    redoc_url="/ai-api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for the application."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )


@app.post(
    "/ai-api/feedback/generate",
    response_model=FeedbackResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_feedback(request: FeedbackRequest):
    """
    Receives a student's open-ended answer and question context,
    processes it through AI modules, and returns personalized feedback.

    The request body must conform to the FeedbackRequest schema.
    The response body will conform to the FeedbackResponse schema.
    """
    try:
        logger.info(
            f"Received feedback request for student {request.student_id}, question {request.question_id}"
        )
        logger.debug(f"Request details: {request.model_dump()}")

        # 1. Preprocessing
        preprocessed_answer = preprocessing.preprocess_text(request.student_answer)
        logger.debug(f"Preprocessed student answer: '{preprocessed_answer}'")
        # Preprocess model answer for consistent comparison
        preprocessed_model_answer = preprocessing.preprocess_text(request.model_answer)
        logger.debug(f"Preprocessed model answer: '{preprocessed_model_answer}'")

        # 2. Rule-Based Check
        rule_feedback_analysis = rule_based_feedback.apply_rules(
            preprocessed_answer,
            request.question_text,
            preprocessed_model_answer,
            request.key_concepts,
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
                    confidence_score=rule_feedback_analysis.get(
                        "confidence_score", 1.0
                    ),
                    concepts_covered=rule_feedback_analysis.get("concepts_covered"),
                    concepts_missed=rule_feedback_analysis.get("concepts_missed"),
                    recommended_resources=rule_feedback_analysis.get(
                        "recommended_resources"
                    ),
                ),
            )

        # 3. Deep AI Analysis (NLP/ML)
        ml_analysis_results = ml_analysis.analyze_response(
            preprocessed_answer,
            preprocessed_model_answer,
            request.key_concepts,
            request.context_info,
        )
        logger.debug(f"ML analysis results: {ml_analysis_results}")

        # 4. Skill Gap Identification
        skill_gaps = ml_analysis.identify_skill_gaps(
            ml_analysis_results, request.key_concepts
        )
        logger.debug(f"Identified skill gaps: {skill_gaps}")

        # 5. Resource Recommendation
        recommended_resources = recommendation_engine.get_recommendations(
            skill_gaps,
            request.context_info.get("topic") if request.context_info else None,
        )
        logger.debug(f"Recommended resources: {recommended_resources}")

        # 6. Feedback Construction
        final_feedback_data = feedback_generation.construct_feedback(
            rule_feedback_analysis,
            ml_analysis_results,
            skill_gaps,
            recommended_resources,
        )
        logger.debug(f"Final feedback data: {final_feedback_data}")

        return FeedbackResponse(
            status="success",
            message="AI-powered feedback generated.",
            feedback=final_feedback_data,
        )

    except RuntimeError as re:  # Specific for model loading issues
        logger.error(f"AI Model Error: {re}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI models are not loaded or accessible. Please check service status. Error: {re}",
        )
    except Exception as e:
        logger.error(f"Unhandled error during feedback generation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal server error occurred during AI processing: {e}",
        )


@app.get("/ai-api/health", response_model=dict[str, str])
async def health_check():
    """
    Checks the health of the AI Feedback Service.
    Indicates if AI models are loaded.
    """
    status_msg = "ok"
    if not ml_analysis.models_loaded():
        status_msg = "degraded (AI models not loaded)"
    return {"status": status_msg}
