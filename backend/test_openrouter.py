"""
Test OpenRouter API connection
"""
import asyncio
import httpx
from src.config import settings

async def test_openrouter():
    api_key = settings.GEMINI_API_KEY
    model = "nvidia/nemotron-3-nano-30b-a3b:free"
    
    print(f"🔑 API Key: {api_key[:20]}...")
    print(f"🤖 Model: {model}")
    print(f"🌐 Testing OpenRouter API...\n")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "Todo App Test"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "user", "content": "Say hello in one word"}
                    ],
                    "max_tokens": 10
                },
                timeout=30.0
            )
            
            print(f"📥 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                message = result["choices"][0]["message"]["content"]
                print(f"✅ Response: {message}")
                print(f"\n✅ OpenRouter is working!")
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_openrouter())
