from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .database import get_db_connection
import psycopg2.extras
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT settings - Get from environment variable
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "PROJECT")  # ⚠️ Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))

# Password hashing
# Use only bcrypt to avoid compatibility issues
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 (token will be provided via /login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Users/login")


# -------------------
# Utility functions
# -------------------
def verify_password(plain_password, hashed_password: str) -> bool:
    """Check if plain password matches the hashed password"""
    # Handle plain text passwords (legacy data)
    if not hashed_password.startswith('$2b$') and not hashed_password.startswith('$2a$'):
        # Plain text password - direct comparison
        return plain_password == hashed_password
    
    # Truncate password to 72 bytes if longer (bcrypt limitation)
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"❌ Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hash a password before storing in DB"""
    # Truncate password to 72 bytes if longer (bcrypt limitation)
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', errors='ignore')
        print(f"⚠️ Password truncated from {len(password_bytes)} to 72 bytes")
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"❌ Hashing error: {e}")
        raise


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """Decode and validate JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# -------------------
# Database Integration
# -------------------
def get_user_from_db(email: str):
    """Fetch user by email from PostgreSQL"""
    with get_db_connection() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM users WHERE user_email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        return user


def authenticate_user(email: str, password: str):
    """Check email + password against DB"""
    user = get_user_from_db(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


# -------------------
# Dependency for protected routes
# -------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    user = get_user_from_db(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
