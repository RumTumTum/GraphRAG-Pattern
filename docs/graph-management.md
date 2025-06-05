# Knowledge Graph Management

This guide covers managing the GraphRAG knowledge graph data, including setup, querying, and cleanup operations.

## Quick Reference

### Setup Commands
```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Set environment variables
cp .env.example .env

# Create schema and populate data
python scripts/setup_knowledge_graph.py

# Run demonstration queries
python scripts/query_graph.py
```

### Data Management
```bash
# Clear all data (interactive confirmation)
python scripts/clear_knowledge_graph.py

# Repopulate fresh data
python scripts/setup_knowledge_graph.py
```

## Available Scripts

### Python Scripts
- **`setup_knowledge_graph.py`** - Complete setup (schema + data)
- **`query_graph.py`** - Demonstrates GraphRAG queries  
- **`clear_knowledge_graph.py`** - Interactive data cleanup

### Cypher Scripts
- **`01_create_schema.cypher`** - Creates constraints and indexes
- **`02_populate_data.cypher`** - Populates sample academic research data
- **`03_clear_data.cypher`** - Removes all data (preserves schema)

### Manual Cypher Execution
```bash
# Connect to Neo4j shell
docker exec -it graphrag-neo4j cypher-shell -u neo4j -p graphrag123

# Execute individual scripts
:source scripts/01_create_schema.cypher
:source scripts/02_populate_data.cypher
:source scripts/03_clear_data.cypher
```

## Sample Dataset Overview

The academic research knowledge graph includes:
- **6 Papers** about GraphRAG and knowledge graphs
- **6 Authors** from major AI research institutions  
- **4 Institutions** (Stanford, MIT, DeepMind, OpenAI)
- **4 Venues** (NeurIPS, ICML, Nature, arXiv)
- **8 Topics** with relevance relationships
- **Rich relationships** for GraphRAG demonstrations

## Safety Features

- **Environment variables**: No hardcoded credentials
- **Confirmation prompts**: Interactive deletion confirmation  
- **Schema preservation**: Clearing data keeps constraints/indexes
- **Error handling**: Proper connection testing and error messages

## Common Operations

### Reset the Graph
To start fresh with clean data:
```bash
python scripts/clear_knowledge_graph.py
python scripts/setup_knowledge_graph.py
```

### Verify Setup
Check that everything is working:
```bash
# Test basic connectivity
curl http://localhost:7474

# Run sample queries
python scripts/query_graph.py
```

### View in Browser
1. Open http://localhost:7474
2. Login with Neo4j credentials from `.env`
3. Run: `MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 25`

For learning Cypher and exploring the data, see [graph-quickstart.md](graph-quickstart.md).