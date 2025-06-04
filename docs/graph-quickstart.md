# Neo4j Quickstart: Learning Cypher with Academic Research Data

This guide teaches you Cypher query language using our sample academic research knowledge graph. We'll start with the basics and progress to advanced GraphRAG-style queries.

## Setup

### 1. Start Neo4j and Load Data

```bash
# Ensure Neo4j is running
docker-compose up -d

# Load the sample academic research data
cp .env.example .env
pip install -r scripts/requirements.txt
python scripts/setup_knowledge_graph.py
```

### 2. Connect via CLI

```bash
# Connect to Neo4j using cypher-shell
docker exec -it graphrag-neo4j cypher-shell -u neo4j -p graphrag123
```

You should see the `neo4j>` prompt. Let's start learning!

## Part 1: Cypher Basics

### Understanding Our Data

First, let's see what types of data we have:

```cypher
// See all node types (labels) and counts
MATCH (n) 
RETURN DISTINCT labels(n) as node_type, count(n) as count
ORDER BY count DESC;
```

**Expected output:**
```
│node_type    │count│
├─────────────┼─────┤
│["Paper"]    │6    │
│["Author"]   │6    │
│["Topic"]    │8    │
│["Institutio"]│4    │
│["Venue"]    │4    │
```

### Basic MATCH Statements

The `MATCH` clause finds patterns in the graph:

```cypher
// List all papers with their titles and years
MATCH (p:Paper) 
RETURN p.title, p.year
ORDER BY p.year DESC;
```

```cypher
// Find all authors with their names
MATCH (a:Author) 
RETURN a.name, a.h_index
ORDER BY a.h_index DESC;
```

```cypher
// Show all institutions
MATCH (i:Institution) 
RETURN i.name, i.country, i.type;
```

### Filtering with WHERE

Use `WHERE` to filter results:

```cypher
// Find papers published in 2024
MATCH (p:Paper) 
WHERE p.year = 2024 
RETURN p.title, p.citation_count;
```

```cypher
// Find highly cited papers (more than 100 citations)
MATCH (p:Paper) 
WHERE p.citation_count > 100 
RETURN p.title, p.citation_count
ORDER BY p.citation_count DESC;
```

```cypher
// Find authors with h-index above 40
MATCH (a:Author) 
WHERE a.h_index > 40 
RETURN a.name, a.h_index, a.total_citations;
```

## Part 2: Exploring Relationships

### Simple Relationships

Now let's explore connections between nodes:

```cypher
// Find which authors wrote which papers
MATCH (a:Author)-[:AUTHORED]->(p:Paper) 
RETURN a.name as author, p.title as paper;
```

```cypher
// See author affiliations
MATCH (a:Author)-[:AFFILIATED_WITH]->(i:Institution) 
RETURN a.name as author, i.name as institution, i.country;
```

```cypher
// Find what topics papers are about
MATCH (p:Paper)-[:ABOUT]->(t:Topic) 
RETURN p.title as paper, t.name as topic
ORDER BY p.title;
```

### Relationship Properties

Relationships can have properties too:

```cypher
// See relevance scores for paper-topic relationships
MATCH (p:Paper)-[r:ABOUT]->(t:Topic) 
RETURN p.title, t.name, r.relevance
ORDER BY r.relevance DESC;
```

```cypher
// Find first authors vs co-authors
MATCH (a:Author)-[r:AUTHORED]->(p:Paper) 
RETURN a.name, p.title, r.role
ORDER BY p.title;
```

## Part 3: Multi-Node Patterns

### Two-Step Relationships

Find patterns that span multiple relationships:

```cypher
// Find papers and their authors' institutions
MATCH (p:Paper)<-[:AUTHORED]-(a:Author)-[:AFFILIATED_WITH]->(i:Institution) 
RETURN p.title, a.name, i.name
ORDER BY p.title;
```

```cypher
// Find papers published in specific venues by institution
MATCH (p:Paper)-[:PUBLISHED_IN]->(v:Venue),
      (p)<-[:AUTHORED]-(a:Author)-[:AFFILIATED_WITH]->(i:Institution)
RETURN v.name as venue, i.name as institution, count(p) as papers_count
ORDER BY papers_count DESC;
```

