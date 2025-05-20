from sqlmodel import Session, select

from app.models import Quiz, QuizCreate, QuizUpdate


def create_quiz(*, session: Session, quiz_in: QuizCreate, creator_id: int) -> Quiz:
    """Create a new quiz"""
    quiz = Quiz.model_validate(quiz_in, update={"creator_id": creator_id})
    session.add(quiz)
    session.commit()
    session.refresh(quiz)
    return quiz


def get_quiz(*, session: Session, quiz_id: int) -> Quiz | None:
    """Get a specific quiz by ID"""
    return session.get(Quiz, quiz_id)


def update_quiz(
    *, session: Session, db_quiz: Quiz, quiz_in: QuizUpdate | dict
) -> Quiz:
    """Update a quiz"""
    if isinstance(quiz_in, dict):
        update_data = quiz_in
    else:
        update_data = quiz_in.model_dump(exclude_unset=True)
    
    db_quiz.sqlmodel_update(update_data)
    session.add(db_quiz)
    session.commit()
    session.refresh(db_quiz)
    return db_quiz


def delete_quiz(*, session: Session, db_quiz: Quiz) -> None:
    """Delete a quiz"""
    session.delete(db_quiz)
    session.commit()


def get_quizzes(
    *, session: Session, skip: int = 0, limit: int = 100, user_id: int | None = None
) -> list[Quiz]:
    """Get a list of quizzes, optionally filtered by user role"""
    statement = select(Quiz)
    # If we want to filter by user role, we would add conditions here
    
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()


def get_user_quizzes(
    *, session: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[Quiz]:
    """Get quizzes created by a specific user"""
    statement = select(Quiz).where(Quiz.creator_id == user_id)
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all() 