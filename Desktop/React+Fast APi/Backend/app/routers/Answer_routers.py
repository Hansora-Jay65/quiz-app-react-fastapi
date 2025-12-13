from fastapi import APIRouter, Request
from app.models.Answer_Model import AnswerBase, UpdateAnswer
from app.services.Answer_Services import (
    create_answer,
    get_all_answers_by_question,
    update_answer_of_question,
    delete_answer,
)
from app.utils.validation import validate_answer_text
from app.rate_limiter import limiter

router = APIRouter(prefix="/Answers", tags=["Answers"])


@router.get("/getAnswer")
@limiter.limit("60/minute")  # 60 requests per minute per IP
def get_Answer_By_Question(request: Request, question_id: int):
    return get_all_answers_by_question(question_id)


@router.post("/createAnswer")
@limiter.limit("30/minute")  # 30 answer creations per minute per IP
def create_Answer(request: Request, answer: AnswerBase):
    # Validate and sanitize answer text
    answer.answer_text = validate_answer_text(answer.answer_text)
    return create_answer(answer)


@router.put("/editAnswer")
@limiter.limit("30/minute")  # 30 edits per minute per IP
def edit_Answer(request: Request, answer: UpdateAnswer):
    # Validate and sanitize answer text
    answer.answer_text = validate_answer_text(answer.answer_text)
    return update_answer_of_question(answer)


@router.delete("/deleteAnswer")
@limiter.limit("20/minute")  # 20 deletions per minute per IP
def delete_Question(request: Request, question_id: int, answer_id: int):
    return delete_answer(question_id, answer_id)
