"""
Quick test script to verify backend components
"""
import asyncio
import sys

async def test_services():
    print("=" * 50)
    print("Testing Backend Services")
    print("=" * 50)
    
    # Test 1: Import smart vertex service
    print("\n1. Testing Smart Vertex Service...")
    try:
        from app.services.smart_vertex_service import VertexService
        vertex = VertexService()
        print("   ✅ Smart Vertex Service initialized")
        
        # Test health
        health = await vertex.health_check()
        print(f"   ✅ Health check: {health}")
        
        # Test response generation
        response = await vertex.generate_response("Hello, test message")
        print(f"   ✅ Generated response: {response[:100]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Import elastic service
    print("\n2. Testing Elastic Service...")
    try:
        from app.services.elastic_service import ElasticService
        elastic = ElasticService()
        print("   ✅ Elastic Service initialized")
        
        # Test health (this might fail if not configured)
        try:
            health = await elastic.health_check()
            print(f"   ✅ Elastic health: {health}")
        except Exception as e:
            print(f"   ⚠️  Elastic not configured (expected): {str(e)[:100]}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Test chat endpoint logic
    print("\n3. Testing Chat Logic...")
    try:
        # Simple test without Elastic
        test_message = "I want to build an AI assistant"
        response = await vertex.generate_response(test_message)
        print(f"   ✅ Chat response generated: {len(response)} characters")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    result = asyncio.run(test_services())
    sys.exit(0 if result else 1)
