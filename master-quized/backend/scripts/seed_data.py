#!/usr/bin/env python3
"""
Seed script to populate database with sample data for development and testing.
"""

import random
from datetime import datetime, timedelta

from sqlmodel import Session, select

from app.core.db import engine
from app.core.security import get_password_hash
from app.models import (
    KnowledgeArea,
    OptionCreate,
    QuestionCreate,
    QuestionOption,
    Quiz,
    QuizAssignment,
    QuizCreate,
    QuizQuestion,
    StudentAttempt,
    StudentResponse,
    StudyClass,
    StudyClassEnrollment,
    User,
)


def create_knowledge_areas(session: Session) -> list[KnowledgeArea]:
    """Create knowledge areas for categorizing quizzes and questions"""

    areas = [
        KnowledgeArea(
            name="Mathematics", description="Mathematical concepts and problem solving"
        ),
        KnowledgeArea(name="Science", description="Scientific principles and theories"),
        KnowledgeArea(
            name="Programming",
            description="Computer programming and software development",
        ),
        KnowledgeArea(name="History", description="Historical events and periods"),
        KnowledgeArea(
            name="Languages", description="Language learning and linguistics"
        ),
    ]

    for area in areas:
        session.add(area)

    session.commit()

    # Refresh the areas to get their assigned IDs
    for area in areas:
        session.refresh(area)

    return areas


def create_user(
    session: Session,
    email: str,
    password: str,
    full_name: str,
    is_superuser: bool = False,
    is_staff: bool = False,
    role: str = "student",
) -> User:
    """Create a user if it doesn't exist"""

    # Check if user already exists
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        hashed_password = get_password_hash(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_superuser=is_superuser,
            is_staff=is_staff,
            role=role,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"Created user: {email}")
    else:
        print(f"User already exists: {email}")

    return user


def create_quiz(
    session: Session,
    creator_id: int,
    title: str,
    area_id: int,
    questions_data: list[dict],
) -> Quiz:
    """Create a quiz with questions and options"""

    # Create the quiz
    quiz_create = QuizCreate(
        title=title,
        instructions=f"Instructions for {title}",
        area_id=area_id,
        is_active=True,
    )

    quiz = Quiz(**quiz_create.model_dump(), creator_id=creator_id)
    session.add(quiz)
    session.commit()
    session.refresh(quiz)

    # Add questions to the quiz
    for i, question_data in enumerate(questions_data):
        question_create = QuestionCreate(
            quiz_id=quiz.id,
            area_id=area_id,
            text=question_data["text"],
            question_type=question_data["type"],
            order_position=i + 1,
            correct_answer=question_data.get("correct_answer", ""),
            model_answer=question_data.get("model_answer", ""),
        )

        question = QuizQuestion(**question_create.model_dump())
        session.add(question)
        session.commit()
        session.refresh(question)

        # Add options for multiple-choice questions
        if question_data["type"] == "multiple_choice":
            for j, option_data in enumerate(question_data["options"]):
                option_create = OptionCreate(
                    question_id=question.id,
                    text=option_data["text"],
                    is_correct=option_data["is_correct"],
                    order_position=j + 1,
                )

                option = QuestionOption(**option_create.model_dump())
                session.add(option)

    session.commit()
    return quiz


def create_study_class(session: Session, educator_id: int, name: str) -> StudyClass:
    """Create a study class"""

    study_class = StudyClass(name=name, educator_id=educator_id)
    session.add(study_class)
    session.commit()
    session.refresh(study_class)

    return study_class


def enroll_students(
    session: Session, class_id: int, student_ids: list[int]
) -> list[StudyClassEnrollment]:
    """Enroll students in a class"""

    enrollments = []
    for student_id in student_ids:
        enrollment = StudyClassEnrollment(class_id=class_id, student_id=student_id)
        session.add(enrollment)
        enrollments.append(enrollment)

    session.commit()

    return enrollments


def assign_quiz(
    session: Session, quiz_id: int, student_id: int, class_id: int = None
) -> QuizAssignment:
    """Assign a quiz to a student"""

    due_date = datetime.utcnow() + timedelta(days=7)

    assignment = QuizAssignment(
        quiz_id=quiz_id,
        student_id=student_id,
        class_id=class_id,
        due_date=due_date,
    )

    session.add(assignment)
    session.commit()
    session.refresh(assignment)

    return assignment


def create_attempt(
    session: Session, quiz_id: int, student_id: int, assignment_id: int = None
) -> StudentAttempt:
    """Create a student attempt for a quiz"""

    completed = random.choice([True, False])
    completed_at = datetime.utcnow() if completed else None
    score = round(random.uniform(60, 100), 2) if completed else None

    attempt = StudentAttempt(
        quiz_id=quiz_id,
        student_id=student_id,
        assignment_id=assignment_id,
        is_completed=completed,
        completed_at=completed_at,
        score=score,
    )

    session.add(attempt)
    session.commit()
    session.refresh(attempt)

    return attempt


