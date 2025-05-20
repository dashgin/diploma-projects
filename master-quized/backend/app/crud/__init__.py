from app.crud.user import (
    create_user,
    get_user_by_email,
    authenticate,
    update_user,
)
from app.crud.item import create_item
# New imports for our API endpoints
from app.crud.quiz import (
    create_quiz,
    get_quiz,
    update_quiz,
    delete_quiz,
    get_quizzes,
    get_user_quizzes,
)
from app.crud.question import (
    create_question,
    get_question,
    update_question,
    delete_question,
    get_questions_by_quiz,
)
from app.crud.option import (
    create_option,
    get_option,
    update_option,
    delete_option,
    get_options_by_question,
)
from app.crud.area import get_areas
from app.crud.assignment import (
    create_assignment,
    get_assignment,
    get_assignments,
    get_user_assignments,
)
from app.crud.attempt import (
    create_attempt,
    get_attempt,
    complete_attempt,
    get_attempts,
    get_user_attempts,
)
from app.crud.response import (
    create_response,
    get_response,
    get_responses_by_attempt,
)
from app.crud.feedback import (
    create_feedback,
    get_feedback,
    get_feedback_by_response,
)
from app.crud.recommendation import (
    create_recommendation,
    get_recommendation,
    get_recommendations_by_feedback,
)

__all__ = [
    "create_user",
    "update_user",
    "get_user_by_email",
    "authenticate",
    "create_item",
]
