import logging
from ..models.Answer_Model import AnswerBase, UpdateAnswer
from ..database import get_db_connection
from fastapi import HTTPException
from fastapi.responses import JSONResponse

import psycopg2.extras


def create_answer(answer: AnswerBase):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute(
                "INSERT INTO answer(question_id,answer_text,is_correct) VALUES(%s,%s,%s);",
                (
                    answer.question_id,
                    answer.answer_text,
                    answer.is_correct,
                ),
            )

            conn.commit()
            cur.close()

        return JSONResponse(status_code=200, content={"Answer": "created"})

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def get_all_answers_by_question(question_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                "SELECT * FROM answer WHERE question_id = %s;",
                (question_id,),
            )
            rows = cur.fetchall()
            print(rows)
            cur.close()

        if not rows:
            raise HTTPException(status_code=404, detail="No Answers found for Question")
        return [AnswerBase(**row) for row in rows]

    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


def update_answer_of_question(answer: UpdateAnswer):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            print(
            "Function Call For Update Answer",
            (
                answer.question_id,
                answer.answer_id,
                answer.answer_text,
                answer.answer_true,
            ),
        )
            cur.execute(
                "UPDATE answer SET answer_text = %s ,is_correct = %s WHERE question_id = %s AND answer_id = %s",
                (
                    answer.answer_text,
                    answer.answer_true,
                    answer.question_id,
                    answer.answer_id,
                ),
            )

            conn.commit()
            cur.close()

        return JSONResponse(status_code=200, content={"Answer": "Updated"})

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def delete_answer(question_id: int, answer_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                "DELETE FROM answer WHERE question_id = %s AND answer_id = %s",
                (
                    question_id,
                    answer_id,
                ),
            )

            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Answer not found")

            conn.commit()
            cur.close()

        return JSONResponse(status_code=200, content={"Answer": "Deleted"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
