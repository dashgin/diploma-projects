from fastapi import APIRouter, HTTPException, Query, status

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import FeedbackCreate, FeedbackRead

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/", response_model=FeedbackRead, status_code=status.HTTP_201_CREATED)
def create_feedback(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    feedback_in: FeedbackCreate,
) -> FeedbackRead:
    """
    Create new AI feedback.
    """
    # Check if response exists
    response = crud.get_response(session=session, response_id=feedback_in.response_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )

    # Check if feedback already exists for this response
    existing_feedback = crud.get_feedback_by_response(
        session=session, response_id=feedback_in.response_id
    )
    if existing_feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback already exists for this response",
        )

    # Check if user has permission to create feedback
    attempt = crud.get_attempt(session=session, attempt_id=response.attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    quiz = crud.get_quiz(session=session, quiz_id=attempt.quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )

    # Only quiz creator or admin can create feedback
    if quiz.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    feedback = crud.create_feedback(session=session, feedback_in=feedback_in)
    return feedback


@router.get("/{feedback_id}", response_model=FeedbackRead)
def read_feedback(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    feedback_id: int,
) -> FeedbackRead:
    """
    Get feedback by ID.
    """
    feedback = crud.get_feedback(session=session, feedback_id=feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found",
        )

    # Ensure user has permission to view this feedback
    response = crud.get_response(session=session, response_id=feedback.response_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )

    attempt = crud.get_attempt(session=session, attempt_id=response.attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    # Student who made the attempt, quiz creator, or admin can view feedback
    if attempt.student_id != current_user.id and not current_user.is_superuser:
        quiz = crud.get_quiz(session=session, quiz_id=attempt.quiz_id)
        if not quiz or quiz.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

    return feedback


@router.get("/by_response/", response_model=FeedbackRead | None)
def read_feedback_by_response(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    response_id: int = Query(..., description="ID of the response to get feedback for"),
) -> FeedbackRead | None:
    """
    Get feedback for a specific response.
    """
    # Check if response exists
    response = crud.get_response(session=session, response_id=response_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )

    # Ensure user has permission to view feedback for this response
    attempt = crud.get_attempt(session=session, attempt_id=response.attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    # Student who made the attempt, quiz creator, or admin can view feedback
    if attempt.student_id != current_user.id and not current_user.is_superuser:
        quiz = crud.get_quiz(session=session, quiz_id=attempt.quiz_id)
        if not quiz or quiz.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

    feedback = crud.get_feedback_by_response(session=session, response_id=response_id)
    return feedback
