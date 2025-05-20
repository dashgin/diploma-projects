from sqlmodel import Session, select

from app.models import QuestionOption, OptionCreate, OptionUpdate


def create_option(*, session: Session, option_in: OptionCreate) -> QuestionOption:
    """Create a new question option"""
    option = QuestionOption.model_validate(option_in)
    session.add(option)
    session.commit()
    session.refresh(option)
    return option


def get_option(*, session: Session, option_id: int) -> QuestionOption | None:
    """Get a specific option by ID"""
    return session.get(QuestionOption, option_id)


def update_option(
    *, session: Session, db_option: QuestionOption, option_in: OptionUpdate | dict
) -> QuestionOption:
    """Update a question option"""
    if isinstance(option_in, dict):
        update_data = option_in
    else:
        update_data = option_in.model_dump(exclude_unset=True)
    
    db_option.sqlmodel_update(update_data)
    session.add(db_option)
    session.commit()
    session.refresh(db_option)
    return db_option


def delete_option(*, session: Session, db_option: QuestionOption) -> None:
    """Delete a question option"""
    session.delete(db_option)
    session.commit()


def get_options_by_question(
    *, session: Session, question_id: int, skip: int = 0, limit: int = 100
) -> list[QuestionOption]:
    """Get options for a specific question"""
    statement = select(QuestionOption).where(QuestionOption.question_id == question_id)
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all() 