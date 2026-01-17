from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, List, Optional


class QuestionBase(BaseModel):
    question_id: Optional[int] = None
    quiz_id: Annotated[int, Field(...)]
    question_text: Annotated[str, Field(...)]

class UpdateQuestionBase(BaseModel):
    quiz_id: int
    question_text: str
    question_id: int

class Answer(BaseModel):
    answer_id: int
    answer_text: str
    is_correct: bool


class QuestionAndAnswerModel(BaseModel):
    question_id: int
    question_text: str
    answers: List[Answer]
