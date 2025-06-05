#!/usr/bin/env python3
"""
GraphRAG Knowledge Graph Query Demonstration
Shows sample queries that demonstrate graph-based retrieval advantages
"""

import os
import json
from neo4j import GraphDatabase
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphQuerier:
    def __init__(self):
        """Initialize Neo4j connection using environment variables"""
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER")
        self.password = os.getenv("NEO4J_PASSWORD")
        
        if not self.user or not self.password:
            raise ValueError("NEO4J_USER and NEO4J_PASSWORD environment variables must be set")
        
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
    
    def close(self):
        """Close the connection"""
        self.driver.close()
    
    def execute_query(self, query, description=""):
        """Execute a query and return results"""
        logger.info(f"Executing: {description}")
        logger.info(f"Query: {query}")
        
        with self.driver.session() as session:
            result = session.run(query)
            records = [record.data() for record in result]
            
        logger.info(f"Results: {len(records)} records found")
        return records
    
    def print_results(self, results, max_items=10):
        """Pretty print query results"""
        for i, record in enumerate(results[:max_items]):
            print(f"  {i+1}. {json.dumps(record, indent=2, default=str)}")
        
        if len(results) > max_items:
            print(f"  ... and {len(results) - max_items} more")
        print()

def demonstrate_graphrag_queries():
    """Demonstrate GraphRAG-style queries that show graph advantages"""
    
    querier = GraphQuerier()
    
    print("🔍 GraphRAG Knowledge Graph Query Demonstration")
    print("=" * 60)
    
    try:
        # Query 1: Multi-hop reasoning - Find papers by institution collaboration
        print("\n1. MULTI-HOP REASONING: Papers from Stanford-MIT collaborations")
        print("-" * 60)
        query1 = """
        MATCH (p:Paper)<-[:AUTHORED]-(a1:Author)-[:AFFILIATED_WITH]->(i1:Institution {name: "Stanford University"})
        MATCH (p)<-[:AUTHORED]-(a2:Author)-[:AFFILIATED_WITH]->(i2:Institution {name: "Massachusetts Institute of Technology"})
        WHERE a1 <> a2
        RETURN p.title as paper_title, 
               collect(DISTINCT a1.name) as stanford_authors,
               collect(DISTINCT a2.name) as mit_authors,
               p.year as year, p.citation_count as citations
        """
        results1 = querier.execute_query(query1, "Stanford-MIT collaboration papers")
        querier.print_results(results1)
        
        # Query 2: Topic-based discovery with citations
        print("2. TOPIC DISCOVERY: GraphRAG papers and their citation network")
        print("-" * 60)
        query2 = """
        MATCH (p:Paper)-[:ABOUT]->(t:Topic {name: "Retrieval-Augmented Generation"})
        OPTIONAL MATCH (p)<-[:CITES]-(citing:Paper)
        OPTIONAL MATCH (p)-[:CITES]->(cited:Paper)
        RETURN p.title as paper_title,
               p.abstract as abstract,
               collect(DISTINCT citing.title) as cited_by,
               collect(DISTINCT cited.title) as cites,
               p.citation_count as total_citations
        ORDER BY p.citation_count DESC
        """
        results2 = querier.execute_query(query2, "RAG topic exploration")
        querier.print_results(results2, max_items=3)
        
        # Query 3: Author expertise and influence
        print("3. AUTHOR EXPERTISE: Most influential authors in Knowledge Graphs")
        print("-" * 60)
        query3 = """
        MATCH (a:Author)-[:AUTHORED]->(p:Paper)-[:ABOUT]->(t:Topic {name: "Knowledge Graphs"})
        MATCH (a)-[:AFFILIATED_WITH]->(i:Institution)
        WITH a, i, count(p) as papers_count, sum(p.citation_count) as total_citations
        RETURN a.name as author_name,
               a.h_index as h_index,
               i.name as institution,
               papers_count as kg_papers,
               total_citations as kg_citations
        ORDER BY total_citations DESC
        """
        results3 = querier.execute_query(query3, "Knowledge graph author expertise")
        querier.print_results(results3)
        
        # Query 4: Venue impact analysis
        print("4. VENUE ANALYSIS: Research impact by publication venue")
        print("-" * 60)
        query4 = """
        MATCH (p:Paper)-[:PUBLISHED_IN]->(v:Venue)
        MATCH (p)-[:ABOUT]->(t:Topic)
        WITH v, t, count(p) as paper_count, avg(p.citation_count) as avg_citations
        WHERE paper_count > 0
        RETURN v.name as venue_name,
               v.type as venue_type,
               collect(DISTINCT t.name) as topics_covered,
               paper_count as papers_published,
               round(avg_citations, 2) as avg_citations_per_paper
        ORDER BY avg_citations_per_paper DESC
        """
        results4 = querier.execute_query(query4, "Venue impact analysis")
        querier.print_results(results4)
        
        # Query 5: Related topic discovery
        print("5. TOPIC RELATIONSHIPS: Related research areas")
        print("-" * 60)
        query5 = """
        MATCH (t1:Topic)-[:RELATED_TO]-(t2:Topic)
        MATCH (p1:Paper)-[:ABOUT]->(t1)
        MATCH (p2:Paper)-[:ABOUT]->(t2)
        WITH t1, t2, count(DISTINCT p1) as t1_papers, count(DISTINCT p2) as t2_papers
        RETURN t1.name as topic_1,
               t2.name as topic_2,
               t1_papers as papers_topic_1,
               t2_papers as papers_topic_2
        ORDER BY t1_papers DESC, t2_papers DESC
        """
        results5 = querier.execute_query(query5, "Topic relationship exploration")
        querier.print_results(results5)
        
        # Query 6: Citation network analysis
        print("6. CITATION NETWORK: Paper influence paths")
        print("-" * 60)
        query6 = """
        MATCH path = (p1:Paper)-[:CITES*1..2]->(p2:Paper)
        WHERE p1.title CONTAINS "GraphRAG" OR p2.title CONTAINS "GraphRAG"
        WITH p1, p2, length(path) as citation_distance
        RETURN p1.title as citing_paper,
               p2.title as cited_paper,
               citation_distance,
               p1.year as citing_year,
               p2.year as cited_year
        ORDER BY citation_distance, citing_year DESC
        """
        results6 = querier.execute_query(query6, "Citation network analysis")
        querier.print_results(results6)
        
        print("\n🎉 GraphRAG Query Demonstration Complete!")
        print("These queries show how graph structure enables:")
        print("• Multi-hop reasoning across relationships")
        print("• Context-aware discovery through graph traversal") 
        print("• Complex analytical queries combining multiple entity types")
        print("• Citation and influence network analysis")
        print("\nThis demonstrates why GraphRAG can be more effective than")
        print("traditional vector-based RAG for complex, relationship-rich queries.")
        
    except Exception as e:
        logger.error(f"Query demonstration failed: {e}")
        raise
    finally:
        querier.close()

if __name__ == "__main__":
    demonstrate_graphrag_queries()