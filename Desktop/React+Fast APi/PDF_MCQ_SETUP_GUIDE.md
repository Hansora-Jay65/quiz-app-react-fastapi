# PDF to MCQ Generator - Setup Guide

## Overview

This feature allows you to automatically generate Multiple Choice Questions (MCQs) from PDF files using AI. The system extracts text from PDFs and uses OpenAI's API to generate relevant questions.

## Prerequisites

1. **OpenAI API Key**: You need an OpenAI API account and API key
   - Sign up at: https://platform.openai.com/
   - Get your API key from: https://platform.openai.com/api-keys
   - Note: OpenAI API usage is paid (pay-as-you-go)

## Installation Steps

### 1. Install Backend Dependencies

Navigate to the Backend directory and install the new dependencies:

```bash
cd Backend
pip install -r requirements.txt
```

This will install:

- `python-multipart` - For file uploads
- `PyPDF2` - For PDF text extraction
- `openai` - For AI-powered MCQ generation
- `python-jose[cryptography]` - Already needed for JWT
- `passlib[bcrypt]` - Already needed for password hashing

### 2. Set Up OpenAI API Key

You have two options:

#### Option A: Environment Variable (Recommended)

Set the environment variable before running the server:

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY="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"
```

**Windows (Command Prompt):**

```cmd
set OPENAI_API_KEY=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
```

**Linux/Mac:**

```bash
export OPENAI_API_KEY="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"
```

#### Option B: Direct Configuration

Edit `Backend/app/services/PDF_MCQ_Services.py` and replace:

```python
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "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"))
```

with:

```python
client = OpenAI(api_key="your-actual-api-key-here")
```

⚠️ **Warning**: Option B is less secure. Use environment variables in production.

### 3. Start the Backend Server

```bash
cd Backend
uvicorn app.main:app --reload
```

### 4. Start the Frontend

```bash
cd frontend
npm install  # If you haven't already
npm run dev
```

## How to Use

1. **Navigate to PDF MCQ Generator**

   - Click on "PDF MCQ Generator" in the navbar
   - Or go to: `http://localhost:5173/pdf-mcq-generator`

2. **Upload PDF File**

   - Click "Select PDF File" and choose your PDF
   - Set the number of questions you want (1-20)

3. **Choose Mode**

   - **Generate MCQs Only**: Just generates questions without creating a quiz
   - **Generate & Create Quiz**: Generates questions and automatically creates a quiz in the system

4. **If Creating Quiz**

   - Enter Quiz Title
   - Enter Creator Name
   - Click "Generate & Create Quiz"

5. **Review Results**
   - View generated questions with correct answers marked
   - If quiz was created, you'll be redirected to the quiz list

## Features

- ✅ Automatic text extraction from PDF
- ✅ AI-powered question generation
- ✅ Multiple choice questions with 4 options
- ✅ Automatic correct answer identification
- ✅ Direct quiz creation integration
- ✅ Preview generated questions before saving

## Cost Considerations

- OpenAI API charges based on usage
- GPT-3.5-turbo is cheaper (~$0.0015 per 1K tokens)
- GPT-4 is more expensive but higher quality (~$0.03 per 1K tokens)
- Current implementation uses GPT-3.5-turbo
- To use GPT-4, edit `Backend/app/services/PDF_MCQ_Services.py` and change:
  ```python
  model="gpt-3.5-turbo"  # Change to "gpt-4"
  ```

## Troubleshooting

### "OpenAI API key not configured"

- Make sure you've set the OPENAI_API_KEY environment variable
- Restart the backend server after setting the variable

### "Failed to extract text from PDF"

- Ensure the PDF is not password-protected
- Check if the PDF contains actual text (not just images)
- Try a different PDF file

### "Failed to parse AI response"

- The AI might return malformed JSON
- Try reducing the number of questions
- Check OpenAI API status: https://status.openai.com/

### File Upload Issues

- Ensure file size is reasonable (< 10MB recommended)
- Check that the file is a valid PDF

## Alternative AI Providers

If you want to use a different AI provider (e.g., Anthropic Claude, Google Gemini), you'll need to:

1. Install the provider's SDK
2. Modify `Backend/app/services/PDF_MCQ_Services.py`
3. Update the `generate_mcqs_from_text()` function

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Consider rate limiting for production use
- Validate file uploads (size, type, content)
