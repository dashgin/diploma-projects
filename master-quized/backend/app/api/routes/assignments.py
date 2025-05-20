from fastapi import APIRouter, HTTPException, status

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import AssignmentCreate, AssignmentRead

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.get("/", response_model=list[AssignmentRead])
def read_assignments(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> list[AssignmentRead]:
    """
    Retrieve quiz assignments.
    """
    # For regular users, limit to their own assignments
    # For admins, return all assignments
    if current_user.is_superuser:
        assignments = crud.get_assignments(session=session, skip=skip, limit=limit)
    else:
        assignments = crud.get_user_assignments(
            session=session, user_id=current_user.id, skip=skip, limit=limit
        )
    return assignments


@router.post("/", response_model=AssignmentRead, status_code=status.HTTP_201_CREATED)
def create_assignment(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    assignment_in: AssignmentCreate,
) -> AssignmentRead:
    """
    Create new quiz assignment.
    """
    # Check if quiz exists
    quiz = crud.get_quiz(session=session, quiz_id=assignment_in.quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )

    # Only educators or admins can create assignments
    if not current_user.is_superuser and quiz.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    assignment = crud.create_assignment(session=session, assignment_in=assignment_in)
    return assignment


@router.get("/{assignment_id}", response_model=AssignmentRead)
def read_assignment(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    assignment_id: int,
) -> AssignmentRead:
    """
    Get assignment by ID.
    """
    assignment = crud.get_assignment(session=session, assignment_id=assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found",
        )

    # Ensure user has permission to view this assignment
    if (
        not current_user.is_superuser
        and assignment.student_id != current_user.id
        and crud.get_quiz(session=session, quiz_id=assignment.quiz_id).creator_id
        != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return assignment


@router.get("/my_assignments/", response_model=list[AssignmentRead])
def read_user_assignments(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> list[AssignmentRead]:
    """
    Get assignments for the current user.
    """
    assignments = crud.get_user_assignments(
        session=session, user_id=current_user.id, skip=skip, limit=limit
    )
    return assignments
