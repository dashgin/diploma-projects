from fastapi import APIRouter, HTTPException, Query, status

from app import crud
from app.api.deps import CurrentUser, SessionDep
from app.models import ResponseCreate, ResponseRead, ResponseWithDetails

router = APIRouter(prefix="/responses", tags=["responses"])


@router.post("/", response_model=ResponseRead, status_code=status.HTTP_201_CREATED)
def create_response(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    response_in: ResponseCreate,
) -> ResponseRead:
    """
    Create new student response.
    """
    # Check if attempt exists
    attempt = crud.get_attempt(session=session, attempt_id=response_in.attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    # Ensure user has permission to create a response for this attempt
    if attempt.student_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    # Check if attempt is already completed
    if attempt.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add responses to a completed attempt",
        )

    # Check if question exists
    question = crud.get_question(session=session, question_id=response_in.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    # Validate response data based on question type
    if question.question_type == "multiple_choice":
        if not response_in.selected_option_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="selected_option_id is required for multiple-choice questions",
            )
    elif question.question_type == "short_answer":
        if not response_in.answer_text or response_in.answer_text.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="answer_text is required for short-answer questions",
            )
        if response_in.selected_option_id is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="selected_option_id should not be provided for short-answer questions",
            )

    # If selected_option_id is provided, check if it exists and belongs to the question
    if response_in.selected_option_id:
        option = crud.get_option(
            session=session, option_id=response_in.selected_option_id
        )
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Option not found",
            )
        if option.question_id != response_in.question_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Option does not belong to the specified question",
            )

    response = crud.create_response(session=session, response_in=response_in)
    return response


@router.get("/{response_id}", response_model=ResponseRead)
def read_response(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    response_id: int,
) -> ResponseRead:
    """
    Get response by ID.
    """
    response = crud.get_response(session=session, response_id=response_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )

    # Ensure user has permission to view this response
    attempt = crud.get_attempt(session=session, attempt_id=response.attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    if attempt.student_id != current_user.id and not current_user.is_superuser:
        # Check if the user is the creator of the quiz
        quiz = crud.get_quiz(session=session, quiz_id=attempt.quiz_id)
        if not quiz or quiz.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

    return response


@router.get("/by_attempt/", response_model=list[ResponseWithDetails])
def read_responses_by_attempt(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    attempt_id: int = Query(..., description="ID of the attempt to get responses for"),
    skip: int = 0,
    limit: int = 100,
) -> list[ResponseWithDetails]:
    """
    Get responses for a specific quiz attempt.
    """
    # Check if attempt exists
    attempt = crud.get_attempt(session=session, attempt_id=attempt_id)
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    # Ensure user has permission to view responses for this attempt
    if attempt.student_id != current_user.id and not current_user.is_superuser:
        # Check if the user is the creator of the quiz
        quiz = crud.get_quiz(session=session, quiz_id=attempt.quiz_id)
        if not quiz or quiz.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

    responses = crud.get_responses_by_attempt(
        session=session, attempt_id=attempt_id, skip=skip, limit=limit
    )

    # Enhance responses with question details for completed attempts
    if attempt.is_completed:
        responses_with_details = []
        for response in responses:
            # Get the question
            question = crud.get_question(session=session, question_id=response.question_id)

            # Get correct answers for this question
            correct_options = []
            if question.question_type == "multiple_choice":
                options = crud.get_options_by_question(
                    session=session, question_id=question.id
                )
                correct_options = [opt for opt in options if opt.is_correct]

            # Check if response is correct
            is_correct = False
            if response.selected_option_id and any(opt.id == response.selected_option_id for opt in correct_options):
                is_correct = True
            elif question.question_type == "short_answer" and response.answer_text.strip().lower() == question.correct_answer.strip().lower():
                is_correct = True

            # Create enhanced response
            enhanced_response = ResponseWithDetails(
                **response.model_dump(),
                explanation=question.explanation
            )
            # Update is_correct after creation to avoid duplicate
            enhanced_response.is_correct = is_correct
            responses_with_details.append(enhanced_response)

        return responses_with_details

    return [ResponseWithDetails(**r.model_dump(), explanation=None) for r in responses]
