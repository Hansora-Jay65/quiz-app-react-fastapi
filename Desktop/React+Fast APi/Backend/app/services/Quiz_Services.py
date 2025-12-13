import logging
from app.models.Quiz_Model import QuizBase
from app.database import get_db_connection
from fastapi import HTTPException
from fastapi.responses import JSONResponse

import psycopg2.extras


def create_quiz(quiz: QuizBase):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                "INSERT INTO quiz(quiz_title,created_by,created_at) VALUES(%s,%s,%s)RETURNING *;",
                (
                    quiz.quiz_title,
                    quiz.created_by,
                    quiz.created_at,
                ),
            )
            new_quiz = cur.fetchone()

            conn.commit()
            cur.close()

        return QuizBase(**new_quiz)

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def get_quizzes():
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM quiz")
            rows = cur.fetchall()
            cur.close()

        if not rows:
            raise HTTPException(status_code=404, detail="No quizzes found")
        return [QuizBase(**row) for row in rows]

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def get_quiz(quiz_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM quiz WHERE quiz_id = %s", (quiz_id,))
            row = cur.fetchone()
            cur.close()

        if row is None:
            raise HTTPException(status_code=404, detail="Quiz not found")

        return QuizBase(**row)

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def edit_quiz(quiz_id: int, quiz_title: str, created_by: str):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                "UPDATE quiz SET quiz_title = %s,created_by = %s WHERE quiz_id = %s",
                (quiz_title, created_by, quiz_id),
            )
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Quiz not found")

            conn.commit()
            cur.close()

        return JSONResponse(status_code=200, content={"Quiz": "Updated"})

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def delete_quiz(quiz_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute("DELETE FROM quiz WHERE quiz_id = %s", (quiz_id,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Quiz not found")

            conn.commit()
            cur.close()

        return JSONResponse(status_code=200, content={"Quiz": "Deleted"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
