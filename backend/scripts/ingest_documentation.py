"""
Documentation Ingestion Script
Indexes hackathon rules, Google Cloud docs, and Elastic docs for RAG
"""

import asyncio
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import json
from datetime import datetime
import sys
import os
from urllib.parse import urljoin, urlparse

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.elastic_service import ElasticService
from app.services.vertex_service import VertexService
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentationScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_hackathon_rules(self) -> List[Dict[str, Any]]:
        """Scrape hackathon rules and guidelines"""
        documents = []
        
        # AI Accelerate Hackathon specific rules
        hackathon_docs = [
            {
                "title": "AI Accelerate Hackathon Rules",
                "content": """
                AI Accelerate: Unlocking New Frontiers - Multi-Partner Google Cloud Hackathon
                
                REQUIREMENTS:
                - Build a new working application that tackles challenges provided by partners
                - Must integrate both Google Cloud products (Vertex AI, Gemini, etc.) and partner technologies
                - Elastic Challenge: Build AI-Powered Search using Elastic's hybrid search capabilities
                - Must deliver intelligent, interactive, and context-aware solution
                
                SUBMISSION REQUIREMENTS:
                - Include URL to hosted project for judging and testing
                - Include URL to open source code repository with all necessary source code
                - Repository must be public with open source license file
                - Include demo video (3 minutes maximum) uploaded to YouTube or Vimeo
                - Complete Devpost submission form
                
                JUDGING CRITERIA:
                - Technological Implementation: Quality software development with Google Cloud and Partner services
                - Design: User experience and design quality
                - Potential Impact: Impact on target communities
                - Quality of the Idea: Creativity and uniqueness
                
                PRIZES:
                - Elastic Challenge First Place: $12,500 USD + social media promotion
                - Elastic Challenge Second Place: $7,500 USD
                - Elastic Challenge Third Place: $5,000 USD
                """,
                "url": "https://ai-accelerate-hackathon.devpost.com/rules",
                "section": "rules",
                "source": "hackathon"
            },
            {
                "title": "Elastic Challenge Requirements",
                "content": """
                Elastic Challenge: Build the Future of AI-Powered Search
                
                REQUIREMENTS:
                - Use Elastic's hybrid search capabilities
                - Seamless integration with Google Cloud's generative AI tools
                - Build conversational and/or agent-based solution
                - Transform how people interact with data
                - Deliver intelligent, interactive, and context-aware solution
                - Showcase how Elastic + Google Cloud can reimagine daily life activities or business processes
                
                TECHNICAL REQUIREMENTS:
                - Elastic Cloud deployment
                - Vector search capabilities
                - Keyword search integration
                - Hybrid search scoring
                - Google Cloud Vertex AI integration
                - Gemini Pro for conversational AI
                
                SOLUTION FOCUS:
                - Relevant to modern AI/data including LLMs, agentic apps, RAG, automation, augmented analytics
                """,
                "url": "https://ai-accelerate-hackathon.devpost.com/details/elastic-challenge",
                "section": "challenge_requirements",
                "source": "hackathon"
            }
        ]
        
        documents.extend(hackathon_docs)
        return documents
    
    def scrape_google_cloud_docs(self) -> List[Dict[str, Any]]:
        """Scrape relevant Google Cloud documentation"""
        documents = []
        
        # Key Google Cloud documentation sections
        gcp_docs = [
            {
                "title": "Vertex AI Overview",
                "content": """
                Google Cloud Vertex AI is a unified ML platform that brings together Google Cloud services for building ML under one unified UI and API.
                
                KEY FEATURES:
                - AutoML and custom training
                - Model deployment and serving
                - MLOps capabilities
                - Pre-trained APIs
                - Generative AI models including Gemini Pro
                
                VERTEX AI SERVICES:
                - Vertex AI Workbench: Jupyter-based notebooks
                - Vertex AI Training: Custom model training
                - Vertex AI Prediction: Model serving
                - Vertex AI Pipelines: ML workflow orchestration
                - Model Garden: Pre-trained models
                - Generative AI Studio: Prompt design and tuning
                
                INTEGRATION:
                - REST APIs and client libraries
                - Integration with other Google Cloud services
                - Support for popular ML frameworks
                """,
                "url": "https://cloud.google.com/vertex-ai/docs/start/introduction-unified-platform",
                "section": "vertex_ai",
                "source": "google_cloud"
            },
            {
                "title": "Gemini Pro API Usage",
                "content": """
                Gemini Pro is Google's most capable AI model for complex reasoning tasks.
                
                CAPABILITIES:
                - Text generation and completion
                - Multi-turn conversations
                - Code generation and explanation
                - Complex reasoning and analysis
                - Multiple language support
                
                API USAGE:
                - REST API endpoints
                - Python SDK integration
                - Streaming responses
                - Token limits and pricing
                - Safety settings and content filtering
                
                BEST PRACTICES:
                - Prompt engineering techniques
                - Context management
                - Error handling
                - Rate limiting considerations
                """,
                "url": "https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini",
                "section": "gemini_api",
                "source": "google_cloud"
            },
            {
                "title": "Cloud Run Deployment",
                "content": """
                Google Cloud Run is a fully managed serverless platform for deploying containerized applications.
                
                KEY FEATURES:
                - Automatic scaling to zero
                - Pay-per-use pricing
                - Support for any language or framework
                - HTTPS endpoints
                - Custom domains
                
                DEPLOYMENT OPTIONS:
                - Deploy from source code
                - Deploy from container images
                - Continuous deployment from Git
                - Blue/green deployments
                
                CONFIGURATION:
                - CPU and memory allocation
                - Environment variables
                - Concurrency settings
                - Timeout configuration
                - Health checks
                """,
                "url": "https://cloud.google.com/run/docs",
                "section": "cloud_run",
                "source": "google_cloud"
            }
        ]
        
        documents.extend(gcp_docs)
        return documents
    
    def scrape_elastic_docs(self) -> List[Dict[str, Any]]:
        """Scrape relevant Elastic documentation"""
        documents = []
        
        # Key Elastic documentation sections
        elastic_docs = [
            {
                "title": "Elastic Hybrid Search",
                "content": """
                Elastic hybrid search combines traditional keyword search with vector search for optimal relevance.
                
                COMPONENTS:
                - BM25 keyword search for exact matches
                - Vector search for semantic similarity
                - Combined scoring algorithms
                - Relevance tuning capabilities
                
                IMPLEMENTATION:
                - Dense vector fields for embeddings
                - Multi-match queries for keywords
                - Script score queries for vector similarity
                - Boolean queries for combination
                
                BEST PRACTICES:
                - Proper field mapping configuration
                - Embedding model selection
                - Score normalization techniques
                - Performance optimization
                """,
                "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html",
                "section": "hybrid_search",
                "source": "elastic"
            },
            {
                "title": "Elasticsearch Vector Search",
                "content": """
                Elasticsearch provides native vector search capabilities for semantic search applications.
                
                VECTOR FIELD TYPES:
                - dense_vector for embeddings
                - Configurable dimensions
                - Similarity functions (cosine, dot_product, l2_norm)
                
                SEARCH METHODS:
                - kNN search for approximate nearest neighbors
                - Script score queries for custom scoring
                - Hybrid queries combining vector and text search
                
                PERFORMANCE:
                - HNSW algorithm for fast approximate search
                - Index-time and query-time optimizations
                - Memory and storage considerations
                """,
                "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/dense-vector.html",
                "section": "vector_search",
                "source": "elastic"
            },
            {
                "title": "Elastic Cloud Integration",
                "content": """
                Elastic Cloud provides hosted Elasticsearch with Google Cloud integration.
                
                FEATURES:
                - Managed Elasticsearch clusters
                - Automatic scaling and updates
                - Security and monitoring
                - Multi-cloud deployment options
                
                GOOGLE CLOUD INTEGRATION:
                - Deploy on Google Cloud Platform
                - VPC peering capabilities
                - IAM integration
                - Stackdriver logging
                
                API ACCESS:
                - REST API endpoints
                - Client libraries
                - Authentication methods
                - Rate limiting and quotas
                """,
                "url": "https://www.elastic.co/guide/en/cloud/current/ec-getting-started-gcp.html",
                "section": "cloud_integration",
                "source": "elastic"
            }
        ]
        
        documents.extend(elastic_docs)
        return documents

