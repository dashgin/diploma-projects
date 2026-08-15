# AI Feedback Service

This microservice provides AI-powered feedback on student quiz responses. It's designed to analyze open-ended text answers, compare them to model answers, and provide personalized, actionable feedback to help students improve.

## Features

- Analyze open-ended student responses using NLP and ML techniques
- Compare against model answers provided by educators
- Identify concepts covered and missed
- Classify error types in student responses
- Suggest personalized learning resources based on skill gaps
- Fast rule-based checks for immediate feedback on common issues
- Deep semantic understanding for nuanced analysis

## Architecture

The service is built as a microservice using FastAPI, with a modular structure:

- **API Layer**: Handles HTTP requests, input validation, and orchestration
- **Preprocessing Module**: Standardizes and cleans text for consistent analysis
- **Rule-Based Module**: Applies deterministic checks for quick feedback
- **ML Analysis Module**: Uses transformer models for deep semantic analysis
- **Feedback Generation**: Synthesizes analysis into coherent, personalized feedback
- **Recommendation Engine**: Suggests targeted learning resources based on skill gaps

## Setup and Usage

### Requirements

- Python 3.10+
- uv (for dependency management)
- Docker and Docker Compose (for containerized deployment)

### Development Setup

1. Clone the repository
2. Install uv if you don't have it:
   ```
   curl -sSf https://install.determinate.systems/uv | sh
   ```

3. Create a virtual environment and install dependencies:
   ```
   cd ai_service
   uv venv
   uv sync
   ```

4. Create a `.env` file (you can copy from `env-example`)

5. Run the service:
   ```
   uvicorn app.main:app --reload
   ```

### Running with Docker

```
cd ai_service
docker compose up -d
```

The service will be available at http://localhost:8000

### API Documentation

After starting the service, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example Request

```json
POST /feedback/generate

{
  "quiz_id": "quiz-123",
  "question_id": "q-456",
  "student_id": "student-789",
  "student_answer": "The carbon cycle is the process where carbon is exchanged between the atmosphere, land, and oceans.",
  "question_text": "Explain the carbon cycle and its importance to the ecosystem.",
  "model_answer": "The carbon cycle is the biogeochemical cycle by which carbon is exchanged among the biosphere, pedosphere, geosphere, hydrosphere, and atmosphere of the Earth. It is crucial for maintaining climate balance and supporting life on Earth.",
  "key_concepts": ["biogeochemical cycle", "carbon exchange", "climate regulation", "ecosystem"],
  "context_info": {"topic": "Environmental Science", "difficulty": "medium"}
}
```

## Environment Variables

- `ERROR_CLASSIFIER_MODEL_PATH`: Path to the error classifier model (default: "/app/app/models/error_classifier")
- `LOG_LEVEL`: Logging level (default: "INFO")

## Development

### Running Tests

```
cd ai_service
uv run pytest
``` 