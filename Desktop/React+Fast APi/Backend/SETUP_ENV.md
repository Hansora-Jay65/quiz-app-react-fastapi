# Quick Setup Guide - Database Connection

## Problem: Database Connection Failed

If you see this error:

```
psycopg2.OperationalError: password authentication failed
```

## Solution: Create .env File

### Step 1: Create .env file

Create a file named `.env` in the `Backend` folder with this content:

```env
# Database Configuration
DB_NAME=QuizApp
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD_HERE
DB_HOST=localhost
DB_PORT=5432

# JWT Configuration
JWT_SECRET_KEY=your_very_strong_secret_key_here
JWT_EXPIRES_MINUTES=60

# AI Provider (for PDF MCQ generation)
AI_PROVIDER=simple

# CORS Configuration
# Development: http://localhost:5173
# Production: https://yourdomain.com,https://www.yourdomain.com (comma-separated)
CORS_ORIGINS=http://localhost:5173
ENVIRONMENT=development

# Rate Limiting (Optional - uses defaults if not set)
# RATE_LIMIT_ENABLED=true
# RATE_LIMIT_PER_MINUTE=60
```

### Step 2: Replace YOUR_POSTGRES_PASSWORD_HERE

Replace `YOUR_POSTGRES_PASSWORD_HERE` with your actual PostgreSQL password.

**How to find your PostgreSQL password:**

- If you set it during installation, use that password
- If you forgot it, you may need to reset it in PostgreSQL
- Default might be: `postgres`, `admin`, or what you set during install

### Step 3: Generate a Strong JWT Secret Key (Optional but Recommended)

Run this command to generate a secure key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and paste it as `JWT_SECRET_KEY` in your `.env` file.

### Step 4: Restart Your Server

```bash
cd Backend
uvicorn app.main:app --reload
```

## File Location

Make sure your `.env` file is here:

```
Backend/
  ├── .env          ← Create this file here
  ├── app/
  ├── requirements.txt
  └── ...
```

## Need to Reset PostgreSQL Password?

If you need to reset your PostgreSQL password:

1. **Windows:** Open Services, find PostgreSQL, stop it, then reset password in pgAdmin or command line
2. **Or:** Connect to PostgreSQL and run:
   ```sql
   ALTER USER postgres WITH PASSWORD 'new_password';
   ```

Then update your `.env` file with the new password.

## Verify Connection

After creating `.env` and restarting, you should see:

```
✅ Successfully connected to database: QuizApp
```

If you still see errors, check:

- ✅ `.env` file exists in `Backend` folder
- ✅ Password is correct
- ✅ PostgreSQL is running
- ✅ Database `QuizApp` exists
