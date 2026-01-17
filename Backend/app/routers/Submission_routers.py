from fastapi import APIRouter, Request
from ..models.Submission_Model import SubmissionBase
from ..services.Submission_Services import (
    get_leaderboard_by_quiz,
    get_submission_by_user,
    create_submission,
    get_quiz_statistics,
)
from .rate_limiter import limiter

router = APIRouter(prefix="/Submissions", tags=["Submissions"])


@router.get("/getLeaderboardByQuiz")
@limiter.limit("60/minute")  # 60 requests per minute per IP
def get_User(request: Request, quiz_id: int):
    return get_leaderboard_by_quiz(quiz_id)


@router.get("/getSubmissionByUser")
@limiter.limit("60/minute")  # 60 requests per minute per IP
def create_User(request: Request, user_id: int):
    return get_submission_by_user(user_id)


@router.post("/createSubmission")
@limiter.limit("30/minute")  # 30 submissions per minute per IP
def create_Submission(request: Request, submission: SubmissionBase):
    return create_submission(submission)


@router.get("/getQuizStatistics")
@limiter.limit("60/minute")  # 60 requests per minute per IP
def get_Quiz_Statistics(request: Request, quiz_id: int):
    return get_quiz_statistics(quiz_id)
