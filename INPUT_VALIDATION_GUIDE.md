# Input Validation & Sanitization Guide

## ✅ What Was Implemented

Comprehensive input validation and sanitization has been added to protect your API from malicious inputs, XSS attacks, and invalid data!

## 🛡️ Security Features Added

### 1. **Input Sanitization**

- ✅ HTML/XSS protection - Escapes HTML entities
- ✅ String length limits - Prevents buffer overflow
- ✅ Null byte removal - Prevents injection attacks
- ✅ Whitespace trimming - Clean data

### 2. **File Upload Validation**

- ✅ File type validation - Checks PDF magic bytes
- ✅ File size limits - Maximum 10MB for PDFs
- ✅ Filename sanitization - Prevents path traversal
- ✅ Content verification - Validates actual file content

### 3. **Password Strength Validation**

- ✅ Minimum 8 characters
- ✅ At least one uppercase letter
- ✅ At least one lowercase letter
- ✅ At least one number
- ✅ Maximum 128 characters

### 4. **Email Validation**

- ✅ Format validation with regex
- ✅ Length limits (max 255 characters)
- ✅ Case normalization (lowercase)

### 5. **Text Input Validation**

- ✅ Quiz titles - 3-200 characters, sanitized
- ✅ Creator names - 2-100 characters, alphanumeric + safe punctuation
- ✅ Question text - 10-1000 characters, sanitized
- ✅ Answer text - 1-500 characters, sanitized

## 📋 Validation Functions

### File Validation

```python
validate_pdf_file(file_content: bytes, filename: str)
# Validates: file extension, size (max 10MB), PDF magic bytes
```

### Password Validation

```python
validate_password_strength(password: str)
# Validates: length, uppercase, lowercase, numbers
```

### Email Validation

```python
validate_email(email: str)
# Validates: format, length, normalizes to lowercase
```

### Text Sanitization

```python
sanitize_quiz_title(title: str)
sanitize_creator_name(name: str)
validate_question_text(text: str)
validate_answer_text(text: str)
```

## 🔍 Where Validation is Applied

### User Registration (`/Users/Users/createUser`)

- ✅ Email format and length validation
- ✅ Password strength validation
- ✅ HTML sanitization

### PDF Upload (`/PDF_MCQ/generate-mcqs`)

- ✅ File type validation (PDF only)
- ✅ File size validation (max 10MB)
- ✅ PDF magic bytes verification
- ✅ Number of questions validation (1-50)
- ✅ Quiz title and creator name sanitization

### Quiz Creation (`/Quizzes/Quizzes/createQuiz`)

- ✅ Quiz title validation and sanitization
- ✅ Creator name validation and sanitization

### Question Creation (`/Questions/Questions/createQuestion`)

- ✅ Question text validation and sanitization
- ✅ Length validation (10-1000 characters)

### Answer Creation (`/Answers/Answers/createAnswer`)

- ✅ Answer text validation and sanitization
- ✅ Length validation (1-500 characters)

## 🚨 Error Responses

When validation fails, the API returns clear error messages:

```json
{
  "detail": "Password must be at least 8 characters long"
}
```

```json
{
  "detail": "File size exceeds maximum allowed size of 10MB"
}
```

```json
{
  "detail": "Invalid PDF file format. File does not appear to be a valid PDF."
}
```

## 📦 Dependencies Added

- `bleach` - For advanced HTML sanitization (optional, can be enhanced)

## 🔧 Installation

Install the new dependency:

```bash
cd Backend
pip install bleach
```

Then restart your server:

```bash
uvicorn app.main:app --reload
```

## 🛠️ Files Created/Modified

### New Files:

1. **`Backend/app/utils/validation.py`** - All validation utilities

### Modified Files:

1. **`Backend/app/routers/User_routers.py`** - Added email & password validation
2. **`Backend/app/routers/PDF_MCQ_routers.py`** - Added file validation
3. **`Backend/app/routers/Quiz_routers.py`** - Added title & creator validation
4. **`Backend/app/routers/Question_routers.py`** - Added question text validation
5. **`Backend/app/routers/Answer_routers.py`** - Added answer text validation
6. **`Backend/requirements.txt`** - Added `bleach` dependency

## 🧪 Testing Validation

### Test Password Strength:

```bash
curl -X POST http://localhost:8000/Users/Users/createUser \
  -H "Content-Type: application/json" \
  -d '{"user_email": "test@test.com", "hashed_password": "weak"}'
# Should return: "Password must be at least 8 characters long"
```

### Test PDF Validation:

```bash
# Try uploading a non-PDF file
# Should return: "Only PDF files are supported"

# Try uploading a file > 10MB
# Should return: "File size exceeds maximum allowed size of 10MB"
```

### Test Email Validation:

```bash
curl -X POST http://localhost:8000/Users/Users/createUser \
  -H "Content-Type: application/json" \
  -d '{"user_email": "invalid-email", "hashed_password": "ValidPass123"}'
# Should return: "Invalid email format"
```

## 🎯 Security Benefits

✅ **XSS Protection** - HTML entities are escaped  
✅ **SQL Injection Protection** - Already using parameterized queries ✅  
✅ **File Upload Security** - Validates file type, size, and content  
✅ **Input Length Limits** - Prevents buffer overflow attacks  
✅ **Password Security** - Enforces strong passwords  
✅ **Data Integrity** - Ensures valid data format

## 🔄 Future Enhancements (Optional)

1. **Advanced HTML Sanitization**: Use `bleach` library for whitelist-based sanitization
2. **File Content Scanning**: Scan uploaded files for malware
3. **Rate Limiting Per Validation**: Different limits for different validation failures
4. **Custom Validation Rules**: Allow admins to configure validation rules
5. **Validation Logging**: Log validation failures for security monitoring

## 📚 Best Practices

1. **Always Validate on Server**: Client-side validation can be bypassed
2. **Sanitize Before Storing**: Clean data before saving to database
3. **Validate File Content**: Don't trust file extensions alone
4. **Set Reasonable Limits**: Balance security with usability
5. **Provide Clear Errors**: Help users understand what went wrong

## ⚠️ Important Notes

- **SQL Injection**: Already protected ✅ (using parameterized queries)
- **XSS**: Protected via HTML escaping
- **File Upload**: Validated for type, size, and content
- **Password**: Enforced strength requirements
- **All Inputs**: Sanitized and validated

---

**Status**: ✅ Input validation and sanitization is now active and protecting your API!