### Citation Networks

Explore how papers cite each other:

```cypher
// Find direct citations
MATCH (citing:Paper)-[:CITES]->(cited:Paper) 
RETURN citing.title as "Paper That Cites", 
       cited.title as "Paper Being Cited";
```

```cypher
// Find citation chains (2 steps deep)
MATCH path = (p1:Paper)-[:CITES]->(p2:Paper)-[:CITES]->(p3:Paper)
RETURN p1.title as start_paper, 
       p2.title as middle_paper, 
       p3.title as end_paper;
```

## Part 4: Aggregation and Analysis

### Counting and Grouping

Use aggregate functions to analyze data:

```cypher
// Count papers per author
MATCH (a:Author)-[:AUTHORED]->(p:Paper) 
RETURN a.name, count(p) as paper_count
ORDER BY paper_count DESC;
```

```cypher
// Count papers per institution
MATCH (i:Institution)<-[:AFFILIATED_WITH]-(a:Author)-[:AUTHORED]->(p:Paper) 
RETURN i.name, count(DISTINCT p) as papers, count(DISTINCT a) as authors
ORDER BY papers DESC;
```

```cypher
// Average citations by venue
MATCH (p:Paper)-[:PUBLISHED_IN]->(v:Venue) 
RETURN v.name, 
       count(p) as paper_count,
       avg(p.citation_count) as avg_citations,
       max(p.citation_count) as max_citations
ORDER BY avg_citations DESC;
```

### Topic Analysis

```cypher
// Most popular research topics
MATCH (p:Paper)-[:ABOUT]->(t:Topic) 
RETURN t.name, count(p) as papers_on_topic
ORDER BY papers_on_topic DESC;
```

```cypher
// Topics by total citation impact
MATCH (p:Paper)-[:ABOUT]->(t:Topic) 
RETURN t.name, 
       count(p) as papers,
       sum(p.citation_count) as total_citations,
       avg(p.citation_count) as avg_citations
ORDER BY total_citations DESC;
```

## Part 5: Advanced GraphRAG Queries

### Multi-Hop Reasoning

These queries show GraphRAG's power for complex questions:

```cypher
// "Find research collaborations between Stanford and MIT"
MATCH (p:Paper)<-[:AUTHORED]-(a1:Author)-[:AFFILIATED_WITH]->(i1:Institution {name: "Stanford University"}),
      (p)<-[:AUTHORED]-(a2:Author)-[:AFFILIATED_WITH]->(i2:Institution {name: "Massachusetts Institute of Technology"})
WHERE a1 <> a2
RETURN p.title as collaborative_paper,
       collect(a1.name) as stanford_authors,
       collect(a2.name) as mit_authors,
       p.year, p.citation_count
ORDER BY p.citation_count DESC;
```

```cypher
// "Who are the Knowledge Graph experts and where do they work?"
MATCH (a:Author)-[:AUTHORED]->(p:Paper)-[:ABOUT]->(t:Topic {name: "Knowledge Graphs"}),
      (a)-[:AFFILIATED_WITH]->(i:Institution)
RETURN a.name, 
       i.name as institution,
       count(p) as kg_papers,
       sum(p.citation_count) as total_kg_citations,
       a.h_index
ORDER BY total_kg_citations DESC;
```

### Citation Influence Networks

```cypher
// "Which papers influenced GraphRAG research?"
MATCH (source:Paper)-[:CITES*1..2]->(target:Paper)
WHERE source.title CONTAINS "GraphRAG" OR target.title CONTAINS "GraphRAG"
RETURN source.title, target.title, 
       length(path) as citation_distance,
       target.citation_count
ORDER BY target.citation_count DESC;
```

### Cross-Topic Discovery

