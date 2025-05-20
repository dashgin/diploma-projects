from fastapi import APIRouter, Depends, HTTPException, status

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_user
from app.models import QuizCreate, QuizRead, QuizUpdate

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.get("/", response_model=list[QuizRead])
def read_quizzes(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> list[QuizRead]:
    """
    Retrieve quizzes.
    """
    # Here you might add logic to filter by user role
    quizzes = crud.get_quizzes(
        session=session, skip=skip, limit=limit, user_id=current_user.id
    )
    return quizzes


@router.post("/", response_model=QuizRead, status_code=status.HTTP_201_CREATED)
def create_quiz(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    quiz_in: QuizCreate,
) -> QuizRead:
    """
    Create new quiz.
    """
    quiz = crud.create_quiz(
        session=session, quiz_in=quiz_in, creator_id=current_user.id
    )
    return quiz


@router.get(
    "/{quiz_id}", response_model=QuizRead, dependencies=[Depends(get_current_user)]
)
def read_quiz(
    *,
    session: SessionDep,
    quiz_id: int,
) -> QuizRead:
    """
    Get quiz by ID.
    """
    quiz = crud.get_quiz(session=session, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )
    return quiz


@router.put("/{quiz_id}", response_model=QuizRead)
def update_quiz(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    quiz_id: int,
    quiz_in: QuizUpdate,
) -> QuizRead:
    """
    Update a quiz.
    """
    quiz = crud.get_quiz(session=session, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )
    if quiz.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    quiz = crud.update_quiz(session=session, db_quiz=quiz, quiz_in=quiz_in)
    return quiz


@router.patch("/{quiz_id}", response_model=QuizRead)
def partially_update_quiz(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    quiz_id: int,
    quiz_in: QuizUpdate,
) -> QuizRead:
    """
    Partially update a quiz.
    """
    quiz = crud.get_quiz(session=session, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )
    if quiz.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    quiz = crud.update_quiz(session=session, db_quiz=quiz, quiz_in=quiz_in)
    return quiz


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    quiz_id: int,
) -> None:
    """
    Delete a quiz.
    """
    quiz = crud.get_quiz(session=session, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )
    if quiz.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    crud.delete_quiz(session=session, db_quiz=quiz)


@router.get("/my_quizzes/", response_model=list[QuizRead])
def read_user_quizzes(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> list[QuizRead]:
    """
    Get quizzes created by the current user.
    """
    quizzes = crud.get_user_quizzes(
        session=session, user_id=current_user.id, skip=skip, limit=limit
    )
    return quizzes
