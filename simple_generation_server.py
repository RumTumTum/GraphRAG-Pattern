#!/usr/bin/env python3
"""
Simple HTTP API server for GraphRAG Generation
Works with your existing Ollama setup
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "llama3.2:latest"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    context: Optional[str] = None
    system_prompt: Optional[str] = None

class ChatMessage(BaseModel):
    role: str  # system, user, assistant
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "llama3.2:latest" 
    temperature: float = 0.7
    max_tokens: Optional[int] = None

class OllamaClient:
    """Simple Ollama client"""
    
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
            logger.error(f"Failed to list models: {e}")
            raise
    
    async def generate(self, 
                      prompt: str, 
                      model: str = "llama3.2:latest",
                      system: Optional[str] = None,
                      context: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None):
        """Generate text"""
        
        # Prepare the full prompt with context if provided
        full_prompt = prompt
        if context:
            full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}"
        
        payload = {
            "model": model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        if system:
            payload["system"] = system
            
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise
    
    async def chat(self, 
                   messages: List[Dict[str, str]], 
                   model: str = "llama3.2:latest",
                   temperature: float = 0.7,
                   max_tokens: Optional[int] = None):
        """Chat completion"""
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }
        
        if max_tokens:
            payload["options"]["num_predict"] = max_tokens
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            raise
    
    async def check_health(self):
        """Check if Ollama is accessible"""
        try:
            response = await self.client.get(f"{self.base_url}/api/version")
            return response.status_code == 200
        except Exception:
            return False

# Initialize FastAPI app and Ollama client
app = FastAPI(title="GraphRAG Generation Server", version="1.0.0")
ollama = OllamaClient()

@app.on_event("startup")
async def startup_event():
    """Check Ollama connection on startup"""
    health = await ollama.check_health()
    if not health:
        logger.warning("Ollama service not accessible at startup!")
    else:
        models = await ollama.list_models()
        model_count = len(models.get("models", []))
        logger.info(f"Connected to Ollama. Available models: {model_count}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "GraphRAG Generation Server",
        "status": "running",
        "ollama_url": ollama.base_url
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    ollama_healthy = await ollama.check_health()
    return {
        "status": "healthy" if ollama_healthy else "unhealthy",
        "ollama_connected": ollama_healthy
    }

@app.get("/models")
async def list_models():
    """List available models"""
    try:
        models_response = await ollama.list_models()
        models = models_response.get("models", [])
        return {
            "models": [model.get("name") for model in models],
            "count": len(models)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")

@app.post("/generate")
async def generate_text(request: GenerateRequest):
    """Generate text using Ollama"""
    try:
        result = await ollama.generate(
            prompt=request.prompt,
            model=request.model,
            system=request.system_prompt,
            context=request.context,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return {
            "text": result.get("response", ""),
            "model": request.model,
            "eval_count": result.get("eval_count", 0),
            "eval_duration_ms": result.get("eval_duration", 0) / 1e6
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.post("/chat")
async def chat_completion(request: ChatRequest):
    """Chat completion using Ollama"""
    try:
        # Convert Pydantic models to dict
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        result = await ollama.chat(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return {
            "message": result.get("message", {}),
            "model": request.model,
            "eval_count": result.get("eval_count", 0),
            "eval_duration_ms": result.get("eval_duration", 0) / 1e6
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat completion failed: {str(e)}")

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000,
        log_level="info"
    )