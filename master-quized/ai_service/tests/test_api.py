"""
Tests for the AI Feedback Service API.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ["ok", "degraded (AI models not loaded)"]


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Welcome" in data["message"]


def test_feedback_endpoint():
    """Test the feedback generation endpoint."""
    test_data = {
        "quiz_id": "test-quiz-123",
        "question_id": "test-question-456",
        "student_id": "test-student-789",
        "student_answer": "The carbon cycle involves carbon moving between atmosphere and plants.",
        "question_text": "Explain the carbon cycle.",
        "model_answer": "The carbon cycle is the biogeochemical process where carbon exchanges between atmosphere, oceans, soil and living organisms.",
        "key_concepts": ["biogeochemical", "carbon", "atmosphere"],
        "context_info": {"topic": "Science", "difficulty": "medium"},
    }

    response = client.post("/feedback/generate", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "feedback" in data
    assert data["feedback"]["feedback_text"] is not None
