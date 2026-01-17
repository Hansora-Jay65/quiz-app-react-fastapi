# Render Deployment Guide

This guide will help you deploy your Quiz App to Render with PostgreSQL database.

## 🚀 Quick Setup

### 1. Push to GitHub
Make sure your latest changes are pushed to GitHub:
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Connect to Render
1. Go to [render.com](https://render.com)
2. Sign up or log in
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Select the `quiz-app-react-fastapi` repository
6. Choose the "Python" environment

### 3. Configure Environment Variables
Add these environment variables in your Render dashboard:

**Backend Service:**
- `DATABASE_URL`: (Auto-populated by Render PostgreSQL)
- `ENVIRONMENT`: `production`
- `CORS_ORIGINS`: `https://your-frontend-url.onrender.com`
- `JWT_SECRET_KEY`: (Generate or use existing)
- `JWT_EXPIRES_MINUTES`: `60`
- `OPENAI_API_KEY`: (Your OpenAI API key)

**Frontend Service:**
- `VITE_API_URL`: `https://your-backend-url.onrender.com`

### 4. Database Setup
1. In Render dashboard, go to "New +" → "PostgreSQL"
2. Name: `quiz-db`
3. Database Name: `quizapp`
4. User: `quizapp_user`
5. Plan: Starter
6. Region: Oregon (or closest to you)
7. Click "Create Database"

### 5. Initialize Database
After deployment, run the database initialization:

**Option A: Using Render Shell (Recommended)**
1. Go to your backend service on Render
2. Click "Shell" tab
3. Run: `python init_render_db.py`

**Option B: Manual Setup**
1. Connect to your database using pgAdmin or DBeaver
2. Run the SQL commands from `init_render_db.py`

## 📋 render.yaml Configuration

Your `render.yaml` includes:

### Backend Service
- **Build**: Installs Python dependencies from `Backend/requirements.txt`
- **Start**: Runs FastAPI with uvicorn
- **Health Check**: `/` endpoint

### Frontend Service
- **Build**: Runs `npm install && npm run build`
- **Static**: Serves built React app from `frontend/dist`
- **Routes**: SPA routing support

### Database
- **Type**: PostgreSQL
- **Name**: quizapp
- **Tables**: Automatically created on first run

## 🔧 Database Schema

The initialization script creates these tables:

```sql
users (user_id, user_email, hashed_password, created_at)
quizzes (quiz_id, quiz_title, created_by, created_at)
questions (question_id, quiz_id, question_text)
answers (answer_id, question_id, answer_text, is_correct)
submissions (submission_id, user_id, quiz_id, score, submitted_at)
user_answers (user_answer_id, submission_id, question_id, answer_id)
```

## 🌐 Access URLs

After deployment:
- **Backend**: `https://quiz-backend.onrender.com`
- **Frontend**: `https://quiz-frontend.onrender.com`
- **Database**: Available in Render dashboard

## 🔄 Updating Your App

To update after deployment:

1. **Code Changes**:
   ```bash
   git add .
   git commit -m "Update: Your changes"
   git push origin main
   ```

2. **Database Changes**:
   - Modify `init_render_db.py` for schema changes
   - Run initialization script again

## 🛠️ Troubleshooting

### Common Issues:

**1. CORS Errors**
- Make sure `CORS_ORIGINS` includes your frontend URL
- Check both backend and frontend environment variables

**2. Database Connection**
- Verify `DATABASE_URL` is correctly set
- Check database name: `quizapp`
- Ensure tables exist (run initialization script)

**3. Build Failures**
- Check `Backend/requirements.txt` has all dependencies
- Verify `package.json` scripts are correct
- Check build logs in Render dashboard

**4. Authentication Issues**
- Ensure `JWT_SECRET_KEY` is set
- Check password hashing compatibility
- Verify token expiration settings

## 📊 Monitoring

Monitor your deployment:
- **Render Dashboard**: Logs, metrics, error tracking
- **Database**: Query performance, storage usage
- **Analytics**: User activity, error rates

## 🔒 Security Notes

- Change default admin password after first login
- Use strong `JWT_SECRET_KEY` in production
- Restrict database IP access in production
- Enable SSL (automatic on Render)
- Monitor for suspicious activity

## 🎯 Production Checklist

Before going live:
- [ ] All environment variables set
- [ ] Database initialized with tables
- [ ] CORS properly configured
- [ ] Test user registration/login
- [ ] Test quiz creation/functionality
- [ ] Check all API endpoints
- [ ] Verify frontend-backend communication
- [ ] Set up monitoring/alerts

## 🆘 Migration from Local

To migrate your local data:
1. Export local data (users, quizzes, etc.)
2. Transform data to match new schema
3. Import using Render shell or database client
4. Test thoroughly after migration

## 📞 Support

- **Render Docs**: https://render.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://reactjs.org/docs/
