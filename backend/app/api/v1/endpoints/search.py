"""
Search endpoints for hybrid search capabilities
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from app.services.elastic_service import ElasticService
# Smart service: tries real Vertex AI first, falls back gracefully if unavailable
from app.services.smart_vertex_service import VertexService

logger = logging.getLogger(__name__)

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    search_type: str = "hybrid"  # "hybrid", "semantic", "keyword"
    index: Optional[str] = None
    size: int = 10

class SearchResult(BaseModel):
    title: str
    description: str
    url: Optional[str] = None
    score: float
    source: str
    metadata: Optional[Dict[str, Any]] = {}

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    query: str
    search_type: str
    took_ms: Optional[int] = None

@router.post("/", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Perform hybrid search across all indices
    """
    try:
        elastic_service = ElasticService()
        vertex_service = VertexService()
        
        # Generate embedding for semantic search
        query_embedding = None
        if request.search_type in ["hybrid", "semantic"]:
            query_embedding = await vertex_service.generate_single_embedding(request.query)
        
        # Determine which indices to search
        indices_to_search = []
        if request.index:
            indices_to_search = [request.index]
        else:
            # Search all available indices
            indices_to_search = ["devpost_projects", "hackathon_docs"]
        
        all_results = []
        
        # Search each index
        for index in indices_to_search:
            try:
                if index == "devpost_projects":
                    projects = await elastic_service.search_devpost_projects(
                        query=request.query,
                        vector_query=query_embedding if request.search_type != "keyword" else None,
                        size=request.size
                    )
                    
                    for project in projects:
                        all_results.append(SearchResult(
                            title=project["title"],
                            description=project["description"],
                            url=project["url"],
                            score=project["score"],
                            source="devpost",
                            metadata={
                                "technologies": project.get("technologies", []),
                                "category": project.get("category", ""),
                                "year": project.get("year", "")
                            }
                        ))
                
                elif index == "hackathon_docs":
                    docs = await elastic_service.search_documentation(
                        query=request.query,
                        vector_query=query_embedding if request.search_type != "keyword" else None,
                        size=request.size
                    )
                    
                    for doc in docs:
                        all_results.append(SearchResult(
                            title=doc["title"],
                            description=doc["content"][:300] + "...",
                            url=doc.get("url", ""),
                            score=doc["score"],
                            source="documentation",
                            metadata={
                                "section": doc.get("section", ""),
                                "doc_source": doc.get("source", "")
                            }
                        ))
                        
            except Exception as e:
                logger.warning(f"Search failed for index {index}: {str(e)}")
                continue
        
        # Sort results by score
        all_results.sort(key=lambda x: x.score, reverse=True)
        
        # Limit results
        limited_results = all_results[:request.size]
        
        return SearchResponse(
            results=limited_results,
            total=len(all_results),
            query=request.query,
            search_type=request.search_type
        )
        
    except Exception as e:
        logger.error(f"Search endpoint failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Search request failed")

@router.get("/devpost", response_model=SearchResponse)
async def search_devpost(
    q: str = Query(..., description="Search query"),
    size: int = Query(10, description="Number of results"),
    search_type: str = Query("hybrid", description="Search type: hybrid, semantic, keyword")
):
    """
    Search Devpost projects specifically
    """
    try:
        elastic_service = ElasticService()
        vertex_service = VertexService()
        
        # Generate embedding for semantic search
        query_embedding = None
        if search_type in ["hybrid", "semantic"]:
            query_embedding = await vertex_service.generate_single_embedding(q)
        
        # Search Devpost projects
        projects = await elastic_service.search_devpost_projects(
            query=q,
            vector_query=query_embedding if search_type != "keyword" else None,
            size=size
        )
        
        results = []
        for project in projects:
            results.append(SearchResult(
                title=project["title"],
                description=project["description"],
                url=project["url"],
                score=project["score"],
                source="devpost",
                metadata={
                    "technologies": project.get("technologies", []),
                    "category": project.get("category", ""),
                    "year": project.get("year", "")
                }
            ))
        
        return SearchResponse(
            results=results,
            total=len(results),
            query=q,
            search_type=search_type
        )
        
    except Exception as e:
        logger.error(f"Devpost search failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Devpost search failed")

@router.get("/documentation", response_model=SearchResponse)
async def search_documentation(
    q: str = Query(..., description="Search query"),
    size: int = Query(5, description="Number of results"),
    search_type: str = Query("hybrid", description="Search type: hybrid, semantic, keyword")
):
    """
    Search hackathon documentation specifically
    """
    try:
        elastic_service = ElasticService()
        vertex_service = VertexService()
        
        # Generate embedding for semantic search
        query_embedding = None
        if search_type in ["hybrid", "semantic"]:
            query_embedding = await vertex_service.generate_single_embedding(q)
        
        # Search documentation
        docs = await elastic_service.search_documentation(
            query=q,
            vector_query=query_embedding if search_type != "keyword" else None,
            size=size
        )
        
        results = []
        for doc in docs:
            results.append(SearchResult(
                title=doc["title"],
                description=doc["content"][:300] + "...",
                url=doc.get("url", ""),
                score=doc["score"],
                source="documentation",
                metadata={
                    "section": doc.get("section", ""),
                    "doc_source": doc.get("source", "")
                }
            ))
        
        return SearchResponse(
            results=results,
            total=len(results),
            query=q,
            search_type=search_type
        )
        
    except Exception as e:
        logger.error(f"Documentation search failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Documentation search failed")

@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., description="Partial query for suggestions"),
    limit: int = Query(5, description="Number of suggestions")
):
    """
    Get search suggestions based on partial query
    """
    try:
        # For now, return static suggestions based on common patterns
        # In a full implementation, this could use Elasticsearch's completion suggester
        
        query_lower = q.lower()
        
        suggestions = []
        
        # Common hackathon-related suggestions
        common_suggestions = [
            "How to use Google Cloud Vertex AI",
            "Elastic hybrid search implementation",
            "Hackathon submission requirements",
            "Best practices for team collaboration",
            "GitHub integration for progress tracking",
            "AI-powered search applications",
            "Real-time data processing",
            "Machine learning model deployment",
            "API development with FastAPI",
            "Frontend development with React"
        ]
        
        # Filter suggestions based on query
        for suggestion in common_suggestions:
            if any(word in suggestion.lower() for word in query_lower.split()):
                suggestions.append(suggestion)
        
        # Add some generic suggestions if we don't have enough matches
        if len(suggestions) < limit:
            generic_suggestions = [
                f"How to implement {q}",
                f"Best practices for {q}",
                f"Examples of {q}",
                f"Troubleshooting {q}",
                f"Advanced {q} techniques"
            ]
            suggestions.extend(generic_suggestions)
        
        return {
            "suggestions": suggestions[:limit],
            "query": q
        }
        
    except Exception as e:
        logger.error(f"Search suggestions failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get search suggestions")
