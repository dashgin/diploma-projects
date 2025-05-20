from fastapi import APIRouter, Depends, HTTPException, Query, status

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_user
from app.models import QuestionCreate, QuestionRead, QuestionUpdate

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def create_question(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    question_in: QuestionCreate,
) -> QuestionRead:
    """
    Create new question.
    """
    # Check if quiz exists and user has permission to add questions to it
    quiz = crud.get_quiz(session=session, quiz_id=question_in.quiz_id)
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

    question = crud.create_question(session=session, question_in=question_in)
    return question


@router.get(
    "/by_quiz/",
    response_model=list[QuestionRead],
    dependencies=[Depends(get_current_user)],
)
def read_questions_by_quiz(
    *,
    session: SessionDep,
    quiz_id: int = Query(..., description="ID of the quiz to get questions for"),
    skip: int = 0,
    limit: int = 100,
) -> list[QuestionRead]:
    """
    Get questions for a specific quiz.
    """
    # Check if quiz exists
    quiz = crud.get_quiz(session=session, quiz_id=quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )

    questions = crud.get_questions_by_quiz(
        session=session, quiz_id=quiz_id, skip=skip, limit=limit
    )
    return questions


@router.get("/{question_id}", dependencies=[Depends(get_current_user)])
def read_question(
    *,
    session: SessionDep,
    question_id: int,
) -> QuestionRead:
    """
    Get question by ID.
    """
    question = crud.get_question(session=session, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )
    # Check if user has permission to view the question
    quiz = crud.get_quiz(session=session, quiz_id=question.quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found",
        )
    return question


@router.put("/{question_id}", response_model=QuestionRead)
def update_question(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    question_id: int,
    question_in: QuestionUpdate,
) -> QuestionRead:
    """
    Update a question.
    """
    question = crud.get_question(session=session, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )
    # Check if user has permission to update the question
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

    question = crud.update_question(
        session=session, db_question=question, question_in=question_in
    )
    return question


@router.patch("/{question_id}", response_model=QuestionRead)
def partially_update_question(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    question_id: int,
    question_in: QuestionUpdate,
) -> QuestionRead:
    """
    Partially update a question.
    """
    question = crud.get_question(session=session, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )
    # Check if user has permission to update the question
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

    question = crud.update_question(
        session=session, db_question=question, question_in=question_in
    )
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    question_id: int,
) -> None:
    """
    Delete a question.
    """
    question = crud.get_question(session=session, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )
    # Check if user has permission to delete the question
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

    crud.delete_question(session=session, db_question=question)
