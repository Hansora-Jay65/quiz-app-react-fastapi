import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in Backend directory
BASE_DIR = Path(__file__).parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Environment / logging
ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development").lower()
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

# Database configuration
# For Render, use DATABASE_URL environment variable
DATABASE_URL: str = os.getenv("DATABASE_URL", "")

# Fallback to individual DB vars for local development
if DATABASE_URL:
    # Parse DATABASE_URL for Render PostgreSQL
    import urllib.parse
    parsed = urllib.parse.urlparse(DATABASE_URL)
    DB_NAME = parsed.path[1:]  # Remove leading slash
    DB_USER = parsed.username
    DB_PASSWORD = parsed.password
    DB_HOST = parsed.hostname
    DB_PORT = str(parsed.port or 5432)
else:
    # Local development configuration
    DB_NAME: str = os.getenv("DB_NAME", "QuizApp")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "1234")  # Default for local dev only
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

# Connection pool settings
DB_MIN_CONNECTIONS: int = int(os.getenv("DB_MIN_CONNECTIONS", "1"))
DB_MAX_CONNECTIONS: int = int(os.getenv("DB_MAX_CONNECTIONS", "10"))

# JWT configuration
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "PROJECT")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_MINUTES: int = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))
