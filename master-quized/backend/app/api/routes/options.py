from fastapi import APIRouter, Depends, HTTPException, Query, status

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_user
from app.models import OptionCreate, OptionRead, OptionUpdate

router = APIRouter(prefix="/options", tags=["options"])


@router.post("/", response_model=OptionRead, status_code=status.HTTP_201_CREATED)
def create_option(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    option_in: OptionCreate,
) -> OptionRead:
    """
    Create new question option.
    """
    # Check if question exists and user has permission to add options to it
    question = crud.get_question(session=session, question_id=option_in.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )
    # Check if user has permission to add options to this question
    quiz = crud.get_quiz(session=session, quiz_id=question.quiz_id)
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

    option = crud.create_option(session=session, option_in=option_in)
    return option


@router.get("/{option_id}", dependencies=[Depends(get_current_user)])
def read_option(
    *,
    session: SessionDep,
    option_id: int,
) -> OptionRead:
    """
    Get option by ID.
    """
    option = crud.get_option(session=session, option_id=option_id)
    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Option not found",
        )
    # For additional security, we could check if the user has permission to view this option
    return option


@router.put("/{option_id}")
def update_option(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    option_id: int,
    option_in: OptionUpdate,
) -> OptionRead:
    """
    Update an option.
    """
    option = crud.get_option(session=session, option_id=option_id)
    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Option not found",
        )
    # Check if user has permission to update this option
    question = crud.get_question(session=session, question_id=option.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )
    quiz = crud.get_quiz(session=session, quiz_id=question.quiz_id)
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

    option = crud.update_option(session=session, db_option=option, option_in=option_in)
    return option


@router.patch("/{option_id}", response_model=OptionRead)
def partially_update_option(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    option_id: int,
    option_in: OptionUpdate,
) -> OptionRead:
    """
    Partially update an option.
    """
    option = crud.get_option(session=session, option_id=option_id)
    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Option not found",
        )
    # Check if user has permission to update this option
    question = crud.get_question(session=session, question_id=option.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )
    quiz = crud.get_quiz(session=session, quiz_id=question.quiz_id)
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

    option = crud.update_option(session=session, db_option=option, option_in=option_in)
    return option


@router.delete("/{option_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_option(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    option_id: int,
) -> None:
    """
    Delete an option.
    """
    option = crud.get_option(session=session, option_id=option_id)
    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Option not found",
        )
    # Check if user has permission to delete this option
    question = crud.get_question(session=session, question_id=option.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )
    quiz = crud.get_quiz(session=session, quiz_id=question.quiz_id)
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

    crud.delete_option(session=session, db_option=option)


@router.get("/by_question/", dependencies=[Depends(get_current_user)])
def read_options_by_question(
    *,
    session: SessionDep,
    question_id: int = Query(..., description="ID of the question to get options for"),
    skip: int = 0,
    limit: int = 100,
) -> list[OptionRead]:
    """
    Get options for a specific question.
    """
    # Check if question exists
    question = crud.get_question(session=session, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    options = crud.get_options_by_question(
        session=session, question_id=question_id, skip=skip, limit=limit
    )
    return options
