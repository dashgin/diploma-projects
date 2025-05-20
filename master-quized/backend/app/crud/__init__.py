from app.crud.area import get_areas
from app.crud.assignment import (
    create_assignment,
    get_assignment,
    get_assignments,
    get_user_assignments,
)
from app.crud.attempt import (
    complete_attempt,
    create_attempt,
    get_attempt,
    get_attempts,
    get_user_attempts,
)
from app.crud.feedback import create_feedback, get_feedback, get_feedback_by_response
from app.crud.item import create_item
from app.crud.option import (
    create_option,
    delete_option,
    get_option,
    get_options_by_question,
    update_option,
)
from app.crud.question import (
    create_question,
    delete_question,
    get_question,
    get_questions_by_quiz,
    update_question,
)

# New imports for our API endpoints
from app.crud.quiz import (
    create_quiz,
    delete_quiz,
    get_quiz,
    get_quizzes,
    get_user_quizzes,
    update_quiz,
)
from app.crud.recommendation import (
    create_recommendation,
    get_recommendation,
    get_recommendations_by_feedback,
)
from app.crud.response import create_response, get_response, get_responses_by_attempt
from app.crud.user import authenticate, create_user, get_user_by_email, update_user

__all__ = [
    # User operations
    "create_user",
    "update_user",
    "get_user_by_email",
    "authenticate",
    # Item operations
    "create_item",
    # Quiz operations
    "create_quiz",
    "get_quiz",
    "update_quiz",
    "delete_quiz",
    "get_quizzes",
    "get_user_quizzes",
    # Question operations
    "create_question",
    "get_question",
    "update_question",
    "delete_question",
    "get_questions_by_quiz",
    # Option operations
    "create_option",
    "get_option",
    "update_option",
    "delete_option",
    "get_options_by_question",
    # Area operations
    "get_areas",
    # Assignment operations
    "create_assignment",
    "get_assignment",
    "get_assignments",
    "get_user_assignments",
    # Attempt operations
    "create_attempt",
    "get_attempt",
    "complete_attempt",
    "get_attempts",
    "get_user_attempts",
    # Response operations
    "create_response",
    "get_response",
    "get_responses_by_attempt",
    # Feedback operations
    "create_feedback",
    "get_feedback",
    "get_feedback_by_response",
    # Recommendation operations
    "create_recommendation",
    "get_recommendation",
    "get_recommendations_by_feedback",
]
