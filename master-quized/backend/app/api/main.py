from fastapi import APIRouter

from app.api.routes import (
    areas,
    assignments,
    attempts,
    feedback,
    login,
    options,
    questions,
    quizzes,
    recommendations,
    responses,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)

# Include new routes
api_router.include_router(areas.router)
api_router.include_router(quizzes.router)
api_router.include_router(questions.router)
api_router.include_router(options.router)
api_router.include_router(assignments.router)
api_router.include_router(attempts.router)
api_router.include_router(responses.router)
api_router.include_router(feedback.router)
api_router.include_router(recommendations.router)
