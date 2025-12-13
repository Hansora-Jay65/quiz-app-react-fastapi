from fastapi import FastAPI
from pydantic import BaseModel,EmailStr,Field
from typing import Annotated,Optional
from datetime import datetime


class User(BaseModel):
    user_id: Optional[int] = None
    user_email: Annotated[EmailStr,Field(...)]
    hashed_password: str
    created_at: Annotated[datetime,Field(default_factory= datetime.now)]

class UserLogin(BaseModel):
    user_email: EmailStr
    password: str