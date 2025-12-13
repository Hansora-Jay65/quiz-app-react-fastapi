from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional


class AnswerBase(BaseModel):
    answer_id: Optional[int] = None
    question_id: Annotated[int, Field(...)]
    answer_text: Annotated[str, Field(...)]
    is_correct: Annotated[bool, Field(...)]

class UpdateAnswer(BaseModel):
    question_id: int
    answer_id: int
    answer_text: str
    answer_true: bool
