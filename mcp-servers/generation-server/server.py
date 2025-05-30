#!/usr/bin/env python3
"""
Generation MCP Server for GraphRAG Pattern
Integrates with Ollama for local LLM inference
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Sequence

import httpx
from mcp.server.models import InitializationOptions
from mcp.server.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    ReadResourceRequest,
    ReadResourceResult,
    Resource,
    TextContent,
    Tool,
)
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List available models from Ollama"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return data.get("models", [])
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    async def generate(self, 
                      prompt: str, 
                      model: str = "llama3.2:latest", 
                      system: Optional[str] = None,
                      context: Optional[str] = None,
                      temperature: float = 0.7,
                      max_tokens: Optional[int] = None) -> str:
        """Generate text using Ollama"""
        
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
            result = response.json()
            return result.get("response", "")
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise
    
    async def chat(self, 
                   messages: List[Dict[str, str]], 
                   model: str = "llama3.2:latest",
                   temperature: float = 0.7,
                   max_tokens: Optional[int] = None) -> str:
        """Chat completion using Ollama"""
        
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
            result = response.json()
            return result.get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            raise
    
    async def check_health(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = await self.client.get(f"{self.base_url}/api/version")
            return response.status_code == 200
        except Exception:
            return False

# Initialize Ollama client
ollama = OllamaClient()

# Create the server instance
server = Server("graphrag-generation-server")

@server.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="generation://models",
            name="Available Models",
            description="List of available Ollama models",
            mimeType="application/json"
        ),
        Resource(
            uri="generation://health",
            name="Service Health", 
            description="Health status of the generation service",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read resource content"""
    if uri == "generation://models":
        models = await ollama.list_models()
        return json.dumps({"models": models}, indent=2)
    elif uri == "generation://health":
        health = await ollama.check_health()
        return json.dumps({"healthy": health, "service": "ollama"}, indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="generate_text",
            description="Generate text using Ollama LLM",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt for text generation"
                    },
                    "model": {
                        "type": "string", 
                        "description": "The Ollama model to use",
                        "default": "llama3.2:latest"
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum tokens to generate"
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Sampling temperature (0.0 to 1.0)",
                        "default": 0.7
                    },
                    "context": {
                        "type": "string",
                        "description": "Additional context from retrieval"
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "System prompt for the model"
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="chat_completion",
            description="Chat completion using Ollama LLM",
            inputSchema={
                "type": "object",
                "properties": {
                    "messages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "role": {
                                    "type": "string",
                                    "enum": ["system", "user", "assistant"]
                                },
                                "content": {
                                    "type": "string"
                                }
                            },
                            "required": ["role", "content"]
                        },
                        "description": "List of chat messages"
                    },
                    "model": {
                        "type": "string",
                        "description": "The Ollama model to use", 
                        "default": "llama3.2:latest"
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Sampling temperature (0.0 to 1.0)",
                        "default": 0.7
                    },
                    "max_tokens": {
                        "type": "integer",
                        "description": "Maximum tokens to generate"
                    }
                },
                "required": ["messages"]
            }
        ),
        Tool(
            name="list_models",
            description="List available Ollama models",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    
    if name == "generate_text":
        prompt = arguments.get("prompt", "")
        model = arguments.get("model", "llama3.2:latest")
        max_tokens = arguments.get("max_tokens")
        temperature = arguments.get("temperature", 0.7)
        context = arguments.get("context")
        system_prompt = arguments.get("system_prompt")
        
        try:
            result = await ollama.generate(
                prompt=prompt,
                model=model,
                system=system_prompt,
                context=context,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return [TextContent(
                type="text",
                text=result
            )]
            
        except Exception as e:
            return [TextContent(
                type="text", 
                text=f"Generation failed: {str(e)}"
            )]
    
    elif name == "chat_completion":
        messages = arguments.get("messages", [])
        model = arguments.get("model", "llama3.2:latest")
        temperature = arguments.get("temperature", 0.7)
        max_tokens = arguments.get("max_tokens")
        
        try:
            result = await ollama.chat(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return [TextContent(
                type="text",
                text=result
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Chat completion failed: {str(e)}"
            )]
    
    elif name == "list_models":
        try:
            models = await ollama.list_models()
            model_list = [model.get("name", "unknown") for model in models]
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "available_models": model_list,
                    "count": len(model_list)
                }, indent=2)
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Failed to list models: {str(e)}"
            )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point for the server"""
    # Check Ollama health on startup
    health = await ollama.check_health()
    if not health:
        logger.warning("Ollama service not accessible at startup. Please ensure Ollama is running.")
    else:
        models = await ollama.list_models()
        logger.info(f"Connected to Ollama. Available models: {len(models)}")
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="graphrag-generation-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())