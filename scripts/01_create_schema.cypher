// GraphRAG Academic Research Ontology
// Schema definition for demonstrating graph-based retrieval

// Clear existing data (for development)
MATCH (n) DETACH DELETE n;

// Create constraints and indexes for performance
CREATE CONSTRAINT paper_id IF NOT EXISTS FOR (p:Paper) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT author_id IF NOT EXISTS FOR (a:Author) REQUIRE a.id IS UNIQUE;
CREATE CONSTRAINT institution_id IF NOT EXISTS FOR (i:Institution) REQUIRE i.id IS UNIQUE;
CREATE CONSTRAINT venue_id IF NOT EXISTS FOR (v:Venue) REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT topic_id IF NOT EXISTS FOR (t:Topic) REQUIRE t.id IS UNIQUE;

// Create indexes for search performance
CREATE INDEX paper_title IF NOT EXISTS FOR (p:Paper) ON (p.title);
CREATE INDEX author_name IF NOT EXISTS FOR (a:Author) ON (a.name);
CREATE INDEX institution_name IF NOT EXISTS FOR (i:Institution) ON (i.name);
CREATE INDEX topic_name IF NOT EXISTS FOR (t:Topic) ON (t.name);

// Schema is now ready for data population