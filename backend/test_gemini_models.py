"""
Test script to list available Gemini models
"""
import google.generativeai as genai
from src.config import settings

# Configure with API key
genai.configure(api_key=settings.GEMINI_API_KEY)

print("🔍 Listing available Gemini models...\n")

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Description: {model.description}")
        print(f"   Supported Methods: {model.supported_generation_methods}")
        print()

print("\n💡 Try using one of these model names in your .env file")
