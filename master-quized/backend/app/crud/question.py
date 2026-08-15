from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import QuestionCreate, QuestionUpdate, QuizQuestion


def create_question(*, session: Session, question_in: QuestionCreate) -> QuizQuestion:
    """Create a new question"""
    question = QuizQuestion.model_validate(question_in)
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


def get_question(*, session: Session, question_id: int) -> QuizQuestion:
    """Get a specific question by ID"""
    question = session.get(QuizQuestion, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


def update_question(
    *, session: Session, db_question: QuizQuestion, question_in: QuestionUpdate | dict
) -> QuizQuestion:
    """Update a question"""
    if isinstance(question_in, dict):
        update_data = question_in
    else:
        update_data = question_in.model_dump(exclude_unset=True)

    db_question.sqlmodel_update(update_data)
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question


def delete_question(*, session: Session, db_question: QuizQuestion) -> None:
    """Delete a question"""
    session.delete(db_question)
    session.commit()


def get_questions_by_quiz(
    *, session: Session, quiz_id: int, skip: int = 0, limit: int = 100
) -> list[QuizQuestion]:
    """Get questions for a specific quiz"""
    statement = select(QuizQuestion).where(QuizQuestion.quiz_id == quiz_id)
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()
