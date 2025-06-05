#!/usr/bin/env python3
"""
Clear Knowledge Graph Data
Removes all data populated by 02_populate_data.cypher while preserving schema
"""

import os
import sys
from pathlib import Path
from neo4j import GraphDatabase
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeGraphCleaner:
    def __init__(self):
        """Initialize Neo4j connection using environment variables"""
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER")
        self.password = os.getenv("NEO4J_PASSWORD")
        
        if not self.user or not self.password:
            raise ValueError("NEO4J_USER and NEO4J_PASSWORD environment variables must be set")
        
        logger.info(f"Connecting to Neo4j at {self.uri} as {self.user}")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
    
    def close(self):
        """Close the connection"""
        self.driver.close()
    
    def count_data(self):
        """Count current nodes and relationships"""
        with self.driver.session() as session:
            # Count nodes
            node_result = session.run("MATCH (n) RETURN count(n) as count")
            node_count = node_result.single()["count"]
            
            # Count relationships
            rel_result = session.run("MATCH ()-[r]-() RETURN count(r) as count")
            rel_count = rel_result.single()["count"]
            
            return node_count, rel_count
    
    def clear_all_data(self):
        """Remove all nodes and relationships but preserve schema"""
        logger.info("Clearing all data from knowledge graph...")
        
        with self.driver.session() as session:
            # Remove all relationships first
            logger.info("Removing all relationships...")
            result = session.run("MATCH ()-[r]-() DELETE r")
            
            # Remove all nodes
            logger.info("Removing all nodes...")
            result = session.run("MATCH (n) DELETE n")
            
        logger.info("Data clearing complete!")
    
    def verify_cleanup(self):
        """Verify that all data has been removed"""
        logger.info("Verifying cleanup...")
        
        node_count, rel_count = self.count_data()
        
        if node_count == 0 and rel_count == 0:
            logger.info("✅ All data successfully removed")
            logger.info("📋 Schema (constraints and indexes) preserved")
        else:
            logger.warning(f"⚠️  Cleanup incomplete: {node_count} nodes, {rel_count} relationships remain")
        
        # Show preserved schema
        with self.driver.session() as session:
            try:
                # Count constraints
                constraints_result = session.run("SHOW CONSTRAINTS")
                constraints = list(constraints_result)
                logger.info(f"📝 {len(constraints)} constraints preserved")
                
                # Count indexes  
                indexes_result = session.run("SHOW INDEXES")
                indexes = list(indexes_result)
                logger.info(f"🔍 {len(indexes)} indexes preserved")
                
            except Exception as e:
                logger.debug(f"Could not show schema info: {e}")

def main():
    """Main cleanup function"""
    
    try:
        # Initialize cleaner
        cleaner = KnowledgeGraphCleaner()
        
        # Test connection
        logger.info("Testing Neo4j connection...")
        with cleaner.driver.session() as session:
            result = session.run("RETURN 'Connection successful' as message")
            message = result.single()["message"]
            logger.info(f"✅ {message}")
        
        # Show current state
        node_count, rel_count = cleaner.count_data()
        logger.info(f"Current state: {node_count} nodes, {rel_count} relationships")
        
        if node_count == 0 and rel_count == 0:
            logger.info("📭 Database is already empty")
            return
        
        # Confirm deletion
        response = input(f"\n⚠️  This will DELETE all {node_count} nodes and {rel_count} relationships.\nSchema (constraints/indexes) will be preserved.\nContinue? [y/N]: ")
        
        if response.lower() != 'y':
            logger.info("❌ Cleanup cancelled")
            return
        
        # Perform cleanup
        cleaner.clear_all_data()
        cleaner.verify_cleanup()
        
        logger.info("\n🎉 Knowledge graph cleanup complete!")
        logger.info("To repopulate data, run: python scripts/setup_knowledge_graph.py")
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please set NEO4J_USER and NEO4J_PASSWORD environment variables")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        sys.exit(1)
    finally:
        if 'cleaner' in locals():
            cleaner.close()

if __name__ == "__main__":
    main()