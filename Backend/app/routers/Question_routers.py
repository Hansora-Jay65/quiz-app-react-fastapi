from typing import List
from fastapi import APIRouter, Request
from ..models.Question_Model import (
    QuestionAndAnswerModel,
    QuestionBase,
    UpdateQuestionBase,
)

from ..services.Question_Services import (
    get_question_by_id,
    get_question_by_quiz,
    get_quiz_questions,
    create_question,
    edit_question,
    delete_question,
)
from ..utils.validation import validate_question_text
from ..rate_limiter import limiter

router = APIRouter(prefix="/Questions", tags=["Questions"])


@router.get("/getQuestion")
@limiter.limit("60/minute")  # 60 requests per minute per IP
def get_Question(request: Request, question_id: int):
    return get_question_by_id(question_id)


@router.get("/getQuestionByQuiz")
@limiter.limit("60/minute")  # 60 requests per minute per IP
def get_Quiz_Question(request: Request, quiz_id: int, question_id: int):
    return get_question_by_quiz(quiz_id, question_id)


@router.get("/getQuizQuestions", response_model=List[QuestionAndAnswerModel])
@limiter.limit("60/minute")  # 60 requests per minute per IP
def get_Quiz_Questions(request: Request, quiz_id: int):
    return get_quiz_questions(quiz_id)


@router.post("/createQuestion")
@limiter.limit("30/minute")  # 30 question creations per minute per IP
def create_Question(request: Request, question: QuestionBase):
    # Validate and sanitize question text
    question.question_text = validate_question_text(question.question_text)
    return create_question(question)


@router.put("/editQuestion")
@limiter.limit("30/minute")  # 30 edits per minute per IP
def edit_Question(request: Request, quetion: UpdateQuestionBase):
    # Validate and sanitize question text
    quetion.question_text = validate_question_text(quetion.question_text)
    return edit_question(quetion)


@router.delete("/deleteQuestion")
@limiter.limit("20/minute")  # 20 deletions per minute per IP
def delete_Question(request: Request, quiz_id: int, question_id: int):
    return delete_question(quiz_id, question_id)
