# GraphRAG Pattern

A comprehensive implementation of the GraphRAG (Graph Retrieval-Augmented Generation) pattern that combines knowledge graphs, vector databases, and local LLM generation for enhanced AI reasoning and retrieval.

## Architecture Overview

This project implements a multi-component GraphRAG system with the following core components:

- **Ontology Management**: Define and manage domain-specific ontologies
- **Knowledge Graph Ingestion**: Extract and structure data into knowledge graphs
- **Hybrid Retrieval System**: Combined GraphDB and Vector DB retrieval via MCP servers
- **Local LLM Generation**: Response generation using Ollama via MCP server

## Features

### 🔧 Core functionality
What's the reason I'm doing this?
To show that GraphRAG is more effective than RAG for certain retrieval tasks
To do this, must:
- Run GraphRAG
- Run RAG
- Compare side-by-side (CLI OK to start)
- Later can also do a front-end comparison
- Really cool if could do a dagger build of all the components

### Next Steps

1. **Build Ontology**: Create domain-specific schemas using Cypher
2. **Populate Graph**: Import your data using Cypher scripts
3. **Query Examples**: Explore the graph with sample queries
4. **MCP Integration**: Connect via GraphDB MCP Server


### 🔧 Next up   
 - Graph queryable
   - Neo4J docker and instructions
   - build ontology using cypher (temporary)
   - Populate KG using cyper (temporary)
   - Script to show graph outputs
   - Instructions to view via CLI and Neo4J
 - RAG using MCP 
   - GraphDB MCP Server
   - Query graph and use context for LLM
 Later features
 - Dagger run
 - Ontology-builder (e.g., pythonic way of building ontologies)
 - Examples
   - Create domain-specific schemas using Cypher
   - Populate Graph with sample data using Cypher scripts
   - Query Examples: Explore the graph with sample queries



### 🔧 Core Components

- [ ] **Ontology Builder**
  - Define domain-specific schemas and relationships
  - Validate entity types and relationship constraints
  - Export ontologies in standard formats (OWL, RDF)

- [ ] **Knowledge Graph Ingestion Pipeline**
  - Document parsing and entity extraction
  - Relationship identification and validation
  - Graph database population (Neo4j/ArangoDB)
  - Incremental updates and versioning

- [ ] **MCP Servers**
  - [ ] **GraphDB MCP Server**: Neo4j/ArangoDB query interface
  - [ ] **Vector DB MCP Server**: Embeddings storage and similarity search
  - [ ] **Generation MCP Server**: Ollama integration for local LLM inference

- [ ] **Retrieval System**
  - Hybrid search combining graph traversal and vector similarity
  - Query planning and optimization
  - Context aggregation and ranking
  - Multi-hop reasoning support

- [ ] **Response Generation**
  - Local LLM integration via Ollama
  - Context-aware prompt engineering
  - Fact verification against knowledge graph
  - Citation and source tracking

### 🛠️ Development Features

- [ ] **Configuration Management**
  - Environment-specific settings
  - MCP server discovery and registration
  - Database connection management

- [ ] **Monitoring & Observability**
  - Query performance metrics
  - Retrieval accuracy tracking
  - LLM generation quality assessment

- [ ] **Testing Framework**
  - Unit tests for all components
  - Integration tests for end-to-end workflows
  - Performance benchmarking

## Technology Stack

- **Graph Database**: Neo4j or ArangoDB
- **Vector Database**: Chroma, Qdrant, or Weaviate
- **Local LLM**: Ollama (supporting Llama, Mistral, CodeLlama, etc.)
- **MCP Protocol**: Model Context Protocol for component communication
- **Backend**: Python with FastAPI
- **Ontology**: OWL/RDF standards

## Project Structure

```
GraphRAG-Pattern/
├── README.md
├── main.py
├── requirements.txt
├── config/
│   ├── ontologies/
│   ├── databases.yaml
│   └── mcp-servers.yaml
├── src/
│   ├── ontology/
│   ├── ingestion/
│   ├── retrieval/
│   └── generation/
├── mcp-servers/
│   ├── graphdb-server/
│   ├── vectordb-server/
│   └── generation-server/
├── tests/
└── docs/
```

## Getting Started

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Ollama installed locally
- Neo4j or ArangoDB instance

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd GraphRAG-Pattern

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up databases (using Docker Compose)
docker-compose up -d

# Initialize Ollama models
ollama pull llama3.2  # or your preferred model
```

### Neo4j Database Setup

```bash
# Copy environment configuration (optional - defaults work for development)
cp .env.example .env

# Customize settings in .env if needed (passwords, ports, memory)
# nano .env

# Start Neo4j and Chroma with Docker Compose
docker-compose up -d

