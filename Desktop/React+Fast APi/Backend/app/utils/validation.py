"""
Input Validation and Sanitization Utilities
Provides functions for validating and sanitizing user inputs
"""

import re
import html
from typing import Optional
from fastapi import HTTPException

# Optional: import magic for advanced file type detection
# Requires: pip install python-magic-bin (Windows) or python-magic (Linux/Mac)


def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize string input by:
    - Stripping whitespace
    - Escaping HTML entities
    - Limiting length
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    # Strip whitespace
    text = text.strip()

    # Escape HTML to prevent XSS
    text = html.escape(text)

    # Limit length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]

    return text


def sanitize_text_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize text input (for questions, answers, etc.)
    Allows some formatting but prevents XSS
    """
    if not text:
        return ""

    # Remove null bytes
    text = text.replace("\x00", "")

    # Strip whitespace
    text = text.strip()

    # Basic HTML escaping (but allow some safe characters)
    # This is a simple approach - for production, consider using bleach library
    text = html.escape(text)

    # Limit length
    if len(text) > max_length:
        text = text[:max_length]

    return text


def validate_email(email: str) -> str:
    """
    Validate and sanitize email address
    """
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    email = email.strip().lower()

    # Basic email validation regex
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(email_pattern, email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Check length
    if len(email) > 255:
        raise HTTPException(status_code=400, detail="Email address too long")

    return email


def validate_password_strength(password: str) -> str:
    """
    Validate password strength
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    """
    if not password:
        raise HTTPException(status_code=400, detail="Password is required")

    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long"
        )

    if len(password) > 128:
        raise HTTPException(
            status_code=400, detail="Password is too long (maximum 128 characters)"
        )

    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter",
        )

    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one lowercase letter",
        )

    # Check for at least one number
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one number"
        )

    return password


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal and other attacks
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    # Remove path components
    filename = filename.replace("\\", "").replace("/", "").replace("..", "")

    # Remove null bytes
    filename = filename.replace("\x00", "")

    # Limit length
    if len(filename) > 255:
        filename = filename[:255]

    # Only allow alphanumeric, dots, dashes, and underscores
    filename = re.sub(r"[^a-zA-Z0-9._-]", "", filename)

    return filename


def validate_file_size(file_size: int, max_size_mb: int = 10) -> None:
    """
    Validate file size
    max_size_mb: Maximum file size in megabytes
    """
    max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes

    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {max_size_mb}MB",
        )

    if file_size == 0:
        raise HTTPException(status_code=400, detail="File is empty")


def validate_pdf_file(file_content: bytes, filename: str) -> None:
    """
    Validate PDF file:
    - Check file extension
    - Check file size
    - Verify PDF magic bytes
    """
    # Check filename extension
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Check file size (max 10MB)
    validate_file_size(len(file_content), max_size_mb=10)

    # Check PDF magic bytes (PDF files start with %PDF)
    if not file_content.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file format. File does not appear to be a valid PDF.",
        )

    # Additional check: PDF should have version number after %PDF
    if len(file_content) < 8:
        raise HTTPException(
            status_code=400, detail="File is too small to be a valid PDF"
        )


def sanitize_quiz_title(title: str) -> str:
    """
    Sanitize quiz title
    """
    if not title:
        raise HTTPException(status_code=400, detail="Quiz title is required")

    title = sanitize_string(title, max_length=200)

    if len(title.strip()) < 3:
        raise HTTPException(
            status_code=400, detail="Quiz title must be at least 3 characters long"
        )

    return title


def sanitize_creator_name(name: str) -> str:
    """
    Sanitize creator name
    """
    if not name:
        raise HTTPException(status_code=400, detail="Creator name is required")

    name = sanitize_string(name, max_length=100)

    if len(name.strip()) < 2:
        raise HTTPException(
            status_code=400, detail="Creator name must be at least 2 characters long"
        )

    # Only allow alphanumeric, spaces, and common punctuation
    if not re.match(r"^[a-zA-Z0-9\s\.,\-_]+$", name):
        raise HTTPException(
            status_code=400, detail="Creator name contains invalid characters"
        )

    return name


def validate_question_text(text: str) -> str:
    """
    Validate and sanitize question text
    """
    if not text:
        raise HTTPException(status_code=400, detail="Question text is required")

    text = sanitize_text_input(text, max_length=1000)

    if len(text.strip()) < 10:
        raise HTTPException(
            status_code=400, detail="Question text must be at least 10 characters long"
        )

    return text


def validate_answer_text(text: str) -> str:
    """
    Validate and sanitize answer text
    """
    if not text:
        raise HTTPException(status_code=400, detail="Answer text is required")

    text = sanitize_text_input(text, max_length=500)

    if len(text.strip()) < 1:
        raise HTTPException(status_code=400, detail="Answer text cannot be empty")

    return text


def validate_num_questions(num: int) -> int:
    """
    Validate number of questions
    """
    if not isinstance(num, int):
        raise HTTPException(
            status_code=400, detail="Number of questions must be an integer"
        )

    if num < 1:
        raise HTTPException(
            status_code=400, detail="Number of questions must be at least 1"
        )

    if num > 50:
        raise HTTPException(
            status_code=400, detail="Number of questions cannot exceed 50"
        )

    return num
