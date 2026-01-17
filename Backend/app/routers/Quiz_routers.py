from fastapi import APIRouter, Request
from ..models.Quiz_Model import QuizBase
from ..services.Quiz_Services import (
    create_quiz,
    get_quiz,
    get_quizzes,
    edit_quiz,
    delete_quiz,
)
from ..utils.validation import sanitize_quiz_title, sanitize_creator_name
from ..rate_limiter import limiter

router = APIRouter(prefix="/Quizzes", tags=["Quizzes"])


@router.get("/getQuiz")
@limiter.limit("60/minute")  # 60 requests per minute per IP
def get_Quiz(request: Request, quiz_id: int):
    return get_quiz(quiz_id)


@router.get("/getQuizzes")
@limiter.limit("60/minute")  # 60 requests per minute per IP
def get_Quizzes(request: Request):
    return get_quizzes()


@router.post("/createQuiz")
@limiter.limit("20/minute")  # 20 quiz creations per minute per IP
def create_Quiz(request: Request, quiz: QuizBase):
    # Validate and sanitize inputs
    quiz.quiz_title = sanitize_quiz_title(quiz.quiz_title)
    quiz.created_by = sanitize_creator_name(quiz.created_by)
    return create_quiz(quiz)


@router.put("/editQuiz")
@limiter.limit("30/minute")  # 30 edits per minute per IP
def edit_Quiz(request: Request, quiz_id: int, quiz_title: str, created_by: str):
    # Validate and sanitize inputs
    quiz_title = sanitize_quiz_title(quiz_title)
    created_by = sanitize_creator_name(created_by)
    return edit_quiz(quiz_id, quiz_title, created_by)


@router.delete("/deleteQuiz")
@limiter.limit("10/minute")  # 10 deletions per minute per IP (prevent abuse)
def delete_Quiz(request: Request, quiz_id: int):
    return delete_quiz(quiz_id)
