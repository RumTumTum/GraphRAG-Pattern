#!/usr/bin/env python3
"""
Simple test script to verify Ollama integration
"""

import asyncio
import json
import httpx

class OllamaClient:
    """Simple Ollama client for testing"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def list_models(self):
        """List available models"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to list models: {e}")
            return None
    
    async def generate(self, prompt: str, model: str = "llama3.2:latest"):
        """Generate text"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Generation failed: {e}")
            return None
    
    async def check_health(self):
        """Check if Ollama is accessible"""
        try:
            response = await self.client.get(f"{self.base_url}/api/version")
            return response.status_code == 200
        except Exception:
            return False

async def main():
    """Test the Ollama connection and generation"""
    print("🧪 Testing Ollama Integration...")
    
    # Initialize client
    ollama = OllamaClient()
    
    # Check health
    print("\n1. Checking Ollama health...")
    healthy = await ollama.check_health()
    if not healthy:
        print("❌ Ollama is not accessible. Make sure it's running with: ollama serve")
        return
    
    print("✅ Ollama is running!")
    
    # List models
    print("\n2. Listing available models...")
    models_response = await ollama.list_models()
    if models_response:
        models = models_response.get("models", [])
        print(f"Found {len(models)} models:")
        for model in models:
            name = model.get("name", "unknown")
            size = model.get("size", 0)
            print(f"  - {name} ({size / 1e9:.1f}GB)")
    else:
        print("❌ Failed to list models")
        return
    
    # Test generation
    print("\n3. Testing text generation...")
    test_prompt = "What is a knowledge graph? Explain in one sentence."
    
    print(f"Prompt: {test_prompt}")
    print("Generating response...")
    
    result = await ollama.generate(test_prompt)
    if result:
        response_text = result.get("response", "")
        print(f"\n✅ Response: {response_text}")
        
        # Show some stats
        eval_count = result.get("eval_count", 0)
        eval_duration = result.get("eval_duration", 0)
        if eval_count > 0 and eval_duration > 0:
            tokens_per_second = eval_count / (eval_duration / 1e9)
            print(f"📊 Generated {eval_count} tokens in {eval_duration/1e9:.2f}s ({tokens_per_second:.1f} tokens/sec)")
    else:
        print("❌ Generation failed")
    
    print("\n🎉 Test complete!")

if __name__ == "__main__":
    asyncio.run(main())