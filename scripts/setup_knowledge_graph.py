#!/usr/bin/env python3
"""
Setup Knowledge Graph for GraphRAG Demonstration
Loads schema and sample data into Neo4j
"""

import os
import sys
from pathlib import Path
from neo4j import GraphDatabase
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeGraphSetup:
    def __init__(self, uri=None, user=None, password=None):
        """Initialize Neo4j connection using environment variables"""
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER")
        self.password = password or os.getenv("NEO4J_PASSWORD")
        
        if not self.user or not self.password:
            raise ValueError("NEO4J_USER and NEO4J_PASSWORD environment variables must be set")
        
        logger.info(f"Connecting to Neo4j at {self.uri} as {self.user}")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        
    def close(self):
        """Close the connection"""
        self.driver.close()
    
    def run_cypher_file(self, file_path):
        """Execute a Cypher script file"""
        logger.info(f"Executing Cypher script: {file_path}")
        
        try:
            with open(file_path, 'r') as file:
                cypher_content = file.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in cypher_content.split(';') if stmt.strip()]
            
            with self.driver.session() as session:
                for i, statement in enumerate(statements):
                    if statement:
                        try:
                            result = session.run(statement)
                            logger.debug(f"Statement {i+1} executed successfully")
                        except Exception as e:
                            logger.error(f"Error in statement {i+1}: {e}")
                            logger.error(f"Statement: {statement[:100]}...")
                            
            logger.info(f"Completed executing {file_path}")
            
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error executing {file_path}: {e}")
            raise
    
    def verify_setup(self):
        """Verify the knowledge graph was created correctly"""
        logger.info("Verifying knowledge graph setup...")
        
        queries = [
            ("Papers", "MATCH (p:Paper) RETURN count(p) as count"),
            ("Authors", "MATCH (a:Author) RETURN count(a) as count"),
            ("Institutions", "MATCH (i:Institution) RETURN count(i) as count"),
            ("Topics", "MATCH (t:Topic) RETURN count(t) as count"),
            ("Venues", "MATCH (v:Venue) RETURN count(v) as count"),
            ("Relationships", "MATCH ()-[r]->() RETURN count(r) as count")
        ]
        
        with self.driver.session() as session:
            for name, query in queries:
                result = session.run(query)
                count = result.single()["count"]
                logger.info(f"{name}: {count}")
        
        logger.info("Knowledge graph verification complete!")

def main():
    """Main setup function"""
    # Get script directory
    script_dir = Path(__file__).parent
    
    try:
        # Setup KG
        kg_setup = KnowledgeGraphSetup()
        
        # Test connection
        logger.info("Testing Neo4j connection...")
        with kg_setup.driver.session() as session:
            result = session.run("RETURN 'Connection successful' as message")
            message = result.single()["message"]
            logger.info(f"✅ {message}")
        
        # Execute schema creation
        schema_file = script_dir / "01_create_schema.cypher"
        kg_setup.run_cypher_file(schema_file)
        
        # Execute data population
        data_file = script_dir / "02_populate_data.cypher"
        kg_setup.run_cypher_file(data_file)
        
        # Verify setup
        kg_setup.verify_setup()
        
        logger.info("🎉 Knowledge graph setup complete!")
        logger.info("You can now:")
        logger.info("1. View the graph in Neo4j Browser: http://localhost:7474")
        logger.info("2. Run sample queries with: python scripts/query_graph.py")
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please set NEO4J_USER and NEO4J_PASSWORD environment variables")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        sys.exit(1)
    finally:
        if 'kg_setup' in locals():
            kg_setup.close()

if __name__ == "__main__":
    main()