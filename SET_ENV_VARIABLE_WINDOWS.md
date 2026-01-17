# How to Set Environment Variables on Windows

## Quick Fix: The API key is already in your code, but let's set it properly

Since you're on Windows, here are the methods to set the environment variable:

## Method 1: PowerShell (Temporary - Current Session Only)

Open PowerShell and run:

```powershell
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
```

Then start your backend server in the SAME PowerShell window:
```powershell
cd Backend
uvicorn app.main:app --reload
```

⚠️ **Note**: This only works for the current PowerShell session. If you close PowerShell, you'll need to set it again.

---

## Method 2: Command Prompt (Temporary - Current Session Only)

Open Command Prompt (cmd) and run:

```cmd
set OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
```

Then start your backend server in the SAME Command Prompt window:
```cmd
cd Backend
uvicorn app.main:app --reload
```

⚠️ **Note**: This only works for the current Command Prompt session.

---

## Method 3: Permanent Setup (Recommended)

### Using Windows GUI:

1. **Press `Win + R`** to open Run dialog
2. Type `sysdm.cpl` and press Enter
3. Click the **"Advanced"** tab
4. Click **"Environment Variables"** button
5. Under **"User variables"** (or "System variables" for all users), click **"New"**
6. Variable name: `OPENAI_API_KEY`
7. Variable value: `YOUR_OPENAI_API_KEY_HERE`
8. Click **"OK"** on all dialogs
9. **Restart your terminal/IDE** for changes to take effect

### Using PowerShell (Permanent):

Run PowerShell as Administrator and execute:

```powershell
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'YOUR_OPENAI_API_KEY_HERE', 'User')
```

Then restart your terminal.

---

## Method 4: Create a .env File (Alternative - Requires python-dotenv)

If you prefer using a `.env` file:

1. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

2. Create a `.env` file in the `Backend` folder:
   ```
   OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
   ```

3. Update `Backend/app/services/PDF_MCQ_Services.py` to load from .env:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

---

## Verify Environment Variable is Set

To check if the variable is set correctly, run in PowerShell:

```powershell
echo $env:OPENAI_API_KEY
```

Or in Command Prompt:
```cmd
echo %OPENAI_API_KEY%
```

---

## Quick Start (Recommended for Testing)

**Easiest method for now:**

1. Open PowerShell
2. Run:
   ```powershell
   $env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
   ```
3. Navigate to Backend folder:
   ```powershell
   cd Backend
   ```
4. Start server:
   ```powershell
   uvicorn app.main:app --reload
   ```

The server should now work with the API key!

---

## Important Security Note

⚠️ **Never commit your API key to version control (Git)**. The API key in your code should be removed and only set via environment variables in production.

