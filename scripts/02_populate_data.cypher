// Populate GraphRAG Academic Research Knowledge Graph
// Sample data focused on AI/ML research for demonstration

// Create Institutions
CREATE (:Institution {
    id: "stanford", 
    name: "Stanford University", 
    country: "USA",
    type: "University"
});

CREATE (:Institution {
    id: "mit", 
    name: "Massachusetts Institute of Technology", 
    country: "USA",
    type: "University"
});

CREATE (:Institution {
    id: "deepmind", 
    name: "DeepMind", 
    country: "UK",
    type: "Research Lab"
});

CREATE (:Institution {
    id: "openai", 
    name: "OpenAI", 
    country: "USA",
    type: "Research Lab"
});

// Create Venues
CREATE (:Venue {
    id: "neurips", 
    name: "Neural Information Processing Systems", 
    type: "Conference",
    abbreviation: "NeurIPS"
});

CREATE (:Venue {
    id: "icml", 
    name: "International Conference on Machine Learning", 
    type: "Conference",
    abbreviation: "ICML"
});

CREATE (:Venue {
    id: "nature", 
    name: "Nature", 
    type: "Journal",
    impact_factor: 49.962
});

CREATE (:Venue {
    id: "arxiv", 
    name: "arXiv", 
    type: "Preprint",
    abbreviation: "arXiv"
});

// Create Topics
CREATE (:Topic {id: "knowledge_graphs", name: "Knowledge Graphs"});
CREATE (:Topic {id: "graph_neural_networks", name: "Graph Neural Networks"});
CREATE (:Topic {id: "retrieval_augmented_generation", name: "Retrieval-Augmented Generation"});
CREATE (:Topic {id: "large_language_models", name: "Large Language Models"});
CREATE (:Topic {id: "information_retrieval", name: "Information Retrieval"});
CREATE (:Topic {id: "natural_language_processing", name: "Natural Language Processing"});
CREATE (:Topic {id: "machine_learning", name: "Machine Learning"});
CREATE (:Topic {id: "graph_embeddings", name: "Graph Embeddings"});

// Create Authors
CREATE (:Author {
    id: "smith_j", 
    name: "Jane Smith", 
    h_index: 45,
    total_citations: 8920
});

CREATE (:Author {
    id: "chen_l", 
    name: "Li Chen", 
    h_index: 38,
    total_citations: 6750
});

CREATE (:Author {
    id: "johnson_m", 
    name: "Michael Johnson", 
    h_index: 52,
    total_citations: 12400
});

CREATE (:Author {
    id: "garcia_a", 
    name: "Ana Garcia", 
    h_index: 33,
    total_citations: 4890
});

CREATE (:Author {
    id: "patel_r", 
    name: "Raj Patel", 
    h_index: 28,
    total_citations: 3200
});

CREATE (:Author {
    id: "kim_s", 
    name: "Sarah Kim", 
    h_index: 41,
    total_citations: 7650
});

// Create Papers
CREATE (:Paper {
    id: "graphrag_survey_2023", 
    title: "Graph-Based Retrieval-Augmented Generation: A Comprehensive Survey",
    abstract: "This paper presents a comprehensive survey of graph-based approaches to retrieval-augmented generation, comparing traditional vector-based RAG with knowledge graph-enhanced methods.",
    year: 2023,
    citation_count: 127,
    doi: "10.1000/graphrag2023"
});

CREATE (:Paper {
    id: "kg_llm_integration_2024", 
    title: "Integrating Knowledge Graphs with Large Language Models for Enhanced Reasoning",
    abstract: "We propose novel methods for integrating structured knowledge graphs with pre-trained language models to improve reasoning capabilities in complex domains.",
    year: 2024,
    citation_count: 89,
    doi: "10.1000/kgllm2024"
});

CREATE (:Paper {
    id: "gnn_retrieval_2023", 
    title: "Graph Neural Networks for Scalable Information Retrieval",
    abstract: "This work introduces graph neural network architectures optimized for large-scale information retrieval tasks, demonstrating superior performance over traditional methods.",
    year: 2023,
    citation_count: 203,
    doi: "10.1000/gnnret2023"
});

CREATE (:Paper {
    id: "rag_limitations_2024", 
    title: "Understanding the Limitations of Retrieval-Augmented Generation",
    abstract: "An empirical analysis of current RAG systems, identifying key limitations and proposing graph-based solutions for multi-hop reasoning tasks.",
    year: 2024,
    citation_count: 156,
    doi: "10.1000/raglim2024"
});

