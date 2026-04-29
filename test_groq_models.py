#!/usr/bin/env python3
"""
Test script to check available models on Groq API.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_groq_models():
    """Test available models on Groq API."""
    print("Checking available models on Groq API...")
    
    try:
        import openai
        
        api_key = os.environ.get("XAI_API_KEY")
        base_url = os.environ.get("XAI_BASE_URL", "https://api.groq.com/openai/v1")
        
        if not api_key:
            print("No API key found")
            return
        
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        
        # List available models
        models = client.models.list()
        
        print(f"Available models on {base_url}:")
        print("=" * 60)
        
        # Filter for chat models
        chat_models = [model for model in models.data if "chat" in model.id.lower() or "llama" in model.id.lower()]
        
        for model in sorted(chat_models, key=lambda x: x.id):
            print(f"- {model.id}")
        
        # Test a simple model
        test_model = "llama3-8b-8192"  # Common Groq model
        if test_model in [m.id for m in chat_models]:
            print(f"\nTesting with model: {test_model}")
            
            response = client.chat.completions.create(
                model=test_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'Hello from Groq API!'"}
                ],
                max_tokens=10,
                timeout=10
            )
            
            content = response.choices[0].message.content
            print(f"Success! Response: {content}")
            
            return test_model
        else:
            print("No suitable test model found")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    test_groq_models()
