# Generation MCP Server

An MCP (Model Context Protocol) server that provides text generation capabilities using Ollama for local LLM inference.

## Features

- **Text Generation**: Generate text responses using local Ollama models
- **Chat Completion**: Multi-turn conversation support
- **Model Management**: List and switch between available Ollama models
- **Context Integration**: Support for retrieval context in generation
- **Health Monitoring**: Service health checks and monitoring

## Prerequisites

- Python 3.9+
- Ollama installed and running locally
- At least one Ollama model pulled (e.g., `ollama pull llama3.2`)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is running
ollama serve
```

## Usage

### Start the MCP Server

```bash
python server.py
```

The server will start on the default MCP port and connect to Ollama at `http://localhost:11434`.

### Available Tools

#### 1. generate_text
Generate text using a prompt with optional context.

```json
{
  "name": "generate_text",
  "arguments": {
    "prompt": "Explain the concept of knowledge graphs",
    "model": "llama3.2:latest",
    "temperature": 0.7,
    "context": "Previous retrieval results...",
    "system_prompt": "You are a helpful AI assistant."
  }
}
```

#### 2. chat_completion
Multi-turn chat conversation.

```json
{
  "name": "chat_completion",
  "arguments": {
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is GraphRAG?"},
      {"role": "assistant", "content": "GraphRAG combines..."},
      {"role": "user", "content": "How does it work?"}
    ],
    "model": "llama3.2:latest",
    "temperature": 0.7
  }
}
```

#### 3. list_models
List all available Ollama models.

```json
{
  "name": "list_models",
  "arguments": {}
}
```

### Available Resources

#### Models Resource
Access information about available models:
```
URI: generation://models
```

#### Health Resource
Check service health status:
```
URI: generation://health
```

## Configuration

The server can be configured with environment variables:

- `OLLAMA_BASE_URL`: Ollama API base URL (default: `http://localhost:11434`)
- `DEFAULT_MODEL`: Default model to use (default: `llama3.2:latest`)
- `DEFAULT_TEMPERATURE`: Default temperature (default: `0.7`)

## Integration with GraphRAG

This server is designed to integrate with the larger GraphRAG pattern:

1. **Retrieval Integration**: Accepts context from graph and vector database retrievals
2. **Ontology Awareness**: Can be prompted with ontology information for structured responses
3. **Citation Support**: Supports generating responses with source citations
4. **Multi-modal**: Extensible for future multi-modal capabilities

## Error Handling

The server includes comprehensive error handling:

- Connection failures to Ollama
- Model not found errors
- Generation timeouts
- Invalid request parameters

## Development

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Adding New Models

1. Pull the model in Ollama: `ollama pull model-name`
2. The model will automatically be available through the `list_models` tool
3. Use the model name in generation requests

## Troubleshooting

### Ollama Not Running
```
Error: Failed to connect to Ollama
Solution: Ensure Ollama is running with `ollama serve`
```

### Model Not Found
```
Error: Model 'model-name' not found
Solution: Pull the model with `ollama pull model-name`
```

### Generation Timeout
```
Error: Generation timed out
Solution: Reduce prompt complexity or increase timeout in configuration
```