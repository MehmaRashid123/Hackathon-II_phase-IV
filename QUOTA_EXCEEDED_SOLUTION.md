# Gemini API Quota Exceeded - Solutions

**Date**: February 9, 2026  
**Issue**: 429 Quota Exceeded Error  
**Status**: ⚠️ API Quota Exhausted

## Problem

The Gemini API is returning a 429 error:

```
429 You exceeded your current quota, please check your plan and billing details.
Quota exceeded for metric: generate_content_free_tier_requests, limit: 0
Please retry in 42 seconds
```

## What This Means

The free tier quota for the Gemini API has been exhausted. This can happen due to:
1. **Too many requests** - Exceeded daily/hourly limits
2. **Rate limiting** - Too many requests per minute
3. **Token limits** - Exceeded input token count

## Gemini Free Tier Limits

### Per Minute Limits
- **Requests**: 15 requests per minute
- **Tokens**: 1 million tokens per minute

### Per Day Limits
- **Requests**: 1,500 requests per day
- **Tokens**: 1 million tokens per day

## Solutions

### Solution 1: Wait and Retry ⏰
The error says "retry in 42 seconds". Just wait a minute and try again.

**Steps**:
1. Wait 1-2 minutes
2. Refresh the page
3. Try sending a message again

### Solution 2: Get a New API Key 🔑

**Steps**:
1. Go to: https://aistudio.google.com/app/apikey
2. Create a new API key
3. Update `backend/.env`:
   ```env
   GEMINI_API_KEY=YOUR_NEW_API_KEY
   ```
4. Restart backend

### Solution 3: Use a Different Model 🔄

Try a lighter model that might have separate quota:

**Option A: Gemini Flash Lite**
```env
GEMINI_MODEL=models/gemini-2.0-flash-lite
```

**Option B: Gemini 2.5 Flash Lite**
```env
GEMINI_MODEL=models/gemini-2.5-flash-lite
```

**Steps**:
1. Update `backend/.env` with new model
2. Restart backend
3. Try again

### Solution 4: Upgrade to Paid Plan 💳

For production use, consider upgrading:
- **Pay-as-you-go**: $0.00025 per 1K characters
- **Higher limits**: 1000 requests per minute
- **More tokens**: 4 million tokens per minute

**Link**: https://ai.google.dev/pricing

### Solution 5: Implement Rate Limiting 🚦

Add rate limiting to prevent quota exhaustion:

**In `backend/src/api/chat.py`**:
```python
from fastapi import HTTPException
from datetime import datetime, timedelta
import asyncio

# Simple rate limiter
last_request_time = {}
MIN_REQUEST_INTERVAL = 4  # seconds between requests

@router.post("/{user_id}/chat")
async def send_chat_message(user_id: str, request: ChatRequest):
    # Check rate limit
    now = datetime.now()
    if user_id in last_request_time:
        time_since_last = (now - last_request_time[user_id]).total_seconds()
        if time_since_last < MIN_REQUEST_INTERVAL:
            wait_time = MIN_REQUEST_INTERVAL - time_since_last
            raise HTTPException(
                status_code=429,
                detail=f"Please wait {wait_time:.1f} seconds before sending another message"
            )
    
    last_request_time[user_id] = now
    
    # Continue with normal processing...
```

### Solution 6: Use Mock Responses (Development) 🧪

For development/testing without API calls:

**Create `backend/src/agents/mock_assistant.py`**:
```python
class MockAssistant:
    async def process_message(self, message: str, context):
        # Return mock response
        return {
            "message": f"Mock response to: {message}",
            "tool_calls": []
        }
```

**Update `backend/.env`**:
```env
USE_MOCK_AI=true
```

## Check Your Quota Usage

### Google AI Studio
1. Go to: https://aistudio.google.com/
2. Click on your API key
3. View usage statistics
4. Check remaining quota

### Monitor in Code
Add logging to track requests:

```python
import logging
logger = logging.getLogger(__name__)

# Before API call
logger.info(f"Making Gemini API request for user {user_id}")

# After API call
logger.info(f"Gemini API request successful")
```

## Temporary Workaround

While waiting for quota reset, you can:

1. **Disable AI features temporarily**
2. **Use mock responses** for testing
3. **Wait for quota reset** (resets daily)
4. **Get a new API key** from different Google account

## Prevention Tips

### 1. Implement Caching
Cache common responses to reduce API calls:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(message: str):
    # Return cached response if available
    pass
```

### 2. Add Request Throttling
Limit requests per user:
```python
MAX_REQUESTS_PER_USER_PER_HOUR = 10
```

### 3. Optimize Prompts
- Keep system instructions concise
- Reduce token usage
- Use shorter messages

### 4. Monitor Usage
- Log all API calls
- Track quota usage
- Set up alerts

## Current Status

⚠️ **Quota Exceeded**: Free tier limit reached  
⏰ **Wait Time**: ~42 seconds (as per error)  
🔄 **Reset**: Daily quota resets at midnight UTC  
💡 **Recommendation**: Wait 1-2 minutes and try again  

## Quick Fix (Right Now)

**Option 1: Wait**
```bash
# Just wait 1-2 minutes
# Then try sending a message again
```

**Option 2: New API Key**
```bash
# Get new key from: https://aistudio.google.com/app/apikey
# Update backend/.env
# Restart backend
```

**Option 3: Different Model**
```bash
# Edit backend/.env
GEMINI_MODEL=models/gemini-2.0-flash-lite

# Restart backend
cd backend
python -m uvicorn src.main:app --reload --port 8000
```

## Error Message for Users

Update the frontend to show a better error message:

```typescript
if (error.includes("quota") || error.includes("429")) {
  return "The AI service is temporarily unavailable due to high usage. Please try again in a few minutes.";
}
```

---

**Status**: ⚠️ Quota Exceeded  
**Solution**: Wait 1-2 minutes OR get new API key  
**Prevention**: Implement rate limiting  
**Long-term**: Consider paid plan for production

## Links

- **API Keys**: https://aistudio.google.com/app/apikey
- **Pricing**: https://ai.google.dev/pricing
- **Rate Limits**: https://ai.google.dev/gemini-api/docs/rate-limits
- **Usage Dashboard**: https://aistudio.google.com/
