from    pydantic import EmailStr
from ..models.User_Model import User, UserLogin
from ..database import get_db_connection
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import psycopg2.extras
import logging
from datetime import datetime
from ..configAndAuth import get_password_hash, verify_password


def create_user(user: User):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # Hash the password before saving (truncate if too long)
            password = user.hashed_password[:72]  # bcrypt max 72 bytes
            hashed_pw = get_password_hash(password)

            # Use current timestamp for created_at to avoid client-side date issues
            created_at = datetime.utcnow()

            cur.execute(
                "INSERT INTO users(user_email, hashed_password, created_at) VALUES(%s, %s, %s) RETURNING user_id, user_email, created_at",
                (
                    user.user_email,
                    hashed_pw,
                    created_at,
                ),
            )

            conn.commit()
            row = cur.fetchone()
            cur.close()

        # Convert DB row (which may contain date/datetime) into JSON-serializable dict
        if row is not None:
            result = dict(row)
            if "created_at" in result:
                # handle both date and datetime objects
                value = result["created_at"]
                try:
                    result["created_at"] = value.isoformat()
                except AttributeError:
                    result["created_at"] = str(value)
        else:
            result = {"message": "User created"}

        return JSONResponse(status_code=201, content=result)

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def get_user(user_id: int):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            row = cur.fetchone()
            cur.close()

        return User(**row)

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def check_UserExist_in_db(user: UserLogin):
    try:
        with get_db_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("SELECT * FROM users WHERE user_email = %s", (user.user_email,))
            row = cur.fetchone()
            cur.close()

        if row:
            stored_hashed_pw = row["hashed_password"]

            # Verify hashed password
            if verify_password(user.password, stored_hashed_pw):
                return {"Exist": True, "user": row}
            else:
                return {"Exist": False}
        return {"Exist": False}

    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