def create_responses(
    session: Session, attempt_id: int, questions: list[QuizQuestion]
) -> list[StudentResponse]:
    """Create student responses for a quiz attempt"""

    responses = []

    for question in questions:
        # Get options for multiple-choice questions
        options = []
        if question.question_type == "multiple_choice":
            options = session.exec(
                select(QuestionOption).where(QuestionOption.question_id == question.id)
            ).all()

        # Create a response
        if question.question_type == "multiple_choice" and options:
            # Select a random option
            selected_option = random.choice(options)

            response = StudentResponse(
                attempt_id=attempt_id,
                question_id=question.id,
                answer_text="",  # Multiple-choice doesn't need text answer
                selected_option_id=selected_option.id,
                is_correct=selected_option.is_correct,
            )
        else:
            # For short-answer questions, provide a random text response
            answer_text = f"Sample answer for question {question.id}"
            is_correct = random.choice([True, False, None])

            response = StudentResponse(
                attempt_id=attempt_id,
                question_id=question.id,
                answer_text=answer_text,
                is_correct=is_correct,
            )

        session.add(response)
        responses.append(response)

    session.commit()

    return responses


def main() -> None:
    """Main function to create sample data"""

    with Session(engine) as session:
        # Create test users if they don't exist
        print("Creating users...")

        # Create an educator
        educator = create_user(
            session=session,
            email="educator@example.com",
            password="educator123",
            full_name="Test Educator",
            is_staff=True,
            role="educator",
        )

        # Create student users
        student_emails = [
            "student1@example.com",
            "student2@example.com",
            "student3@example.com",
            "student4@example.com",
            "student5@example.com",
        ]

        students = []
        for i, email in enumerate(student_emails):
            student = create_user(
                session=session,
                email=email,
                password=f"student{i + 1}",
                full_name=f"Student {i + 1}",
                role="student",
            )
            students.append(student)

        student_ids = [student.id for student in students]

        # Create knowledge areas
        print("Creating knowledge areas...")
        areas = create_knowledge_areas(session)

        # Create quizzes
        print("Creating quizzes...")

        # Math quiz
        math_questions = [
            {
                "text": "What is 2 + 2?",
                "type": "multiple_choice",
                "options": [
                    {"text": "3", "is_correct": False},
                    {"text": "4", "is_correct": True},
                    {"text": "5", "is_correct": False},
                    {"text": "6", "is_correct": False},
                ],
            },
            {
                "text": "Solve for x: 3x - 7 = 8",
                "type": "multiple_choice",
                "options": [
                    {"text": "x = 3", "is_correct": False},
                    {"text": "x = 5", "is_correct": True},
                    {"text": "x = 7", "is_correct": False},
                    {"text": "x = 15", "is_correct": False},
                ],
            },
            {
                "text": "Explain the concept of prime numbers.",
                "type": "short_answer",
                "model_answer": "Prime numbers are natural numbers greater than 1 that are not divisible by any number other than 1 and themselves.",
            },
        ]

        math_quiz = create_quiz(
            session=session,
            creator_id=educator.id,
            title="Basic Mathematics Quiz",
            area_id=areas[0].id,
            questions_data=math_questions,
        )

        # Programming quiz
        programming_questions = [
            {
                "text": "Which is NOT a programming language?",
                "type": "multiple_choice",
                "options": [
                    {"text": "Python", "is_correct": False},
                    {"text": "Java", "is_correct": False},
                    {"text": "HTML", "is_correct": True},
                    {"text": "Rust", "is_correct": False},
                ],
            },
            {
                "text": "What is a variable?",
                "type": "short_answer",
                "model_answer": "A variable is a named storage location in a program that holds a value which can be modified during program execution.",
            },
            {
                "text": "What does the acronym API stand for?",
                "type": "multiple_choice",
                "options": [
                    {"text": "Application Programming Interface", "is_correct": True},
                    {"text": "Automated Program Instruction", "is_correct": False},
                    {
                        "text": "Advanced Programming Implementation",
                        "is_correct": False,
                    },
                    {"text": "Application Process Integration", "is_correct": False},
                ],
            },
        ]

        programming_quiz = create_quiz(
            session=session,
            creator_id=educator.id,
            title="Introduction to Programming",
            area_id=areas[2].id,
            questions_data=programming_questions,
        )

        # Create study classes
        print("Creating study classes...")
        math_class = create_study_class(session, educator.id, "Mathematics 101")
        programming_class = create_study_class(
            session, educator.id, "Programming Fundamentals"
        )

        # Enroll students in classes
        print("Enrolling students...")
        enroll_students(
            session, math_class.id, student_ids[:3]
        )  # First 3 students in math
        enroll_students(
            session, programming_class.id, student_ids[2:]
        )  # Last 3 students in programming

        # Assign quizzes to students
        print("Assigning quizzes...")
        for student_id in student_ids[:3]:
            assign_quiz(session, math_quiz.id, student_id, math_class.id)

        for student_id in student_ids[2:]:
            assign_quiz(session, programming_quiz.id, student_id, programming_class.id)

        # Create attempts and responses
        print("Creating quiz attempts and responses...")

        # Get all questions for each quiz
        math_questions = session.exec(
            select(QuizQuestion).where(QuizQuestion.quiz_id == math_quiz.id)
        ).all()

        programming_questions = session.exec(
            select(QuizQuestion).where(QuizQuestion.quiz_id == programming_quiz.id)
        ).all()

        # Create attempts for math quiz
        for student_id in student_ids[:3]:
            attempt = create_attempt(session, math_quiz.id, student_id)
            create_responses(session, attempt.id, math_questions)

        # Create attempts for programming quiz
        for student_id in student_ids[2:]:
            attempt = create_attempt(session, programming_quiz.id, student_id)
            create_responses(session, attempt.id, programming_questions)

        print("Sample data created successfully!")


if __name__ == "__main__":
    main()
