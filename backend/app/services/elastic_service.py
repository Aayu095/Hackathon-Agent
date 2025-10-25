"""
Elasticsearch service for hybrid search capabilities
"""

import logging
from typing import List, Dict, Any, Optional
from elasticsearch import AsyncElasticsearch
from app.core.config import settings

logger = logging.getLogger(__name__)

class ElasticService:
    def __init__(self):
        # For Hosted Elastic Cloud deployments (using cloud_id)
        self.client = AsyncElasticsearch(
            cloud_id=settings.ELASTIC_CLOUD_ID,
            api_key=settings.ELASTIC_API_KEY,
            request_timeout=30,
            max_retries=3,
            retry_on_timeout=True
        )
    
    async def health_check(self) -> bool:
        """Check Elasticsearch cluster health"""
        try:
            health = await self.client.cluster.health()
            return health['status'] in ['green', 'yellow']
        except Exception as e:
            logger.error(f"Elasticsearch health check failed: {str(e)}")
            return False
    
    async def get_cluster_info(self) -> Dict[str, Any]:
        """Get cluster information"""
        try:
            info = await self.client.info()
            return {
                "cluster_name": info.get("cluster_name"),
                "version": info.get("version", {}).get("number"),
                "lucene_version": info.get("version", {}).get("lucene_version")
            }
        except Exception as e:
            logger.error(f"Failed to get cluster info: {str(e)}")
            return {}
    
    async def hybrid_search(
        self, 
        query: str, 
        index: str,
        vector_field: str = "embedding",
        text_fields: List[str] = None,
        size: int = 10,
        vector_query: List[float] = None
    ) -> Dict[str, Any]:
        """
        Perform hybrid search for Hosted Elasticsearch deployments
        Combines BM25 keyword search with kNN vector search
        """
        try:
            if text_fields is None:
                text_fields = ["title", "description", "content"]
            
            # Build query combining BM25 and kNN
            if query and vector_query:
                # Hybrid: Both keyword and vector search
                search_body = {
                    "size": size,
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "multi_match": {
                                        "query": query,
                                        "fields": text_fields,
                                        "type": "best_fields",
                                        "boost": 1.0
                                    }
                                }
                            ]
                        }
                    },
                    "knn": {
                        "field": vector_field,
                        "query_vector": vector_query,
                        "k": size,
                        "num_candidates": size * 10,
                        "boost": 1.0
                    },
                    "_source": {
                        "excludes": [vector_field]
                    }
                }
            elif vector_query:
                # Vector search only
                search_body = {
                    "size": size,
                    "knn": {
                        "field": vector_field,
                        "query_vector": vector_query,
                        "k": size,
                        "num_candidates": size * 10
                    },
                    "_source": {
                        "excludes": [vector_field]
                    }
                }
            elif query:
                # Keyword search only
                search_body = {
                    "size": size,
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": text_fields,
                            "type": "best_fields"
                        }
                    },
                    "_source": {
                        "excludes": [vector_field]
                    }
                }
            else:
                # Match all
                search_body = {
                    "size": size,
                    "query": {"match_all": {}},
                    "_source": {"excludes": [vector_field]}
                }
            
            # Execute search
            response = await self.client.search(
                index=index,
                body=search_body
            )
            
            return {
                "hits": response["hits"]["hits"],
                "total": response["hits"]["total"]["value"] if "total" in response["hits"] else len(response["hits"]["hits"]),
                "max_score": response["hits"]["max_score"]
            }
            
        except Exception as e:
            logger.error(f"Hybrid search failed: {str(e)}")
            # Fallback to simple text search
            try:
                fallback_body = {
                    "size": size,
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": text_fields,
                            "type": "best_fields"
                        }
                    },
                    "_source": {"excludes": [vector_field]}
                }
                
                response = await self.client.search(
                    index=index,
                    body=fallback_body
                )
                
                return {
                    "hits": response["hits"]["hits"],
                    "total": response["hits"]["total"]["value"],
                    "max_score": response["hits"]["max_score"]
                }
            except Exception as fallback_error:
                logger.error(f"Fallback search also failed: {str(fallback_error)}")
                return {"hits": [], "total": 0, "max_score": 0}
    
    async def index_document(
        self, 
        index: str, 
        doc_id: str, 
        document: Dict[str, Any]
    ) -> bool:
        """Index a single document"""
        try:
            await self.client.index(
                index=index,
                id=doc_id,
                body=document
            )
            return True
        except Exception as e:
            logger.error(f"Failed to index document: {str(e)}")
            return False
    
    async def bulk_index(
        self, 
        index: str, 
        documents: List[Dict[str, Any]]
    ) -> bool:
        """Bulk index multiple documents"""
        try:
            actions = []
            for doc in documents:
                action = {
                    "_index": index,
                    "_id": doc.get("id"),
                    "_source": doc
                }
                actions.append(action)
            
            from elasticsearch.helpers import async_bulk
            await async_bulk(self.client, actions)
            return True
            
        except Exception as e:
            logger.error(f"Bulk indexing failed: {str(e)}")
            return False
    
    async def create_index(self, index: str, mapping: Dict[str, Any]) -> bool:
        """Create an index with mapping"""
        try:
            await self.client.indices.create(
                index=index,
                body={"mappings": mapping}
            )
            return True
        except Exception as e:
            logger.error(f"Failed to create index: {str(e)}")
            return False
    
    async def search_devpost_projects(
        self, 
        query: str, 
        vector_query: List[float] = None,
        size: int = 5
    ) -> List[Dict[str, Any]]:
        """Search Devpost projects using hybrid search"""
        try:
            results = await self.hybrid_search(
                query=query,
                index=settings.DEVPOST_INDEX,
                text_fields=["title", "description", "technologies", "category"],
                vector_query=vector_query,
                size=size
            )
            
            projects = []
            for hit in results["hits"]:
                source = hit["_source"]
                projects.append({
                    "title": source.get("title", ""),
                    "description": source.get("description", ""),
                    "url": source.get("url", ""),
                    "technologies": source.get("technologies", []),
                    "category": source.get("category", ""),
                    "year": source.get("year", ""),
                    "score": hit["_score"]
                })
            
            return projects
            
        except Exception as e:
            logger.error(f"Devpost search failed: {str(e)}")
            return []
    
    async def search_documentation(
        self, 
        query: str, 
        vector_query: List[float] = None,
        size: int = 3
    ) -> List[Dict[str, Any]]:
        """Search hackathon documentation using hybrid search"""
        try:
            results = await self.hybrid_search(
                query=query,
                index=settings.DOCUMENTATION_INDEX,
                text_fields=["title", "content", "section", "tags"],
                vector_query=vector_query,
                size=size
            )
            
            docs = []
            for hit in results["hits"]:
                source = hit["_source"]
                docs.append({
                    "title": source.get("title", ""),
                    "content": source.get("content", ""),
                    "url": source.get("url", ""),
                    "section": source.get("section", ""),
                    "source": source.get("source", ""),
                    "score": hit["_score"]
                })
            
            return docs
            
        except Exception as e:
            logger.error(f"Documentation search failed: {str(e)}")
            return []
    
    async def close(self):
        """Close the Elasticsearch connection"""
        await self.client.close()
