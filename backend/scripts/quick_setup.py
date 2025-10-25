"""
Quick setup script to populate Elasticsearch with sample data
This is for rapid hackathon development - gets you running in minutes!
"""

import asyncio
import logging
from typing import List, Dict, Any
import json
from datetime import datetime

from app.services.elastic_service import ElasticService
from app.services.vertex_service import VertexService
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuickSetup:
    def __init__(self):
        self.elastic_service = ElasticService()
        self.vertex_service = VertexService()

    async def setup_indices(self):
        """Create all required Elasticsearch indices"""
        logger.info("🔧 Creating Elasticsearch indices...")
        
        # Devpost projects index
        devpost_mapping = {
            "properties": {
                "title": {"type": "text", "analyzer": "standard"},
                "description": {"type": "text", "analyzer": "standard"},
                "technologies": {"type": "keyword"},
                "category": {"type": "keyword"},
                "year": {"type": "integer"},
                "url": {"type": "keyword"},
                "team_members": {"type": "keyword"},
                "embedding": {"type": "dense_vector", "dims": 768}
            }
        }
        
        # Documentation index
        docs_mapping = {
            "properties": {
                "title": {"type": "text", "analyzer": "standard"},
                "content": {"type": "text", "analyzer": "standard"},
                "section": {"type": "keyword"},
                "source": {"type": "keyword"},
                "url": {"type": "keyword"},
                "tags": {"type": "keyword"},
                "embedding": {"type": "dense_vector", "dims": 768}
            }
        }
        
        # GitHub activity index
        github_mapping = {
            "properties": {
                "type": {"type": "keyword"},
                "repository": {"type": "keyword"},
                "message": {"type": "text", "analyzer": "standard"},
                "author": {"type": "keyword"},
                "timestamp": {"type": "date"},
                "files": {"type": "keyword"},
                "event_type": {"type": "keyword"}
            }
        }
        
        # Create indices
        await self._create_index(settings.DEVPOST_INDEX, devpost_mapping)
        await self._create_index(settings.DOCUMENTATION_INDEX, docs_mapping)
        await self._create_index(settings.GITHUB_INDEX, github_mapping)
        
        logger.info("✅ All indices created successfully!")

    async def _create_index(self, index_name: str, mapping: Dict[str, Any]):
        """Create a single index with mapping"""
        try:
            # Delete index if exists
            try:
                await self.elastic_service.client.indices.delete(index=index_name)
                logger.info(f"Deleted existing index: {index_name}")
            except:
                pass
            
            # Create new index
            await self.elastic_service.client.indices.create(
                index=index_name,
                body={"mappings": mapping}
            )
            logger.info(f"Created index: {index_name}")
            
        except Exception as e:
            logger.error(f"Failed to create index {index_name}: {str(e)}")

    async def populate_sample_data(self):
        """Populate indices with sample data for demo"""
        logger.info("📊 Populating sample data...")
        
        # Sample Devpost projects
        sample_projects = [
            {
                "id": "project_1",
                "title": "AI-Powered Code Review Assistant",
                "description": "An intelligent code review tool that uses machine learning to identify bugs, security vulnerabilities, and performance issues in pull requests automatically.",
                "technologies": ["Python", "TensorFlow", "GitHub API", "Docker"],
                "category": "Developer Tools",
                "year": 2024,
                "url": "https://devpost.com/software/ai-code-review",
                "team_members": ["Alice Johnson", "Bob Smith"]
            },
            {
                "id": "project_2", 
                "title": "Smart Campus Navigation",
                "description": "A mobile app that provides real-time indoor navigation for university campuses using AR and machine learning to optimize routes based on crowd density.",
                "technologies": ["React Native", "ARCore", "Firebase", "Google Maps API"],
                "category": "Education",
                "year": 2024,
                "url": "https://devpost.com/software/smart-campus",
                "team_members": ["Carol Davis", "David Wilson"]
            },
            {
                "id": "project_3",
                "title": "Sustainable Supply Chain Tracker",
                "description": "Blockchain-based platform for tracking product sustainability metrics across supply chains, helping consumers make environmentally conscious decisions.",
                "technologies": ["Ethereum", "Solidity", "React", "Node.js"],
                "category": "Sustainability",
                "year": 2024,
                "url": "https://devpost.com/software/supply-chain-tracker",
                "team_members": ["Eve Brown", "Frank Miller"]
            }
        ]
        
        # Sample documentation
        sample_docs = [
            {
                "id": "doc_1",
                "title": "Google Cloud Vertex AI Setup Guide",
                "content": "Vertex AI is Google Cloud's unified ML platform. To get started: 1. Enable the Vertex AI API in your project 2. Create a service account with proper permissions 3. Install the Google Cloud SDK 4. Set up authentication using service account keys",
                "section": "Getting Started",
                "source": "Google Cloud Documentation",
                "url": "https://cloud.google.com/vertex-ai/docs",
                "tags": ["vertex-ai", "setup", "authentication"]
            },
            {
                "id": "doc_2",
                "title": "Elastic Hybrid Search Implementation",
                "content": "Hybrid search combines traditional keyword search with vector similarity search. Configure your index with both text fields and dense_vector fields. Use the multi_search API to combine BM25 and cosine similarity scores for optimal relevance.",
                "section": "Search Configuration",
                "source": "Elastic Documentation", 
                "url": "https://www.elastic.co/guide/en/elasticsearch/reference/current/search-your-data.html",
                "tags": ["elasticsearch", "hybrid-search", "vectors"]
            },
            {
                "id": "doc_3",
                "title": "Hackathon Submission Requirements",
                "content": "Your submission must include: 1. A working hosted application 2. Public GitHub repository with open source license 3. 3-minute demo video 4. Complete Devpost submission form 5. Integration with both Google Cloud and partner technologies",
                "section": "Submission Guidelines",
                "source": "Hackathon Rules",
                "url": "https://hackathon.devpost.com/rules",
                "tags": ["hackathon", "submission", "requirements"]
            }
        ]
        
        # Generate embeddings and index data
        await self._index_projects_with_embeddings(sample_projects)
        await self._index_docs_with_embeddings(sample_docs)
        
        logger.info("✅ Sample data populated successfully!")

    async def _index_projects_with_embeddings(self, projects: List[Dict[str, Any]]):
        """Index projects with embeddings"""
        for project in projects:
            try:
                # Generate embedding for title + description
                text_for_embedding = f"{project['title']} {project['description']}"
                embedding = await self.vertex_service.generate_single_embedding(text_for_embedding)
                
                if embedding:
                    project['embedding'] = embedding
                
                # Index document
                await self.elastic_service.index_document(
                    index=settings.DEVPOST_INDEX,
                    doc_id=project['id'],
                    document=project
                )
                logger.info(f"Indexed project: {project['title']}")
                
            except Exception as e:
                logger.error(f"Failed to index project {project['title']}: {str(e)}")

    async def _index_docs_with_embeddings(self, docs: List[Dict[str, Any]]):
        """Index documentation with embeddings"""
        for doc in docs:
            try:
                # Generate embedding for title + content
                text_for_embedding = f"{doc['title']} {doc['content']}"
                embedding = await self.vertex_service.generate_single_embedding(text_for_embedding)
                
                if embedding:
                    doc['embedding'] = embedding
                
                # Index document
                await self.elastic_service.index_document(
                    index=settings.DOCUMENTATION_INDEX,
                    doc_id=doc['id'],
                    document=doc
                )
                logger.info(f"Indexed doc: {doc['title']}")
                
            except Exception as e:
                logger.error(f"Failed to index doc {doc['title']}: {str(e)}")

    async def test_search(self):
        """Test the search functionality"""
        logger.info("🔍 Testing search functionality...")
        
        try:
            # Test project search
            projects = await self.elastic_service.search_devpost_projects(
                query="AI code review",
                size=2
            )
            logger.info(f"Found {len(projects)} projects for 'AI code review'")
            
            # Test documentation search
            docs = await self.elastic_service.search_documentation(
                query="Vertex AI setup",
                size=2
            )
            logger.info(f"Found {len(docs)} docs for 'Vertex AI setup'")
            
            logger.info("✅ Search functionality working!")
            
        except Exception as e:
            logger.error(f"Search test failed: {str(e)}")

async def main():
    """Run the quick setup"""
    try:
        setup = QuickSetup()
        
        logger.info("🚀 Starting quick setup for Hackathon Agent...")
        
        # Setup indices
        await setup.setup_indices()
        
        # Populate sample data
        await setup.populate_sample_data()
        
        # Test functionality
        await setup.test_search()
        
        logger.info("🎉 Quick setup completed! Your Hackathon Agent is ready!")
        logger.info("💡 Next steps:")
        logger.info("   1. Run the backend: uvicorn main:app --reload")
        logger.info("   2. Run the frontend: npm run dev")
        logger.info("   3. Test the chat interface at http://localhost:3000")
        
    except Exception as e:
        logger.error(f"Quick setup failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