# Verify Neo4j is running (should return JSON response)
curl http://localhost:7474
```

**Access Neo4j:**
- Neo4j Browser: http://localhost:7474 
- Username: `neo4j`, Password: `graphrag123`
- Bolt Protocol: bolt://localhost:7687

For detailed Neo4j setup and troubleshooting, see [docs/neo4j-setup.md](docs/neo4j-setup.md).

### Quick Start

#### Start the Generation Server

```bash
# Activate virtual environment
source venv/bin/activate

# Start the Generation HTTP API server
python simple_generation_server.py
```

The server will start at `http://127.0.0.1:8000` with the following endpoints:
- `/generate` - Text generation with optional context (GraphRAG-style)
- `/chat` - Multi-turn conversations
- `/models` - List available Ollama models
- `/health` - Service health check

#### Test the Generation Server

```bash
# In another terminal, run the test client
source venv/bin/activate
python test_client.py

# Or test with curl
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is GraphRAG?", "model": "llama3.2:latest"}'
```

#### Start Other Components (Coming Soon)

```bash
# Start the MCP servers (in development)
python -m mcp_servers.graphdb_server
python -m mcp_servers.vectordb_server

# Run the main application
python main.py
```

## Usage Examples

### Generate Text with Context (GraphRAG-style)

```python
import httpx
import asyncio

async def graphrag_example():
    async with httpx.AsyncClient() as client:
        # Context from graph/vector retrieval (simulated)
        context = """
        Knowledge graphs are structured representations of information that use nodes 
        to represent entities and edges to represent relationships between those entities.
        They enable semantic understanding and reasoning about complex data relationships.
        """
        
        # Generate response with context
        response = await client.post("http://127.0.0.1:8000/generate", json={
            "prompt": "How do knowledge graphs improve AI reasoning?",
            "context": context,
            "system_prompt": "Answer based on the provided context.",
            "model": "llama3.2:latest",
            "temperature": 0.7
        })
        
        result = response.json()
        print(f"Response: {result['text']}")

# Run the example
asyncio.run(graphrag_example())
```

### Multi-turn Chat

```python
import httpx
import asyncio

async def chat_example():
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8000/chat", json={
            "messages": [
                {"role": "system", "content": "You are an expert in knowledge graphs and GraphRAG."},
                {"role": "user", "content": "What is GraphRAG?"},
                {"role": "assistant", "content": "GraphRAG combines knowledge graphs with retrieval-augmented generation..."},
                {"role": "user", "content": "How does it differ from traditional RAG?"}
            ],
            "model": "llama3.2:latest"
        })
        
        result = response.json()
        print(f"Assistant: {result['message']['content']}")

asyncio.run(chat_example())
```

### Future Usage (In Development)

```python
# Define an Ontology
from src.ontology import OntologyBuilder

builder = OntologyBuilder()
builder.define_entity("Person", properties=["name", "age", "email"])
builder.define_relationship("WORKS_FOR", source="Person", target="Company")
ontology = builder.build()

# Ingest Documents
from src.ingestion import KnowledgeGraphBuilder

kg_builder = KnowledgeGraphBuilder(ontology)
kg_builder.ingest_document("path/to/document.pdf")
kg_builder.commit_to_graph()

# Query the System
from src.retrieval import HybridRetriever
from src.generation import ResponseGenerator

retriever = HybridRetriever()
generator = ResponseGenerator()

# Hybrid retrieval
context = retriever.search("What is the relationship between AI and machine learning?")

# Generate response
response = generator.generate(query, context)
print(response.text)
print(response.citations)
```

## Configuration

See `config/` directory for detailed configuration options:

- `ontologies/`: Domain-specific ontology definitions
- `databases.yaml`: Database connection settings
- `mcp-servers.yaml`: MCP server configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Current Status

### ✅ Completed
- [x] **Generation Server**: HTTP API for local LLM inference via Ollama
  - Text generation with context support (GraphRAG-style)
  - Multi-turn chat conversations
  - Model management and health monitoring
  - FastAPI-based REST endpoints

### 🚧 In Development
- [ ] **GraphDB MCP Server**: Neo4j/ArangoDB integration
- [ ] **Vector DB MCP Server**: Embeddings and similarity search
- [ ] **Ontology Management**: Schema definition and validation
- [ ] **Knowledge Graph Ingestion**: Document parsing and graph population

## Roadmap

- [x] **Phase 1a**: Generation Server with Ollama integration ✅
- [ ] **Phase 1b**: Core MCP servers and basic retrieval
- [ ] **Phase 2**: Advanced ontology management
- [ ] **Phase 3**: Multi-modal ingestion support
- [ ] **Phase 4**: Performance optimization and scaling
- [ ] **Phase 5**: Web interface and visualization tools