import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from .config import (
    DATABASE_URL,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_MIN_CONNECTIONS,
    DB_MAX_CONNECTIONS,
)

DB_POOL: pool.SimpleConnectionPool | None = None

def init_connection_pool() -> None:
    global DB_POOL
    if DB_POOL is None:
        if DATABASE_URL:
            # Use DATABASE_URL for Render PostgreSQL
            DB_POOL = pool.SimpleConnectionPool(
                minconn=DB_MIN_CONNECTIONS,
                maxconn=DB_MAX_CONNECTIONS,
                dsn=DATABASE_URL,
            )
        else:
            # Use individual connection parameters for local development
            DB_POOL = pool.SimpleConnectionPool(
                minconn=DB_MIN_CONNECTIONS,
                maxconn=DB_MAX_CONNECTIONS,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
            )

@contextmanager
def get_db_connection():
    """Yield a database connection from the pool and return it after use."""
    if DB_POOL is None:
        init_connection_pool()

    assert DB_POOL is not None
    conn = DB_POOL.getconn()
    try:
        yield conn
    finally:
        DB_POOL.putconn(conn)

try:
    with get_db_connection() as conn:
        if DATABASE_URL:
            print(f"✅ Successfully connected to Render PostgreSQL database")
        else:
            print(f"✅ Successfully connected to database: {DB_NAME}")
except psycopg2.OperationalError as e:
    print("\n" + "=" * 70)
    print("❌ DATABASE CONNECTION FAILED!")
    print("=" * 70)
    print(f"Error: {str(e)}")
    print("\n💡 SOLUTION:")
    if DATABASE_URL:
        print("   Render DATABASE_URL is set but connection failed.")
        print("   Check if your Render PostgreSQL database is running and accessible.")
    else:
        print("   1. Create a file named '.env' in the Backend folder")
        print("   2. Add your database credentials:")
        print(f"      DB_NAME={DB_NAME}")
        print(f"      DB_USER={DB_USER}")
        print(f"      DB_PASSWORD=YOUR_ACTUAL_POSTGRES_PASSWORD")
        print(f"      DB_HOST={DB_HOST}")
        print(f"      DB_PORT={DB_PORT}")
        print("\n   Example .env file content:")
        print("   DB_NAME=QuizApp")
        print("   DB_USER=postgres")
        print("   DB_PASSWORD=your_actual_password")
        print("   DB_HOST=localhost")
        print("   DB_PORT=5432")
    print("=" * 70 + "\n")
    raise
