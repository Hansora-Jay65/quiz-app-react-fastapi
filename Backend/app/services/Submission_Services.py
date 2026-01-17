import logging
from app.models.Submission_Model import SubmissionBase
from app.database import get_db_connection
from fastapi import HTTPException
from fastapi.responses import JSONResponse

import psycopg2.extras


def create_submission(submission: SubmissionBase):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                "INSERT INTO submission(user_id,quiz_id,score,submitted_at) VALUES(%s,%s,%s,%s);",
                (
                    submission.user_id,
                    submission.quiz_id,
                    submission.score,
                    submission.submitted_at,
                ),
            )

            conn.commit()
            cur.close()

        return JSONResponse(status_code=200, content={"Submission": "Submitted"})

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def get_quiz_statistics(quiz_id: int):
    """Return basic statistics for a given quiz based on submissions.

    Stats include:
    - total_attempts
    - average_score
    - best_score
    - total_questions
    - average_percentage
    - best_percentage
    """

    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # Get question count for this quiz
            cur.execute("SELECT COUNT(*) AS total_questions FROM question WHERE quiz_id = %s", (quiz_id,))
            q_row = cur.fetchone()
            total_questions = q_row["total_questions"] if q_row else 0

            # Get aggregate stats from submissions
            cur.execute(
                """
                SELECT
                    COUNT(*) AS attempts,
                    AVG(score)::float AS average_score,
                    MAX(score) AS best_score
                FROM submission
                WHERE quiz_id = %s
                """,
                (quiz_id,),
            )
            s_row = cur.fetchone()
            cur.close()

        if not s_row or s_row["attempts"] == 0:
            raise HTTPException(status_code=404, detail="No submissions found for quiz")

        attempts = s_row["attempts"] or 0
        average_score = s_row["average_score"] or 0.0
        best_score = s_row["best_score"] or 0

        if total_questions and total_questions > 0:
            average_percentage = round((average_score / total_questions) * 100, 2)
            best_percentage = round((best_score / total_questions) * 100, 2)
        else:
            average_percentage = None
            best_percentage = None

        return {
            "quiz_id": quiz_id,
            "total_attempts": attempts,
            "average_score": average_score,
            "best_score": best_score,
            "total_questions": total_questions,
            "average_percentage": average_percentage,
            "best_percentage": best_percentage,
        }

    except HTTPException:
        # Re-raise HTTPExceptions directly
        raise
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def get_leaderboard_by_quiz(quiz_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                "SELECT * FROM submission WHERE quiz_id = %s ORDER BY score DESC, submitted_at ASC",
                (quiz_id,),
            )
            rows = cur.fetchall()
            cur.close()

        if not rows:
            raise HTTPException(status_code=404, detail="No Submission found for Quiz")
        return [SubmissionBase(**row) for row in rows]

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def get_submission_by_user(user_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM submission WHERE user_id = %s", (user_id,))
            rows = cur.fetchall()
            cur.close()

        if not rows:
            raise HTTPException(status_code=404, detail="No Submission found for user")
        return [SubmissionBase(**row) for row in rows]

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
