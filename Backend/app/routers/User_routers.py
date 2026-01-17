from ..configAndAuth import authenticate_user, create_access_token
from ..services.User_Services import get_user, create_user
from ..utils.validation import validate_email, validate_password_strength
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Request
from ..models.User_Model import User
from datetime import timedelta
from .rate_limiter import limiter

router = APIRouter(prefix="/Users", tags=["Users"])


@router.get("/getUser")
@limiter.limit("30/minute")  # 30 requests per minute per IP
def get_User(request: Request, user_id: int):
    return get_user(user_id)


@router.post("/createUser")
@limiter.limit("5/minute")  # 5 registrations per minute per IP (prevent spam)
def create_User(request: Request, user: User):
    # Validate and sanitize email
    user.user_email = validate_email(user.user_email)

    # Validate password strength
    validate_password_strength(user.hashed_password)

    return create_user(user)


@router.post("/login")
@limiter.limit("10/minute")  # 10 login attempts per minute per IP (prevent brute force)
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # JWT token with subject = user email
    access_token = create_access_token(
        data={"sub": user["user_email"], "user_id": user["user_id"]},
        expires_delta=timedelta(minutes=60),
    )
    print(f"Generated JWT Token for {user['user_email']}: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}