```cypher
// "Find connections between different research areas"
MATCH (p1:Paper)-[:ABOUT]->(t1:Topic),
      (p1)-[:CITES]->(p2:Paper)-[:ABOUT]->(t2:Topic)
WHERE t1 <> t2
RETURN t1.name as citing_topic, 
       t2.name as cited_topic,
       count(*) as connection_strength
ORDER BY connection_strength DESC;
```

### Author Network Analysis

```cypher
// "Find research communities through co-authorship"
MATCH (a1:Author)-[:AUTHORED]->(p:Paper)<-[:AUTHORED]-(a2:Author)
WHERE a1 <> a2
RETURN a1.name, a2.name, 
       count(p) as shared_papers,
       collect(p.title) as collaboration_papers
ORDER BY shared_papers DESC;
```

## Part 6: Complex Analytical Queries

### Venue Impact Analysis

```cypher
// "Which venues publish the most impactful research in each topic?"
MATCH (p:Paper)-[:PUBLISHED_IN]->(v:Venue),
      (p)-[:ABOUT]->(t:Topic)
WITH v, t, count(p) as papers, avg(p.citation_count) as avg_impact
WHERE papers > 0
RETURN v.name as venue, 
       t.name as topic,
       papers,
       round(avg_impact, 1) as avg_citations_per_paper
ORDER BY avg_impact DESC;
```

### Temporal Analysis

```cypher
// "How has research focus changed over time?"
MATCH (p:Paper)-[:ABOUT]->(t:Topic)
RETURN p.year, 
       t.name as topic,
       count(p) as papers_that_year,
       avg(p.citation_count) as avg_citations
ORDER BY p.year, avg_citations DESC;
```

### Research Impact Pathways

```cypher
// "Trace how ideas flow through the research community"
MATCH path = (start:Paper)-[:CITES*1..3]->(end:Paper)
WHERE start.year > end.year // Ensure chronological order
RETURN start.title as recent_paper,
       end.title as foundational_paper,
       length(path) as citation_hops,
       start.year - end.year as years_apart,
       end.citation_count as foundation_impact
ORDER BY foundation_impact DESC, years_apart DESC
LIMIT 10;
```

## Part 7: Graph Visualization Queries

For use in Neo4j Browser (http://localhost:7474):

```cypher
// Visualize the complete knowledge graph structure
MATCH (n)-[r]->(m) 
RETURN n, r, m 
LIMIT 50;
```

```cypher
// Focus on GraphRAG research network
MATCH (p:Paper)-[r]-(n)
WHERE p.title CONTAINS "GraphRAG" OR p.title CONTAINS "Knowledge Graph"
RETURN p, r, n;
```

```cypher
// Show author collaboration network
MATCH (a1:Author)-[:AUTHORED]->(p:Paper)<-[:AUTHORED]-(a2:Author)
RETURN a1, p, a2
LIMIT 20;
```

## Key Cypher Concepts Learned

1. **MATCH**: Find patterns in the graph
2. **WHERE**: Filter results based on conditions  
3. **RETURN**: Specify what data to return
4. **Relationships**: Use `-[:RELATIONSHIP_TYPE]->` syntax
5. **Properties**: Access with `node.property` syntax
6. **Aggregation**: `count()`, `sum()`, `avg()`, `collect()`
7. **Path patterns**: Variable-length paths with `*1..3`
8. **ORDER BY**: Sort results
9. **LIMIT**: Restrict number of results

## Why This Matters for GraphRAG

These queries demonstrate GraphRAG's advantages:

- **Multi-hop reasoning**: "Find Stanford-MIT collaborations" requires 3+ relationship traversals
- **Context discovery**: Citation networks reveal research influence paths
- **Relationship-aware search**: Traditional search can't find "papers by X's collaborators"
- **Complex analytics**: Cross-topic connections and temporal analysis

Traditional vector-based RAG would struggle with these relationship-rich queries, while graph-based retrieval handles them naturally.

## Next Steps

1. Try modifying these queries with different filters
2. Explore the graph visually in Neo4j Browser
3. Build custom queries for your research questions
4. Proceed to GraphDB MCP Server development to integrate with LLMs

Happy querying! 🔍📊