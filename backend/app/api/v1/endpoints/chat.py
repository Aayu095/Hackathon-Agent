"""
Chat endpoints for conversational AI
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import asyncio

# Smart service: tries real Vertex AI first, falls back gracefully if unavailable
from app.services.smart_vertex_service import VertexService
from app.services.elastic_service import ElasticService
from app.services.github_service import GitHubService

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []
    repo_url: Optional[str] = None
    context_type: Optional[str] = None  # "idea_validation", "documentation", "progress"

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[Dict[str, Any]]] = []
    suggestions: Optional[List[str]] = []
    conversation_id: Optional[str] = None

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - handles all conversational interactions
    """
    try:
        vertex_service = VertexService()
        elastic_service = ElasticService()
        github_service = GitHubService()
        
        # Generate embedding for the user's message
        user_embedding = await vertex_service.generate_single_embedding(request.message)
        
        # Determine the type of query and gather relevant context
        context_data = await _gather_context(
            request.message,
            user_embedding,
            request.context_type,
            request.repo_url,
            elastic_service,
            github_service
        )
        
        # Convert conversation history to the format expected by VertexService
        history = []
        if request.conversation_history:
            for msg in request.conversation_history:
                history.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Generate AI response
        response = await vertex_service.generate_response(
            prompt=request.message,
            context=context_data.get("formatted_context"),
            conversation_history=history
        )
        
        # Generate suggestions for follow-up questions
        suggestions = _generate_suggestions(request.message, context_data.get("context_type"))
        
        return ChatResponse(
            response=response,
            sources=context_data.get("sources", []),
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat request")

@router.post("/validate-idea", response_model=ChatResponse)
async def validate_idea(request: ChatRequest):
    """
    Specialized endpoint for idea validation
    """
    try:
        vertex_service = VertexService()
        elastic_service = ElasticService()
        
        # Generate embedding for the idea
        idea_embedding = await vertex_service.generate_single_embedding(request.message)
        
        # Search for similar projects
        similar_projects = await elastic_service.search_devpost_projects(
            query=request.message,
            vector_query=idea_embedding,
            size=5
        )
        
        # Generate validation response
        response = await vertex_service.generate_idea_validation_response(
            idea_description=request.message,
            similar_projects=similar_projects
        )
        
        # Format sources
        sources = []
        for project in similar_projects:
            sources.append({
                "type": "devpost_project",
                "title": project["title"],
                "description": project["description"][:200] + "...",
                "url": project["url"],
                "relevance_score": project["score"]
            })
        
        suggestions = [
            "How can I differentiate my idea from these similar projects?",
            "What technical challenges should I expect?",
            "What technologies would work best for this idea?",
            "How can I validate this idea with potential users?"
        ]
        
        return ChatResponse(
            response=response,
            sources=sources,
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"Idea validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to validate idea")

@router.post("/progress-report", response_model=ChatResponse)
async def progress_report(request: ChatRequest):
    """
    Generate progress report from GitHub activity
    """
    try:
        if not request.repo_url:
            raise HTTPException(status_code=400, detail="Repository URL is required")
        
        vertex_service = VertexService()
        github_service = GitHubService()
        
        # Get GitHub activity analysis
        progress_analysis = await github_service.analyze_project_progress(request.repo_url)
        
        if "error" in progress_analysis:
            raise HTTPException(status_code=400, detail=progress_analysis["error"])
        
        # Generate progress summary
        response = await vertex_service.generate_progress_summary(
            github_activity=progress_analysis.get("recent_activity", [])
        )
        
        # Format sources
        sources = [{
            "type": "github_analysis",
            "repository": progress_analysis.get("repository", "Unknown"),
            "analysis_period": progress_analysis.get("analysis_period", "Unknown"),
            "commit_count": progress_analysis.get("commit_analysis", {}).get("total_commits", 0),
            "progress_metrics": progress_analysis.get("progress_metrics", {})
        }]
        
        suggestions = [
            "What should we focus on next?",
            "Are we on track for the deadline?",
            "What potential blockers should we address?",
            "How can we improve our development velocity?"
        ]
        
        return ChatResponse(
            response=response,
            sources=sources,
            suggestions=suggestions
        )
        
    except Exception as e:
        logger.error(f"Progress report failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate progress report")

async def _gather_context(
    message: str,
    message_embedding: List[float],
    context_type: Optional[str],
    repo_url: Optional[str],
    elastic_service: ElasticService,
    github_service: GitHubService
) -> Dict[str, Any]:
    """
    Gather relevant context based on the message and context type
    """
    context_data = {
        "formatted_context": "",
        "sources": [],
        "context_type": context_type or _detect_context_type(message)
    }
    
    try:
        # Always search documentation for general questions using hybrid search
        docs = await elastic_service.search_documentation(
            query=message,
            vector_query=message_embedding,
            size=3
        )
        
        if docs:
            doc_context = "📚 **Relevant Documentation:**\n"
            for i, doc in enumerate(docs, 1):
                doc_context += f"{i}. **{doc['title']}** (Source: {doc.get('source', 'Unknown')})\n"
                doc_context += f"   {doc['content'][:400]}...\n"
                doc_context += f"   🔗 {doc.get('url', 'No URL')}\n\n"
                
                context_data["sources"].append({
                    "type": "documentation",
                    "title": doc["title"],
                    "content": doc["content"][:300] + "...",
                    "url": doc.get("url", ""),
                    "source": doc.get("source", ""),
                    "relevance_score": doc.get("score", 0)
                })
            context_data["formatted_context"] += doc_context
        
        # Search Devpost projects for idea-related queries
        if context_data["context_type"] in ["idea_validation", "inspiration"]:
            projects = await elastic_service.search_devpost_projects(
                query=message,
                vector_query=message_embedding,
                size=3
            )
            
            if projects:
                project_context = "\n🚀 **Similar Hackathon Projects:**\n"
                for i, project in enumerate(projects, 1):
                    project_context += f"{i}. **{project['title']}** ({project.get('year', 'Unknown Year')})\n"
                    project_context += f"   📝 {project['description'][:300]}...\n"
                    project_context += f"   🛠️ Tech: {', '.join(project.get('technologies', []))}\n"
                    project_context += f"   🔗 {project.get('url', 'No URL')}\n"
                    project_context += f"   📊 Relevance: {project.get('score', 0):.2f}\n\n"
                    
                    context_data["sources"].append({
                        "type": "devpost_project",
                        "title": project["title"],
                        "description": project["description"][:200] + "...",
                        "url": project.get("url", ""),
                        "technologies": project.get("technologies", []),
                        "year": project.get("year", "Unknown"),
                        "relevance_score": project.get("score", 0)
                    })
                context_data["formatted_context"] += project_context
        
        # Get GitHub context for progress-related queries
        if context_data["context_type"] == "progress" and repo_url:
            activity = await github_service.get_repository_activity(repo_url, days=3)
            if activity:
                github_context = "Recent GitHub Activity:\n"
                for item in activity[:5]:
                    github_context += f"- {item['type']}: {item['message'][:100]}...\n"
                context_data["formatted_context"] += github_context
        
        return context_data
        
    except Exception as e:
        logger.error(f"Failed to gather context: {str(e)}")
        return context_data

def _detect_context_type(message: str) -> str:
    """
    Detect the type of context needed based on the message content
    """
    message_lower = message.lower()
    
    # Idea validation keywords
    if any(keyword in message_lower for keyword in [
        "idea", "project", "validate", "original", "similar", "unique", "concept"
    ]):
        return "idea_validation"
    
    # Progress tracking keywords
    if any(keyword in message_lower for keyword in [
        "progress", "status", "commit", "github", "development", "team", "accomplished"
    ]):
        return "progress"
    
    # Documentation keywords
    if any(keyword in message_lower for keyword in [
        "how to", "documentation", "rules", "guidelines", "google cloud", "elastic", "vertex"
    ]):
        return "documentation"
    
    return "general"

def _generate_suggestions(message: str, context_type: str) -> List[str]:
    """
    Generate follow-up suggestions based on the message and context
    """
    base_suggestions = [
        "Can you help me validate my project idea?",
        "What's our current development progress?",
        "How do I use Google Cloud with Elastic?",
        "What are the hackathon submission requirements?"
    ]
    
    context_suggestions = {
        "idea_validation": [
            "How can I make my idea more unique?",
            "What technical challenges should I expect?",
            "What technologies would work best?",
            "How do I validate this with users?"
        ],
        "progress": [
            "What should we focus on next?",
            "Are we on track for the deadline?",
            "How can we improve our velocity?",
            "What blockers should we address?"
        ],
        "documentation": [
            "Show me examples of this implementation",
            "What are the best practices?",
            "Are there any limitations I should know?",
            "How do I troubleshoot common issues?"
        ]
    }
    
    return context_suggestions.get(context_type, base_suggestions)
