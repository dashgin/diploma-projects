from fastapi import APIRouter, HTTPException, Query, status

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import ResourceCreate, ResourceRead

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
def create_recommendation(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    resource_in: ResourceCreate,
) -> ResourceRead:
    """
    Create new learning resource recommendation.
    """
    # Check if feedback exists
    feedback = crud.get_feedback(session=session, feedback_id=resource_in.feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found",
        )

    # Check user permissions
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

    quiz = crud.get_quiz(session=session, quiz_id=attempt.quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )

    # Only quiz creator or admin can create recommendations
    if quiz.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    resource = crud.create_recommendation(session=session, resource_in=resource_in)
    return resource


@router.get("/{resource_id}", response_model=ResourceRead)
def read_recommendation(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    resource_id: int,
) -> ResourceRead:
    """
    Get recommendation by ID.
    """
    resource = crud.get_recommendation(session=session, resource_id=resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found",
        )

    # Check user permissions
    feedback = crud.get_feedback(session=session, feedback_id=resource.feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found",
        )

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

    # Student who made the attempt, quiz creator, or admin can view recommendations
    if attempt.student_id != current_user.id and not current_user.is_superuser:
        quiz = crud.get_quiz(session=session, quiz_id=attempt.quiz_id)
        if not quiz or quiz.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

    return resource


@router.get("/by_feedback/", response_model=list[ResourceRead])
def read_recommendations_by_feedback(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    feedback_id: int = Query(
        ..., description="ID of the feedback to get recommendations for"
    ),
    skip: int = 0,
    limit: int = 100,
) -> list[ResourceRead]:
    """
    Get recommendations for a specific feedback.
    """
    # Check if feedback exists
    feedback = crud.get_feedback(session=session, feedback_id=feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found",
        )

    # Check user permissions
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

    # Student who made the attempt, quiz creator, or admin can view recommendations
    if attempt.student_id != current_user.id and not current_user.is_superuser:
        quiz = crud.get_quiz(session=session, quiz_id=attempt.quiz_id)
        if not quiz or quiz.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

    recommendations = crud.get_recommendations_by_feedback(
        session=session, feedback_id=feedback_id, skip=skip, limit=limit
    )
    return recommendations
