"""
Health check endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import logging

from app.services.elastic_service import ElasticService
# Smart service: tries real Vertex AI first, falls back gracefully if unavailable
from app.services.smart_vertex_service import VertexService
from app.services.github_service import GitHubService

logger = logging.getLogger(__name__)

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    services: Dict[str, str]
    details: Dict[str, Any]

@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check for all services
    """
    try:
        services_status = {}
        details = {}
        
        # Check Elasticsearch
        try:
            elastic_service = ElasticService()
            elastic_health = await elastic_service.health_check()
            services_status["elasticsearch"] = "healthy" if elastic_health else "unhealthy"
            details["elasticsearch"] = {"cluster_status": "green" if elastic_health else "red"}
        except Exception as e:
            services_status["elasticsearch"] = "error"
            details["elasticsearch"] = {"error": str(e)}
        
        # Check Vertex AI
        try:
            vertex_service = VertexService()
            vertex_health = await vertex_service.health_check()
            services_status["vertex_ai"] = "healthy" if vertex_health else "unhealthy"
            details["vertex_ai"] = {"model_available": vertex_health}
        except Exception as e:
            services_status["vertex_ai"] = "error"
            details["vertex_ai"] = {"error": str(e)}
        
        # Check GitHub
        try:
            github_service = GitHubService()
            github_health = await github_service.health_check()
            services_status["github"] = "healthy" if github_health else "unhealthy"
            details["github"] = {"api_accessible": github_health}
        except Exception as e:
            services_status["github"] = "error"
            details["github"] = {"error": str(e)}
        
        # Determine overall status
        overall_status = "healthy"
        if any(status in ["error", "unhealthy"] for status in services_status.values()):
            overall_status = "degraded"
        
        return HealthResponse(
            status=overall_status,
            services=services_status,
            details=details
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

@router.get("/elastic")
async def elastic_health():
    """Check Elasticsearch health specifically"""
    try:
        elastic_service = ElasticService()
        health = await elastic_service.health_check()
        cluster_info = await elastic_service.get_cluster_info()
        
        return {
            "status": "healthy" if health else "unhealthy",
            "cluster_info": cluster_info
        }
    except Exception as e:
        logger.error(f"Elastic health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Elastic health check failed: {str(e)}")

@router.get("/vertex")
async def vertex_health():
    """Check Vertex AI health specifically"""
    try:
        vertex_service = VertexService()
        health = await vertex_service.health_check()
        
        return {
            "status": "healthy" if health else "unhealthy",
            "model": vertex_service.model_name,
            "location": vertex_service.location
        }
    except Exception as e:
        logger.error(f"Vertex health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Vertex health check failed: {str(e)}")
