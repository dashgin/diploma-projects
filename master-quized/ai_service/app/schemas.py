from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    """
    Schema for the incoming request to generate AI feedback.
    """

    quiz_id: str = Field(..., description="Unique identifier for the quiz.")
    question_id: str = Field(
        ..., description="Unique identifier for the question within the quiz."
    )
    student_id: str = Field(..., description="Unique identifier for the student.")
    student_answer: str = Field(
        ..., description="The student's open-ended textual response."
    )
    question_text: str = Field(..., description="The full text of the question.")
    model_answer: str = Field(
        ...,
        description="The ideal/model answer for comparison, provided by the educator.",
    )
    key_concepts: list[str] = Field(
        ..., description="List of key concepts expected in the answer."
    )
    context_info: dict[str, str] | None = Field(
        None,
        description="Additional contextual information for the AI, e.g., topic, difficulty.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "quiz_id": "quiz-123",
                "question_id": "q-456",
                "student_id": "student-789",
                "student_answer": "The carbon cycle is the process where carbon is exchanged between the atmosphere, land, and oceans.",
                "question_text": "Explain the carbon cycle and its importance to the ecosystem.",
                "model_answer": "The carbon cycle is the biogeochemical cycle by which carbon is exchanged among the biosphere, pedosphere, geosphere, hydrosphere, and atmosphere of the Earth. It is crucial for maintaining climate balance and supporting life on Earth.",
                "key_concepts": [
                    "biogeochemical cycle",
                    "carbon exchange",
                    "climate regulation",
                    "ecosystem",
                ],
                "context_info": {
                    "topic": "Environmental Science",
                    "difficulty": "medium",
                },
            }
        }
    }


class RecommendedResource(BaseModel):
    """
    Schema for a recommended learning resource.
    """

    title: str = Field(..., description="Title of the learning resource.")
    url: str = Field(..., description="URL to access the learning resource.")
    type: str = Field(
        ..., description="Type of resource (e.g., 'video', 'article', 'practice_set')."
    )


class FeedbackResponseData(BaseModel):
    """
    Schema for the detailed AI-generated feedback content.
    """

    feedback_text: str = Field(
        ..., description="The generated personalized feedback message."
    )
    error_identified: bool = Field(
        ..., description="True if any significant error was identified."
    )
    error_type: list[str] | None = Field(
        None,
        description="List of identified error types (e.g., 'factual_inaccuracy', 'conceptual_misunderstanding').",
    )
    confidence_score: float | None = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence score of the AI's analysis (0.0 to 1.0).",
    )
    concepts_covered: list[str] | None = Field(
        None,
        description="List of key concepts correctly identified/addressed by the student.",
    )
    concepts_missed: list[str] | None = Field(
        None,
        description="List of key concepts missed or partially addressed by the student.",
    )
    recommended_resources: list[RecommendedResource] | None = Field(
        None, description="List of recommended learning resources."
    )


class FeedbackResponse(BaseModel):
    """
    Overall schema for the AI feedback service's response.
    """

    status: str = Field(
        ..., description="Status of the request ('success' or 'error')."
    )
    message: str = Field(..., description="General status message.")
    feedback: FeedbackResponseData | None = Field(
        None, description="Detailed feedback data if successful."
    )