CREATE (:Paper {
    id: "graph_embeddings_nlp_2023", 
    title: "Graph Embeddings for Natural Language Processing: Methods and Applications",
    abstract: "A comprehensive review of graph embedding techniques applied to NLP tasks, with focus on knowledge-aware language understanding.",
    year: 2023,
    citation_count: 445,
    doi: "10.1000/graphemb2023"
});

CREATE (:Paper {
    id: "knowledge_reasoning_llm_2024", 
    title: "Knowledge-Aware Reasoning in Large Language Models",
    abstract: "We investigate how external knowledge graphs can be leveraged to improve reasoning capabilities in large language models across diverse domains.",
    year: 2024,
    citation_count: 78,
    doi: "10.1000/kgreas2024"
});

// Create Author-Institution Affiliations
MATCH (a:Author {id: "smith_j"}), (i:Institution {id: "stanford"})
CREATE (a)-[:AFFILIATED_WITH {start_year: 2020}]->(i);

MATCH (a:Author {id: "chen_l"}), (i:Institution {id: "mit"})
CREATE (a)-[:AFFILIATED_WITH {start_year: 2018}]->(i);

MATCH (a:Author {id: "johnson_m"}), (i:Institution {id: "deepmind"})
CREATE (a)-[:AFFILIATED_WITH {start_year: 2021}]->(i);

MATCH (a:Author {id: "garcia_a"}), (i:Institution {id: "stanford"})
CREATE (a)-[:AFFILIATED_WITH {start_year: 2019}]->(i);

MATCH (a:Author {id: "patel_r"}), (i:Institution {id: "openai"})
CREATE (a)-[:AFFILIATED_WITH {start_year: 2022}]->(i);

MATCH (a:Author {id: "kim_s"}), (i:Institution {id: "mit"})
CREATE (a)-[:AFFILIATED_WITH {start_year: 2020}]->(i);

// Create Author-Paper relationships
MATCH (a:Author {id: "smith_j"}), (p:Paper {id: "graphrag_survey_2023"})
CREATE (a)-[:AUTHORED {role: "first_author"}]->(p);

MATCH (a:Author {id: "garcia_a"}), (p:Paper {id: "graphrag_survey_2023"})
CREATE (a)-[:AUTHORED {role: "co_author"}]->(p);

MATCH (a:Author {id: "chen_l"}), (p:Paper {id: "kg_llm_integration_2024"})
CREATE (a)-[:AUTHORED {role: "first_author"}]->(p);

MATCH (a:Author {id: "kim_s"}), (p:Paper {id: "kg_llm_integration_2024"})
CREATE (a)-[:AUTHORED {role: "co_author"}]->(p);

MATCH (a:Author {id: "johnson_m"}), (p:Paper {id: "gnn_retrieval_2023"})
CREATE (a)-[:AUTHORED {role: "first_author"}]->(p);

MATCH (a:Author {id: "patel_r"}), (p:Paper {id: "rag_limitations_2024"})
CREATE (a)-[:AUTHORED {role: "first_author"}]->(p);

MATCH (a:Author {id: "smith_j"}), (p:Paper {id: "rag_limitations_2024"})
CREATE (a)-[:AUTHORED {role: "co_author"}]->(p);

MATCH (a:Author {id: "garcia_a"}), (p:Paper {id: "graph_embeddings_nlp_2023"})
CREATE (a)-[:AUTHORED {role: "first_author"}]->(p);

MATCH (a:Author {id: "chen_l"}), (p:Paper {id: "graph_embeddings_nlp_2023"})
CREATE (a)-[:AUTHORED {role: "co_author"}]->(p);

MATCH (a:Author {id: "kim_s"}), (p:Paper {id: "knowledge_reasoning_llm_2024"})
CREATE (a)-[:AUTHORED {role: "first_author"}]->(p);

// Create Paper-Venue relationships
MATCH (p:Paper {id: "graphrag_survey_2023"}), (v:Venue {id: "arxiv"})
CREATE (p)-[:PUBLISHED_IN {year: 2023}]->(v);

MATCH (p:Paper {id: "kg_llm_integration_2024"}), (v:Venue {id: "neurips"})
CREATE (p)-[:PUBLISHED_IN {year: 2024}]->(v);

MATCH (p:Paper {id: "gnn_retrieval_2023"}), (v:Venue {id: "icml"})
CREATE (p)-[:PUBLISHED_IN {year: 2023}]->(v);

MATCH (p:Paper {id: "rag_limitations_2024"}), (v:Venue {id: "arxiv"})
CREATE (p)-[:PUBLISHED_IN {year: 2024}]->(v);

MATCH (p:Paper {id: "graph_embeddings_nlp_2023"}), (v:Venue {id: "nature"})
CREATE (p)-[:PUBLISHED_IN {year: 2023}]->(v);

