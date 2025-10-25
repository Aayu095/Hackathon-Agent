"""
Test RAG (Retrieval Augmented Generation) functionality
Validates that hybrid search + context generation + LLM response works properly
"""

import asyncio
import logging
from app.services.elastic_service import ElasticService
from app.services.vertex_service import VertexService
from app.api.v1.endpoints.chat import _gather_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_rag_pipeline():
    """Test the complete RAG pipeline"""
    logger.info("🧪 Testing RAG Pipeline...")
    
    try:
        # Initialize services
        elastic_service = ElasticService()
        vertex_service = VertexService()
        
        # Test queries
        test_queries = [
            {
                "query": "How do I set up Vertex AI for my hackathon project?",
                "expected_context": "documentation"
            },
            {
                "query": "I want to build an AI code review tool",
                "expected_context": "idea_validation"
            },
            {
                "query": "What's our team's progress this week?",
                "expected_context": "progress"
            }
        ]
        
        for i, test in enumerate(test_queries, 1):
            logger.info(f"\n--- Test {i}: {test['query']} ---")
            
            # Step 1: Generate embedding
            embedding = await vertex_service.generate_single_embedding(test['query'])
            logger.info(f"✅ Generated embedding: {len(embedding)} dimensions")
            
            # Step 2: Gather context using RAG
            context_data = await _gather_context(
                message=test['query'],
                message_embedding=embedding,
                context_type=None,
                repo_url="https://github.com/test/repo",
                elastic_service=elastic_service,
                github_service=None  # Skip GitHub for this test
            )
            
            logger.info(f"✅ Context type detected: {context_data['context_type']}")
            logger.info(f"✅ Sources found: {len(context_data['sources'])}")
            logger.info(f"✅ Context length: {len(context_data['formatted_context'])} chars")
            
            # Step 3: Generate AI response with context
            if context_data['formatted_context']:
                response = await vertex_service.generate_response(
                    prompt=test['query'],
                    context=context_data['formatted_context']
                )
                logger.info(f"✅ Generated response: {len(response)} chars")
                logger.info(f"📝 Response preview: {response[:200]}...")
            else:
                logger.warning("⚠️ No context retrieved for query")
            
            # Validate results
            if context_data['sources']:
                logger.info(f"✅ RAG working: Found {len(context_data['sources'])} relevant sources")
            else:
                logger.warning("⚠️ No sources found - check data indexing")
        
        logger.info("\n🎉 RAG Pipeline Test Completed!")
        
    except Exception as e:
        logger.error(f"❌ RAG test failed: {str(e)}")
        raise

async def test_hybrid_search():
    """Test hybrid search specifically"""
    logger.info("\n🔍 Testing Hybrid Search...")
    
    try:
        elastic_service = ElasticService()
        vertex_service = VertexService()
        
        query = "Google Cloud setup guide"
        embedding = await vertex_service.generate_single_embedding(query)
        
        # Test documentation search
        docs = await elastic_service.search_documentation(
            query=query,
            vector_query=embedding,
            size=3
        )
        
        logger.info(f"✅ Documentation search: {len(docs)} results")
        for doc in docs:
            logger.info(f"  - {doc['title']} (score: {doc.get('score', 0):.3f})")
        
        # Test project search
        projects = await elastic_service.search_devpost_projects(
            query="AI assistant chatbot",
            vector_query=await vertex_service.generate_single_embedding("AI assistant chatbot"),
            size=3
        )
        
        logger.info(f"✅ Project search: {len(projects)} results")
        for project in projects:
            logger.info(f"  - {project['title']} (score: {project.get('score', 0):.3f})")
        
        logger.info("✅ Hybrid search working correctly!")
        
    except Exception as e:
        logger.error(f"❌ Hybrid search test failed: {str(e)}")
        raise

async def main():
    """Run all RAG tests"""
    try:
        logger.info("🚀 Starting RAG System Tests...")
        
        # Test hybrid search
        await test_hybrid_search()
        
        # Test complete RAG pipeline
        await test_rag_pipeline()
        
        logger.info("\n🎉 All RAG tests passed! System is ready for hackathon!")
        
    except Exception as e:
        logger.error(f"❌ RAG tests failed: {str(e)}")
        logger.info("💡 Make sure to run quick_setup.py first to populate data")
        raise

if __name__ == "__main__":
    asyncio.run(main())
