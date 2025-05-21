from fastapi import APIRouter, HTTPException, status
from sqlmodel import func, select

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import (
    AttemptCreate,
    AttemptCreateApiSchema,
    AttemptRead,
    AttemptsPublic,
    StudentAttempt,
)

router = APIRouter(prefix="/attempts", tags=["attempts"])


@router.get("/", response_model=AttemptsPublic)
def read_attempts(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> AttemptsPublic:
    """
    Retrieve quiz attempts.
    """
    # For regular users, limit to their own attempts
    # For admins, return all attempts
    if current_user.is_superuser:
        # Get the count
        count_statement = select(func.count()).select_from(StudentAttempt)
        count = session.exec(count_statement).one()

        # Get paginated data
        attempts = crud.get_attempts(session=session, skip=skip, limit=limit)
    else:
        # Get the count
        count_statement = (
            select(func.count())
            .select_from(StudentAttempt)
            .where(StudentAttempt.student_id == current_user.id)
        )
        count = session.exec(count_statement).one()

        # Get paginated data
        attempts = crud.get_user_attempts(
            session=session, user_id=current_user.id, skip=skip, limit=limit
        )

    return AttemptsPublic(data=attempts, count=count)


@router.post("/", response_model=AttemptRead, status_code=status.HTTP_201_CREATED)
def create_attempt(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    attempt_in: AttemptCreateApiSchema,
) -> AttemptRead:
    """
    Create new quiz attempt.
    """
    # Create attempt object with current user's ID
    attempt_in = AttemptCreate(
        student_id=current_user.id,
        quiz_id=attempt_in.quiz_id,
        assignment_id=attempt_in.assignment_id,
        is_completed=attempt_in.is_completed
    )

    # Check if quiz exists
    quiz = crud.get_quiz(session=session, quiz_id=attempt_in.quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )

    # If assignment_id is provided, check if it exists and belongs to the student
    if attempt_in.assignment_id:
        assignment = crud.get_assignment(
            session=session, assignment_id=attempt_in.assignment_id
        )
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found",
            )
        if assignment.student_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Assignment does not belong to the current user",
            )

    attempt = crud.create_attempt(session=session, attempt_in=attempt_in)
    return attempt


@router.get("/{attempt_id}", response_model=AttemptRead)
def read_attempt(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    attempt_id: int,
) -> AttemptRead:
    """
    Get attempt by ID.
    """
    attempt = crud.get_attempt(session=session, attempt_id=attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    # Ensure user has permission to view this attempt
    if attempt.student_id != current_user.id and not current_user.is_superuser:
        # Check if the user is the creator of the quiz
        quiz = crud.get_quiz(session=session, quiz_id=attempt.quiz_id)
        if not quiz or quiz.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

    return attempt


@router.post("/{attempt_id}/complete", response_model=AttemptRead)
def complete_attempt(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    attempt_id: int,
    score: float | None = None,
) -> AttemptRead:
    """
    Mark a quiz attempt as completed.
    """
    attempt = crud.get_attempt(session=session, attempt_id=attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    # Ensure user has permission to complete this attempt
    if attempt.student_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    # Check if attempt is already completed
    if attempt.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempt is already completed",
        )

    attempt = crud.complete_attempt(session=session, db_attempt=attempt, score=score)
    return attempt


@router.get("/my_attempts/", response_model=AttemptsPublic)
def read_user_attempts(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> AttemptsPublic:
    """
    Get attempts for the current user.
    """
    # Get the count
    count_statement = (
        select(func.count())
        .select_from(StudentAttempt)
        .where(StudentAttempt.student_id == current_user.id)
    )
    count = session.exec(count_statement).one()

    # Get paginated data
    attempts = crud.get_user_attempts(
        session=session, user_id=current_user.id, skip=skip, limit=limit
    )

    return AttemptsPublic(data=attempts, count=count)
