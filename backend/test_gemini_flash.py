"""
Test Gemini Flash 1.5 on OpenRouter
"""
import asyncio
import httpx
from src.config import settings

async def test_gemini_flash():
    api_key = settings.GEMINI_API_KEY
    
    print("🧪 Testing google/gemini-flash-1.5 on OpenRouter...\n")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "google/gemini-flash-1.5",
                    "messages": [
                        {"role": "user", "content": "Say hello"}
                    ]
                },
                timeout=30.0
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"Response: {result['choices'][0]['message']['content']}")
            else:
                print(f"❌ Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini_flash())
