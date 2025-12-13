# CORS Configuration Guide

## ✅ What Was Implemented

CORS (Cross-Origin Resource Sharing) is now configurable via environment variables, making it easy to configure for both development and production environments!

## 🔒 Security Improvements

### Before:

- Hardcoded to `localhost:5173`
- Not configurable for production
- No environment-based settings

### After:

- ✅ Configurable via environment variables
- ✅ Production-safe (blocks wildcard in production)
- ✅ Supports multiple origins (comma-separated)
- ✅ Environment-aware (development vs production)

## ⚙️ Configuration

### Development Setup

In your `.env` file:

```env
# Development (default)
CORS_ORIGINS=http://localhost:5173
ENVIRONMENT=development
```

### Production Setup

In your production `.env` file:

```env
# Production - Specify your actual domains
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://app.yourdomain.com
ENVIRONMENT=production
```

**Multiple Origins:** Separate with commas (no spaces around commas)

## 📋 Environment Variables

| Variable       | Description                       | Default                 | Example                                       |
| -------------- | --------------------------------- | ----------------------- | --------------------------------------------- |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | `http://localhost:5173` | `https://example.com,https://www.example.com` |
| `ENVIRONMENT`  | Environment type                  | `development`           | `production`                                  |

## 🔐 Security Features

### Production Protection

When `ENVIRONMENT=production`, the system will:

- ✅ **Block wildcard (`*`)** - Prevents allowing all origins
- ✅ **Require explicit origins** - Must specify actual domains
- ✅ **Fail to start** if misconfigured - Prevents accidental insecure deployment

### Development Mode

When `ENVIRONMENT=development`:

- ✅ Allows `localhost` origins
- ✅ More lenient (but still secure)
- ✅ Easy local testing

## 🚀 Quick Setup

### Step 1: Update Your `.env` File

For **development** (already set):

```env
CORS_ORIGINS=http://localhost:5173
ENVIRONMENT=development
```

For **production**:

```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ENVIRONMENT=production
```

### Step 2: Restart Server

```bash
cd Backend
uvicorn app.main:app --reload
```

## 📝 Allowed HTTP Methods

The following methods are explicitly allowed:

- `GET` - Retrieve data
- `POST` - Create data
- `PUT` - Update data
- `DELETE` - Delete data
- `OPTIONS` - Preflight requests

## 🔍 How It Works

1. **Reads Environment Variables**: Checks `.env` file for `CORS_ORIGINS`
2. **Parses Origins**: Splits comma-separated origins into a list
3. **Production Check**: In production, validates no wildcard is used
4. **Applies Middleware**: Configures FastAPI CORS middleware

## ⚠️ Common Mistakes to Avoid

### ❌ DON'T Do This in Production:

```env
# WRONG - Wildcard in production
CORS_ORIGINS=*
ENVIRONMENT=production

# WRONG - Empty in production
CORS_ORIGINS=
ENVIRONMENT=production
```

### ✅ DO This in Production:

```env
# CORRECT - Explicit domains
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ENVIRONMENT=production
```

## 🧪 Testing CORS

### Test from Browser Console:

```javascript
fetch("http://localhost:8000/Quizzes/Quizzes/getQuizzes", {
  method: "GET",
  credentials: "include",
})
  .then((res) => res.json())
  .then((data) => console.log(data))
  .catch((err) => console.error("CORS Error:", err));
```

### Test with cURL:

```bash
curl -X GET http://localhost:8000/Quizzes/Quizzes/getQuizzes \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: GET" \
  -v
```

## 📊 CORS Headers Explained

When a request is made from an allowed origin, the server responds with:

```
Access-Control-Allow-Origin: https://yourdomain.com
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: *
```

## 🔄 Multiple Environments

### Local Development:

```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
ENVIRONMENT=development
```

### Staging:

```env
CORS_ORIGINS=https://staging.yourdomain.com
ENVIRONMENT=production
```

### Production:

```env
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ENVIRONMENT=production
```

## 🛡️ Security Best Practices

1. **Never Use Wildcard in Production**: Always specify exact domains
2. **Use HTTPS in Production**: Only allow HTTPS origins
3. **Limit Origins**: Only include domains that actually need access
4. **Review Regularly**: Periodically review allowed origins
5. **Environment Separation**: Use different `.env` files for dev/staging/prod

## 🔧 Troubleshooting

### Error: "CORS_ORIGINS must be explicitly set"

**Problem**: Production environment detected but CORS misconfigured

**Solution**: Set `CORS_ORIGINS` with actual domain names (no wildcards)

### Error: "CORS policy blocked"

**Problem**: Frontend domain not in allowed origins

**Solution**: Add your frontend domain to `CORS_ORIGINS` in `.env`

### Frontend Can't Connect

**Check:**

1. Is your frontend URL in `CORS_ORIGINS`?
2. Is the server restarted after `.env` changes?
3. Are you using the correct protocol (http vs https)?

## 📚 Additional Resources

- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [FastAPI CORS Documentation](https://fastapi.tiangolo.com/tutorial/cors/)

## ✅ Checklist for Production Deployment

- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Set `CORS_ORIGINS` to your actual production domains
- [ ] Verify no wildcards (`*`) in `CORS_ORIGINS`
- [ ] Use HTTPS URLs only
- [ ] Test CORS with actual frontend
- [ ] Review allowed origins regularly

---

**Status**: ✅ CORS is now production-ready and configurable!
