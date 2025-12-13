# API Rate Limiting - Implementation Guide

## ✅ What Was Implemented

Rate limiting has been successfully added to protect your API from abuse and brute force attacks!

## 🛡️ Rate Limits Applied

### Critical Endpoints (Strict Limits):

- **Login**: `10/minute` per IP - Prevents brute force attacks
- **User Registration**: `5/minute` per IP - Prevents spam accounts
- **PDF MCQ Generation**: `5/hour` per IP - Resource-intensive operation

### Standard Endpoints (Moderate Limits):

- **GET Requests** (Quizzes, Questions, Answers, Submissions): `60/minute` per IP
- **POST/PUT Requests** (Create/Edit): `20-30/minute` per IP
- **DELETE Requests**: `10-20/minute` per IP - Prevents accidental mass deletion

## 📊 Rate Limit Details

| Endpoint Category | Rate Limit   | Reason              |
| ----------------- | ------------ | ------------------- |
| Login             | 10/minute    | Prevent brute force |
| Registration      | 5/minute     | Prevent spam        |
| PDF Processing    | 5/hour       | Resource intensive  |
| GET Operations    | 60/minute    | Normal usage        |
| Create/Edit       | 20-30/minute | Moderate operations |
| Delete            | 10-20/minute | Prevent abuse       |

## 🚀 How It Works

1. **IP-Based Limiting**: Rate limits are applied per IP address
2. **Automatic Tracking**: Uses in-memory storage (no database needed)
3. **Error Response**: Returns `429 Too Many Requests` when limit exceeded
4. **Reset Timer**: Limits reset after the time window expires

## 📝 Response When Limit Exceeded

When a rate limit is exceeded, the API returns:

```json
{
  "error": "Rate limit exceeded: 10 per 1 minute"
}
```

HTTP Status Code: **429 Too Many Requests**

## 🔧 Installation

Rate limiting is already set up! Just install the dependency:

```bash
cd Backend
pip install slowapi
```

Then restart your server:

```bash
uvicorn app.main:app --reload
```

## ⚙️ Configuration

Rate limits are hardcoded in the router files. To change them, edit the decorator:

```python
@limiter.limit("10/minute")  # Change this value
def your_endpoint(request: Request, ...):
    ...
```

### Common Rate Limit Formats:

- `"10/minute"` - 10 requests per minute
- `"100/hour"` - 100 requests per hour
- `"5/second"` - 5 requests per second
- `"1000/day"` - 1000 requests per day

## 🔍 Files Modified

1. **`Backend/app/rate_limiter.py`** - Centralized limiter configuration
2. **`Backend/app/main.py`** - Added limiter to FastAPI app
3. **All router files** - Added rate limit decorators to endpoints

## 🧪 Testing Rate Limits

You can test rate limiting by making rapid requests:

```bash
# Test login endpoint (10/minute limit)
for i in {1..15}; do
  curl -X POST http://localhost:8000/Users/Users/login \
    -d "username=test&password=test"
  echo "Request $i"
done
```

After 10 requests, you should see `429 Too Many Requests`.

## 💡 Best Practices

1. **Adjust Limits Based on Usage**: Monitor your API and adjust limits as needed
2. **User-Based Limiting** (Future): Consider user-based limits instead of just IP-based
3. **Redis for Production**: For production with multiple servers, use Redis backend:

   ```python
   from slowapi import Limiter
   from slowapi.middleware import SlowAPIMiddleware
   from slowapi.util import get_remote_address
   import redis

   redis_client = redis.Redis(host='localhost', port=6379, db=0)
   limiter = Limiter(
       key_func=get_remote_address,
       storage_uri="redis://localhost:6379"
   )
   ```

## 🎯 Benefits

✅ **Prevents Brute Force Attacks** - Login attempts limited  
✅ **Prevents Spam** - Registration limited  
✅ **Protects Resources** - Expensive operations (PDF processing) limited  
✅ **Prevents Abuse** - All endpoints have reasonable limits  
✅ **Better Security** - API is now more resilient to attacks

## 🔄 Next Steps (Optional Improvements)

1. **User-Based Limits**: Limit by user ID instead of just IP
2. **Redis Backend**: For distributed systems
3. **Dynamic Limits**: Adjust limits based on user tier/premium status
4. **Monitoring**: Log rate limit violations for analysis
5. **Custom Error Messages**: Provide helpful messages when limit exceeded

## 📚 Resources

- [SlowAPI Documentation](https://slowapi.readthedocs.io/)
- [FastAPI Rate Limiting Guide](https://fastapi.tiangolo.com/advanced/middleware/)

---

**Status**: ✅ Rate limiting is now active and protecting your API!
