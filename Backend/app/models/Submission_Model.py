from fastapi import FastAPI
from pydantic import BaseModel,EmailStr,Field
from typing import Annotated,Optional
from datetime import datetime

class SubmissionBase(BaseModel):
    submission_id : Optional[int] = None
    user_id: Annotated[int,Field(...)]
    quiz_id: Annotated[int, Field(...)]
    score: Annotated[int,Field(...)]
    submitted_at : Optional[datetime] = None
