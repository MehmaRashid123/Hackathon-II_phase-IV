"""
Quick test to verify chat endpoint works with OpenRouter
"""
import httpx
import asyncio

async def test_chat():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/c560957f-4bc7-4a62-bc7d-ec18a56b15a1/chat",
            json={
                "message": "hi",
                "conversation_id": None
            },
            timeout=30.0
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

if __name__ == "__main__":
    asyncio.run(test_chat())
