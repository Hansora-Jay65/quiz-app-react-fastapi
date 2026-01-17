import logging
from ..models.Question_Model import QuestionBase, UpdateQuestionBase
from ..database import get_db_connection
from fastapi import HTTPException
from fastapi.responses import JSONResponse

import psycopg2.extras


def create_question(question: QuestionBase):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                "INSERT INTO question(quiz_id,question_text) VALUES(%s,%s) RETURNING *;",
                (
                    question.quiz_id,
                    question.question_text,
                ),
            )
            new_question = cur.fetchone()
            conn.commit()
            cur.close()

        return JSONResponse(status_code=200, content={"Question": dict(new_question)})

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def get_question_by_quiz(quiz_id: int, question_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                "SELECT * FROM question WHERE quiz_id = %s AND question_id = %s",
                (
                    quiz_id,
                    question_id,
                ),
            )
            row = cur.fetchone()
            cur.close()

        if not row:
            raise HTTPException(status_code=404, detail="No Question found for Quiz")
        return QuestionBase(**row)

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def get_quiz_questions(quiz_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                "SELECT q.question_id,q.question_text,a.answer_id,a.answer_text,a.is_correct FROM question q JOIN answer a ON q.question_id = a.question_id WHERE q.quiz_id = %s ORDER BY q.question_id, a.answer_id;",
                (quiz_id,),
            )
            rows = cur.fetchall()
            cur.close()

        result = {}
        for row in rows:
            q_id = row["question_id"]
            if q_id not in result:
                result[q_id] = {
                    "question_id": q_id,
                    "question_text": row["question_text"],
                    "answers": [],
                }
            result[q_id]["answers"].append(
                {
                    "answer_id": row["answer_id"],
                    "answer_text": row["answer_text"],
                    "is_correct": row["is_correct"],
                }
            )

        return list(result.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_question_by_id(question_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM question WHERE question_id = %s", (question_id,))
            row = cur.fetchone()
            cur.close()

        if not row:
            raise HTTPException(status_code=404, detail="Question not found")

        return QuestionBase(**row)

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def edit_question(question: UpdateQuestionBase):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            print(
                "Function Call for update question",
                (question.quiz_id, question.question_text, question.question_id),
            )
            cur.execute(
                "UPDATE question SET question_text = %s WHERE quiz_id = %s AND question_id = %s",
                (
                    question.question_text,
                    question.quiz_id,
                    question.question_id,
                ),
            )
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Question not found")

            conn.commit()
            cur.close()

        return JSONResponse(status_code=200, content={"Question": "Updated"})

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def delete_question(quiz_id: int, question_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                "DELETE FROM question WHERE quiz_id = %s AND question_id = %s",
                (
                    quiz_id,
                    question_id,
                ),
            )

            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Question not found")

            conn.commit()
            cur.close()

        return JSONResponse(status_code=200, content={"Question": "Deleted"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
