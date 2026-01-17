from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import logging
from .routers import (
    User_routers,
    Submission_routers,
    Question_routers,
    Quiz_routers,
    Answer_routers,
    PDF_MCQ_routers,
)
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .rate_limiter import limiter
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="Quiz App API")

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(
        "HTTPException: %s %s - %s", request.method, request.url.path, exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "path": str(request.url.path),
            },
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logging.exception("Unhandled exception for %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": 500,
                "message": "Internal server error",
                "path": str(request.url.path),
            },
        },
    )

# CORS Configuration from environment variables
# For development: Use CORS_ORIGINS=http://localhost:5173
# For production: Use CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
# Multiple origins should be comma-separated
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173")
cors_origins = [
    origin.strip() for origin in cors_origins_env.split(",") if origin.strip()
]

# In production, never allow all origins
if os.getenv("ENVIRONMENT", "development").lower() == "production":
    if "*" in cors_origins or len(cors_origins) == 0:
        raise ValueError(
            "⚠️ SECURITY ERROR: In production, CORS_ORIGINS must be explicitly set. "
            "Cannot use '*' or empty list. Set CORS_ORIGINS in your .env file."
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicit methods
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(User_routers.router, tags=["Users"])
app.include_router(
    Submission_routers.router, prefix="/Submissions", tags=["Submissions"]
)
app.include_router(Question_routers.router, prefix="/Questions", tags=["Questions"])
app.include_router(Quiz_routers.router, prefix="/Quizzes", tags=["Quizzes"])
app.include_router(Answer_routers.router, prefix="/Answers", tags=["Answers"])
app.include_router(PDF_MCQ_routers.router, tags=["PDF MCQ Generator"])

@app.get("/")
def home():
    return {"Message": "Welcome to Quiz App API"}