class DocumentationIngestion:
    def __init__(self):
        self.elastic_service = ElasticService()
        self.vertex_service = VertexService()
        self.scraper = DocumentationScraper()
    
    async def create_documentation_index(self):
        """Create Elasticsearch index for documentation"""
        mapping = {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "content": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "section": {
                    "type": "keyword"
                },
                "source": {
                    "type": "keyword"
                },
                "url": {
                    "type": "keyword"
                },
                "tags": {
                    "type": "keyword"
                },
                "embedding": {
                    "type": "dense_vector",
                    "dims": 768
                },
                "indexed_at": {
                    "type": "date"
                }
            }
        }
        
        success = await self.elastic_service.create_index(settings.DOCUMENTATION_INDEX, mapping)
        if success:
            logger.info(f"Created index: {settings.DOCUMENTATION_INDEX}")
        else:
            logger.warning(f"Index {settings.DOCUMENTATION_INDEX} might already exist")
    
    async def process_and_index_documents(self, documents: List[Dict[str, Any]]):
        """Process documents and index them with embeddings"""
        logger.info(f"Processing {len(documents)} documents...")
        
        for doc in documents:
            try:
                # Generate embedding for the document
                text_for_embedding = f"{doc['title']} {doc['content']}"
                embedding = await self.vertex_service.generate_single_embedding(text_for_embedding)
                
                if embedding:
                    doc['embedding'] = embedding
                
                # Add metadata
                doc['indexed_at'] = datetime.now().isoformat()
                doc_id = f"{doc['source']}_{doc['section']}_{doc['title'].lower().replace(' ', '_')}"
                
                # Index the document
                success = await self.elastic_service.index_document(
                    index=settings.DOCUMENTATION_INDEX,
                    doc_id=doc_id,
                    document=doc
                )
                
                if success:
                    logger.info(f"Indexed document: {doc['title']}")
                else:
                    logger.error(f"Failed to index document: {doc['title']}")
                
                # Rate limiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing document {doc.get('title', 'Unknown')}: {str(e)}")
    
    async def run_ingestion(self):
        """Run the complete documentation ingestion process"""
        logger.info("Starting documentation ingestion...")
        
        # Create index
        await self.create_documentation_index()
        
        all_documents = []
        
        # Scrape hackathon rules
        logger.info("Processing hackathon rules...")
        hackathon_docs = self.scraper.scrape_hackathon_rules()
        all_documents.extend(hackathon_docs)
        
        # Scrape Google Cloud docs
        logger.info("Processing Google Cloud documentation...")
        gcp_docs = self.scraper.scrape_google_cloud_docs()
        all_documents.extend(gcp_docs)
        
        # Scrape Elastic docs
        logger.info("Processing Elastic documentation...")
        elastic_docs = self.scraper.scrape_elastic_docs()
        all_documents.extend(elastic_docs)
        
        # Process and index all documents
        if all_documents:
            await self.process_and_index_documents(all_documents)
            logger.info(f"✅ Documentation ingestion completed! Indexed {len(all_documents)} documents.")
        else:
            logger.warning("No documents found to index.")

async def main():
    """Main function to run the documentation ingestion"""
    try:
        ingestion = DocumentationIngestion()
        await ingestion.run_ingestion()
    except Exception as e:
        logger.error(f"Documentation ingestion failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
