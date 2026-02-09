# Google Gemini API Setup Guide

## Quick Start: Get Your Free Gemini API Key

### Step 1: Visit Google AI Studio
Go to: **https://makersuite.google.com/app/apikey**

Or alternatively: **https://aistudio.google.com/app/apikey**

### Step 2: Sign In
- Sign in with your Google account
- Accept the terms of service if prompted

### Step 3: Create API Key
1. Click "Create API Key" button
2. Select "Create API key in new project" (or choose an existing project)
3. Copy the generated API key (starts with `AIza...`)

### Step 4: Add to Your Project
Open `backend/.env` and add:
```env
GEMINI_API_KEY=AIzaSy...your-actual-key-here
```

### Step 5: Test It
```bash
cd backend
python -m pytest tests/unit/test_todo_assistant.py -v
```

## Free Tier Limits

Gemini offers a generous free tier:
- **60 requests per minute**
- **1,500 requests per day**
- **1 million tokens per minute**

Perfect for development and testing!

## Supported Models

- `gemini-1.5-pro` (recommended) - Most capable, best for complex tasks
- `gemini-1.5-flash` - Faster, good for simple tasks
- `gemini-pro` - Previous generation

## Troubleshooting

### "API key not valid"
- Make sure you copied the entire key
- Check for extra spaces or newlines
- Regenerate the key if needed

### "Resource exhausted"
- You've hit the rate limit
- Wait a minute and try again
- Consider upgrading to paid tier

### "Model not found"
- Check the model name in `.env`
- Use `gemini-1.5-pro` (recommended)

## Security Best Practices

1. **Never commit API keys to git**
   - `.env` is already in `.gitignore`
   - Use environment variables in production

2. **Restrict API key usage**
   - In Google Cloud Console, restrict by IP or referrer
   - Set up API key restrictions

3. **Monitor usage**
   - Check usage in Google AI Studio
   - Set up billing alerts

## Upgrading to Paid Tier

If you need more capacity:
1. Go to Google Cloud Console
2. Enable billing for your project
3. Gemini API will automatically use paid tier
4. Pay-as-you-go pricing applies

## Support

- Documentation: https://ai.google.dev/docs
- Community: https://discuss.ai.google.dev/
- Issues: https://github.com/google/generative-ai-python/issues

## Next Steps

Once you have your API key set up:
1. Start the backend server: `cd backend && python -m uvicorn src.main:app --reload`
2. Test the chat endpoint
3. Integrate with your frontend
4. Build amazing AI-powered features!

Happy coding! 🚀
