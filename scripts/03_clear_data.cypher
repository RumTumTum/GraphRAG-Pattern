// Clear All Data from GraphRAG Knowledge Graph
// Removes all nodes and relationships created by 02_populate_data.cypher
// Keeps schema (constraints and indexes) intact

// Remove all relationships first (Neo4j requirement)
MATCH ()-[r]-()
DELETE r;

// Remove all nodes
MATCH (n)
DELETE n;

// Verify deletion
MATCH (n) RETURN count(n) as remaining_nodes;
MATCH ()-[r]-() RETURN count(r) as remaining_relationships;

// Note: Constraints and indexes are preserved
// To see remaining schema elements:
// SHOW CONSTRAINTS;
// SHOW INDEXES;