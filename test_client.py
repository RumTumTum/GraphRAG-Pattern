#!/usr/bin/env python3
"""
Test client for the GraphRAG Generation Server
"""

import asyncio
import json
import httpx

async def test_server():
    """Test the generation server endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing GraphRAG Generation Server...")
        
        # Test health
        print("\n1. Health check...")
        try:
            response = await client.get(f"{base_url}/health")
            health_data = response.json()
            print(f"✅ Server health: {health_data}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return
        
        # Test models
        print("\n2. List models...")
        try:
            response = await client.get(f"{base_url}/models")
            models_data = response.json()
            print(f"✅ Available models: {models_data}")
        except Exception as e:
            print(f"❌ Models list failed: {e}")
            return
        
        # Test text generation
        print("\n3. Test text generation...")
        generation_request = {
            "prompt": "Explain GraphRAG in simple terms",
            "model": "llama3.2:latest",
            "temperature": 0.7
        }
        
        try:
            response = await client.post(
                f"{base_url}/generate",
                json=generation_request
            )
            gen_data = response.json()
            print(f"✅ Generated text: {gen_data['text'][:200]}...")
            print(f"📊 Tokens: {gen_data['eval_count']}, Duration: {gen_data['eval_duration_ms']:.0f}ms")
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            return
        
        # Test chat completion
        print("\n4. Test chat completion...")
        chat_request = {
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant specializing in knowledge graphs."},
                {"role": "user", "content": "What are the benefits of using GraphRAG?"}
            ],
            "model": "llama3.2:latest",
            "temperature": 0.7
        }
        
        try:
            response = await client.post(
                f"{base_url}/chat",
                json=chat_request
            )
            chat_data = response.json()
            message_content = chat_data['message']['content']
            print(f"✅ Chat response: {message_content[:200]}...")
            print(f"📊 Tokens: {chat_data['eval_count']}, Duration: {chat_data['eval_duration_ms']:.0f}ms")
        except Exception as e:
            print(f"❌ Chat completion failed: {e}")
            return
        
        # Test with context (GraphRAG-style)
        print("\n5. Test generation with context...")
        context_request = {
            "prompt": "How does this relate to the knowledge graph structure?",
            "context": "Knowledge graphs are structured representations of information that use nodes to represent entities and edges to represent relationships between those entities.",
            "model": "llama3.2:latest",
            "system_prompt": "You are an AI assistant that answers questions based on provided context.",
            "temperature": 0.7
        }
        
        try:
            response = await client.post(
                f"{base_url}/generate",
                json=context_request
            )
            context_data = response.json()
            print(f"✅ Context-aware response: {context_data['text'][:200]}...")
            print(f"📊 Tokens: {context_data['eval_count']}, Duration: {context_data['eval_duration_ms']:.0f}ms")
        except Exception as e:
            print(f"❌ Context generation failed: {e}")
        
        print("\n🎉 All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_server())