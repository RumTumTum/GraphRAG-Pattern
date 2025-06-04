# Neo4j Setup Guide

This guide covers setting up Neo4j for the GraphRAG pattern implementation.

## Quick Start

### 1. Start Neo4j with Docker Compose

```bash
# Start Neo4j and Chroma services
docker-compose up -d

# Check if services are running
docker-compose ps

# View logs if needed
docker-compose logs neo4j
```

### 2. Access Neo4j

- **Neo4j Browser**: http://localhost:7474
- **Bolt Protocol**: bolt://localhost:7687
- **Username**: `neo4j`
- **Password**: `graphrag123`

### 3. Verify Installation

```bash
# Test connection via cypher-shell (if installed locally)
cypher-shell -a bolt://localhost:7687 -u neo4j -p graphrag123

# Or test via Python
python -c "
from neo4j import GraphDatabase
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'graphrag123'))
with driver.session() as session:
    result = session.run('RETURN \"Neo4j is connected!\" as message')
    print(result.single()['message'])
driver.close()
"
```

## Configuration Details

### Docker Compose Services

- **Neo4j Community Edition 5.15**
  - HTTP: Port 7474 (Browser interface)
  - Bolt: Port 7687 (Database connections)
  - APOC plugins enabled for advanced procedures
  - Memory: 1GB heap, 512MB page cache

- **Chroma Vector Database**
  - HTTP: Port 8001
  - Ready for future vector storage needs

### Environment Variables

Copy `.env.example` to `.env` and customize if needed:

```bash
cp .env.example .env
# Edit settings if needed: nano .env
```

Available configuration options:
- `NEO4J_PASSWORD`: Database password (default: graphrag123)
- `NEO4J_HTTP_PORT`: Browser port (default: 7474)
- `NEO4J_BOLT_PORT`: Database connection port (default: 7687)
- `NEO4J_HEAP_MAX`: Maximum heap memory (default: 1G)
- `CHROMA_PORT`: Vector DB port (default: 8001)

### Memory Configuration

Current settings are optimized for development:
- Heap: 512M initial, 1G maximum
- Page cache: 512M
- Query cache: 100 queries

For production, adjust based on your data size and available RAM.

## Basic Operations

### Start/Stop Services

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose down -v

# Restart Neo4j only
docker-compose restart neo4j
```

### Data Persistence

Data is persisted in Docker volumes:
- `neo4j_data`: Database files
- `neo4j_logs`: Log files
- `neo4j_import`: Import directory for bulk data
- `neo4j_plugins`: Additional plugins

### Import Directory

To import CSV or other data files:

```bash
# Copy files to import directory
docker cp your-data.csv graphrag-neo4j:/var/lib/neo4j/import/

# Or use volume mount (already configured)
# Place files in the neo4j_import volume
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :7474
   lsof -i :7687
   
   # Modify ports in docker-compose.yml if needed
   ```

2. **Memory issues**
   ```bash
   # Reduce memory in docker-compose.yml
   NEO4J_dbms_memory_heap_max__size: 512M
   ```

3. **Connection refused**
   ```bash
   # Check if container is running
   docker ps | grep neo4j
   
   # Check logs
   docker-compose logs neo4j
   ```

4. **Authentication failed**
   - Default credentials: `neo4j` / `graphrag123`
   - Change in docker-compose.yml: `NEO4J_AUTH: neo4j/newpassword`

### Useful Commands

```bash
# Enter Neo4j container
docker exec -it graphrag-neo4j bash

# Run cypher-shell inside container
docker exec -it graphrag-neo4j cypher-shell -u neo4j -p graphrag123

# Monitor resource usage
docker stats graphrag-neo4j

# Backup database
docker exec graphrag-neo4j neo4j-admin dump --database=neo4j --to=/tmp/backup.dump
docker cp graphrag-neo4j:/tmp/backup.dump ./backup.dump
```

## Next Steps

1. **Build Ontology**: Create domain-specific schemas using Cypher
2. **Populate Graph**: Import your data using Cypher scripts
3. **Query Examples**: Explore the graph with sample queries
4. **MCP Integration**: Connect via GraphDB MCP Server

See the main README for the complete workflow.