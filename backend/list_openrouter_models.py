"""
List available OpenRouter models
"""
import asyncio
import httpx
from src.config import settings

async def list_models():
    api_key = settings.GEMINI_API_KEY
    
    print("🔍 Fetching available OpenRouter models...\n")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={
                    "Authorization": f"Bearer {api_key}"
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                models = result.get("data", [])
                
                print(f"✅ Found {len(models)} models\n")
                print("FREE MODELS:\n")
                
                free_count = 0
                for model in models:
                    if model.get("pricing", {}).get("prompt") == "0" or ":free" in model["id"]:
                        free_count += 1
                        print(f"✅ {model['id']}")
                        print(f"   Name: {model.get('name', 'N/A')}")
                        print(f"   Context: {model.get('context_length', 'N/A')} tokens")
                        print()
                        
                        if free_count >= 10:  # Show first 10 free models
                            break
                
                print(f"\n💡 Total free models shown: {free_count}")
                print("\n📝 Recommended models:")
                print("   - google/gemini-flash-1.5")
                print("   - meta-llama/llama-3.2-3b-instruct:free")
                print("   - microsoft/phi-3-mini-128k-instruct:free")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(list_models())
