"""
GitHub integration endpoints
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import hmac
import hashlib

from app.services.github_service import GitHubService
from app.services.elastic_service import ElasticService
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

class RepositoryRequest(BaseModel):
    repo_url: str

class ProgressResponse(BaseModel):
    repository: str
    analysis_period: str
    commit_analysis: Dict[str, Any]
    file_analysis: Dict[str, Any]
    progress_metrics: Dict[str, Any]
    recent_activity: List[Dict[str, Any]]
    recommendations: List[str]

class WebhookPayload(BaseModel):
    action: Optional[str] = None
    repository: Optional[Dict[str, Any]] = None
    commits: Optional[List[Dict[str, Any]]] = None
    head_commit: Optional[Dict[str, Any]] = None

@router.post("/analyze", response_model=ProgressResponse)
async def analyze_repository(request: RepositoryRequest):
    """
    Analyze GitHub repository progress and activity
    """
    try:
        github_service = GitHubService()
        
        # Analyze project progress
        analysis = await github_service.analyze_project_progress(request.repo_url)
        
        if "error" in analysis:
            raise HTTPException(status_code=400, detail=analysis["error"])
        
        return ProgressResponse(**analysis)
        
    except Exception as e:
        logger.error(f"Repository analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze repository")

@router.get("/activity/{owner}/{repo}")
async def get_repository_activity(
    owner: str,
    repo: str,
    days: int = 7
):
    """
    Get recent activity for a specific repository
    """
    try:
        github_service = GitHubService()
        
        repo_url = f"https://github.com/{owner}/{repo}"
        activity = await github_service.get_repository_activity(repo_url, days)
        
        return {
            "repository": f"{owner}/{repo}",
            "period_days": days,
            "activity": activity,
            "total_activities": len(activity)
        }
        
    except Exception as e:
        logger.error(f"Failed to get repository activity: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get repository activity")

@router.get("/stats/{owner}/{repo}")
async def get_repository_stats(owner: str, repo: str):
    """
    Get repository statistics and metadata
    """
    try:
        github_service = GitHubService()
        
        repo_url = f"https://github.com/{owner}/{repo}"
        stats = await github_service.get_repository_stats(repo_url)
        
        if not stats:
            raise HTTPException(status_code=404, detail="Repository not found or inaccessible")
        
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get repository stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get repository stats")

@router.post("/webhook")
async def github_webhook(request: Request):
    """
    Handle GitHub webhook events for real-time updates
    """
    try:
        # Verify webhook signature
        signature = request.headers.get("X-Hub-Signature-256")
        if not signature or not settings.GITHUB_WEBHOOK_SECRET:
            raise HTTPException(status_code=401, detail="Unauthorized webhook request")
        
        body = await request.body()
        
        # Verify signature
        expected_signature = "sha256=" + hmac.new(
            settings.GITHUB_WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
        # Parse webhook payload
        import json
        payload = json.loads(body)
        
        # Process webhook event
        event_type = request.headers.get("X-GitHub-Event")
        await _process_webhook_event(event_type, payload)
        
        return {"status": "processed", "event": event_type}
        
    except Exception as e:
        logger.error(f"Webhook processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process webhook")

async def _process_webhook_event(event_type: str, payload: Dict[str, Any]):
    """
    Process different types of GitHub webhook events
    """
    try:
        elastic_service = ElasticService()
        
        repository = payload.get("repository", {})
        repo_name = repository.get("full_name", "unknown")
        
        # Create activity document for indexing
        activity_doc = {
            "repository": repo_name,
            "event_type": event_type,
            "timestamp": payload.get("created_at") or payload.get("updated_at"),
            "processed_at": "2024-01-01T00:00:00Z"  # Current timestamp
        }
        
        if event_type == "push":
            # Handle push events
            commits = payload.get("commits", [])
            head_commit = payload.get("head_commit", {})
            
            activity_doc.update({
                "action": "push",
                "commit_count": len(commits),
                "head_commit": {
                    "id": head_commit.get("id", ""),
                    "message": head_commit.get("message", ""),
                    "author": head_commit.get("author", {}).get("name", ""),
                    "modified_files": head_commit.get("modified", []),
                    "added_files": head_commit.get("added", []),
                    "removed_files": head_commit.get("removed", [])
                }
            })
            
        elif event_type == "issues":
            # Handle issue events
            issue = payload.get("issue", {})
            action = payload.get("action", "")
            
            activity_doc.update({
                "action": f"issue_{action}",
                "issue": {
                    "number": issue.get("number", 0),
                    "title": issue.get("title", ""),
                    "state": issue.get("state", ""),
                    "author": issue.get("user", {}).get("login", ""),
                    "labels": [label.get("name", "") for label in issue.get("labels", [])]
                }
            })
            
        elif event_type == "pull_request":
            # Handle pull request events
            pr = payload.get("pull_request", {})
            action = payload.get("action", "")
            
            activity_doc.update({
                "action": f"pr_{action}",
                "pull_request": {
                    "number": pr.get("number", 0),
                    "title": pr.get("title", ""),
                    "state": pr.get("state", ""),
                    "author": pr.get("user", {}).get("login", ""),
                    "base_branch": pr.get("base", {}).get("ref", ""),
                    "head_branch": pr.get("head", {}).get("ref", "")
                }
            })
        
        # Index the activity in Elasticsearch
        doc_id = f"{repo_name}_{event_type}_{activity_doc.get('timestamp', '')}"
        await elastic_service.index_document(
            index=settings.GITHUB_INDEX,
            doc_id=doc_id,
            document=activity_doc
        )
        
        logger.info(f"Processed {event_type} event for {repo_name}")
        
    except Exception as e:
        logger.error(f"Failed to process webhook event: {str(e)}")
        raise

@router.post("/setup-webhook")
async def setup_webhook(request: RepositoryRequest):
    """
    Instructions for setting up GitHub webhook
    """
    try:
        # Extract owner and repo from URL
        parts = request.repo_url.split("/")
        if len(parts) >= 2:
            owner = parts[-2]
            repo = parts[-1].replace(".git", "")
        else:
            raise HTTPException(status_code=400, detail="Invalid repository URL")
        
        webhook_url = f"{request.url_for('github_webhook')}"
        
        instructions = {
            "repository": f"{owner}/{repo}",
            "webhook_setup": {
                "url": webhook_url,
                "content_type": "application/json",
                "events": ["push", "issues", "pull_request"],
                "active": True
            },
            "setup_steps": [
                f"1. Go to https://github.com/{owner}/{repo}/settings/hooks",
                "2. Click 'Add webhook'",
                f"3. Set Payload URL to: {webhook_url}",
                "4. Set Content type to: application/json",
                "5. Select individual events: push, issues, pull_request",
                "6. Ensure 'Active' is checked",
                "7. Click 'Add webhook'"
            ],
            "verification": {
                "test_url": f"/api/v1/github/activity/{owner}/{repo}",
                "description": "Use this endpoint to verify the webhook is working"
            }
        }
        
        return instructions
        
    except Exception as e:
        logger.error(f"Webhook setup instructions failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate webhook setup instructions")