MATCH (p:Paper {id: "knowledge_reasoning_llm_2024"}), (v:Venue {id: "neurips"})
CREATE (p)-[:PUBLISHED_IN {year: 2024}]->(v);

// Create Paper-Topic relationships
MATCH (p:Paper {id: "graphrag_survey_2023"}), (t:Topic {id: "knowledge_graphs"})
CREATE (p)-[:ABOUT {relevance: 0.9}]->(t);

MATCH (p:Paper {id: "graphrag_survey_2023"}), (t:Topic {id: "retrieval_augmented_generation"})
CREATE (p)-[:ABOUT {relevance: 0.95}]->(t);

MATCH (p:Paper {id: "kg_llm_integration_2024"}), (t:Topic {id: "knowledge_graphs"})
CREATE (p)-[:ABOUT {relevance: 0.85}]->(t);

MATCH (p:Paper {id: "kg_llm_integration_2024"}), (t:Topic {id: "large_language_models"})
CREATE (p)-[:ABOUT {relevance: 0.9}]->(t);

MATCH (p:Paper {id: "gnn_retrieval_2023"}), (t:Topic {id: "graph_neural_networks"})
CREATE (p)-[:ABOUT {relevance: 0.95}]->(t);

MATCH (p:Paper {id: "gnn_retrieval_2023"}), (t:Topic {id: "information_retrieval"})
CREATE (p)-[:ABOUT {relevance: 0.8}]->(t);

MATCH (p:Paper {id: "rag_limitations_2024"}), (t:Topic {id: "retrieval_augmented_generation"})
CREATE (p)-[:ABOUT {relevance: 0.9}]->(t);

MATCH (p:Paper {id: "graph_embeddings_nlp_2023"}), (t:Topic {id: "graph_embeddings"})
CREATE (p)-[:ABOUT {relevance: 0.95}]->(t);

MATCH (p:Paper {id: "graph_embeddings_nlp_2023"}), (t:Topic {id: "natural_language_processing"})
CREATE (p)-[:ABOUT {relevance: 0.8}]->(t);

MATCH (p:Paper {id: "knowledge_reasoning_llm_2024"}), (t:Topic {id: "large_language_models"})
CREATE (p)-[:ABOUT {relevance: 0.85}]->(t);

MATCH (p:Paper {id: "knowledge_reasoning_llm_2024"}), (t:Topic {id: "knowledge_graphs"})
CREATE (p)-[:ABOUT {relevance: 0.8}]->(t);

// Create Citation relationships (papers citing other papers)
MATCH (p1:Paper {id: "kg_llm_integration_2024"}), (p2:Paper {id: "graphrag_survey_2023"})
CREATE (p1)-[:CITES {context: "foundational survey"}]->(p2);

MATCH (p1:Paper {id: "rag_limitations_2024"}), (p2:Paper {id: "graphrag_survey_2023"})
CREATE (p1)-[:CITES {context: "comparison methodology"}]->(p2);

MATCH (p1:Paper {id: "kg_llm_integration_2024"}), (p2:Paper {id: "graph_embeddings_nlp_2023"})
CREATE (p1)-[:CITES {context: "embedding techniques"}]->(p2);

MATCH (p1:Paper {id: "knowledge_reasoning_llm_2024"}), (p2:Paper {id: "kg_llm_integration_2024"})
CREATE (p1)-[:CITES {context: "integration methods"}]->(p2);

MATCH (p1:Paper {id: "rag_limitations_2024"}), (p2:Paper {id: "gnn_retrieval_2023"})
CREATE (p1)-[:CITES {context: "retrieval performance"}]->(p2);

// Create Topic relationships
MATCH (t1:Topic {id: "knowledge_graphs"}), (t2:Topic {id: "graph_embeddings"})
CREATE (t1)-[:RELATED_TO {strength: 0.8}]->(t2);

MATCH (t1:Topic {id: "retrieval_augmented_generation"}), (t2:Topic {id: "information_retrieval"})
CREATE (t1)-[:RELATED_TO {strength: 0.9}]->(t2);

MATCH (t1:Topic {id: "graph_neural_networks"}), (t2:Topic {id: "machine_learning"})
CREATE (t1)-[:RELATED_TO {strength: 0.7}]->(t2);

MATCH (t1:Topic {id: "large_language_models"}), (t2:Topic {id: "natural_language_processing"})
CREATE (t1)-[:RELATED_TO {strength: 0.85}]->(t2);

MATCH (t1:Topic {id: "knowledge_graphs"}), (t2:Topic {id: "natural_language_processing"})
CREATE (t1)-[:RELATED_TO {strength: 0.6}]->(t2);