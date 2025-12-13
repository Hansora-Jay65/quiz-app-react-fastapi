from fastapi import FastAPI
from pydantic import BaseModel,EmailStr,Field
from typing import Annotated,Optional

from datetime import datetime

class QuizBase(BaseModel):
    quiz_id: Optional[int] = None
    quiz_title: Annotated[str,Field(...)]
    created_by: Annotated[str,Field(...)]
    created_at: Annotated[datetime,Field(default_factory=datetime.now)]
    