"""
GitHub webhook endpoints for real-time progress tracking
"""

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import hmac
import hashlib
import json

from app.services.github_service import GitHubService
from app.services.elastic_service import ElasticService
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

class WebhookPayload(BaseModel):
    action: Optional[str] = None
    repository: Optional[Dict[str, Any]] = None
    commits: Optional[list] = None
    head_commit: Optional[Dict[str, Any]] = None
    pusher: Optional[Dict[str, Any]] = None

@router.post("/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """
    Handle GitHub webhook events for real-time progress tracking
    """
    try:
        # Get raw body and headers
        body = await request.body()
        signature = request.headers.get("X-Hub-Signature-256")
        event_type = request.headers.get("X-GitHub-Event")
        
        # Verify webhook signature
        if not _verify_signature(body, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse payload
        payload = json.loads(body.decode())
        
        logger.info(f"Received GitHub webhook: {event_type}")
        
        # Process different event types
        if event_type == "push":
            background_tasks.add_task(
                _process_push_event,
                payload
            )
        elif event_type == "pull_request":
            background_tasks.add_task(
                _process_pr_event,
                payload
            )
        elif event_type == "issues":
            background_tasks.add_task(
                _process_issue_event,
                payload
            )
        
        return {"status": "received", "event": event_type}
        
    except Exception as e:
        logger.error(f"Webhook processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")

async def _process_push_event(payload: Dict[str, Any]):
    """Process push events and update progress tracking"""
    try:
        elastic_service = ElasticService()
        
        repository = payload.get("repository", {})
        commits = payload.get("commits", [])
        pusher = payload.get("pusher", {})
        
        # Extract repository info
        repo_name = repository.get("full_name", "unknown")
        repo_url = repository.get("html_url", "")
        
        # Process each commit
        for commit in commits:
            commit_data = {
                "id": f"commit_{commit.get('id', '')}",
                "type": "commit",
                "repository": repo_name,
                "repository_url": repo_url,
                "commit_id": commit.get("id", ""),
                "message": commit.get("message", ""),
                "author": commit.get("author", {}).get("name", "Unknown"),
                "author_email": commit.get("author", {}).get("email", ""),
                "timestamp": commit.get("timestamp", ""),
                "url": commit.get("url", ""),
                "added_files": commit.get("added", []),
                "modified_files": commit.get("modified", []),
                "removed_files": commit.get("removed", []),
                "total_changes": len(commit.get("added", [])) + len(commit.get("modified", [])) + len(commit.get("removed", [])),
                "pusher": pusher.get("name", "Unknown"),
                "event_type": "push",
                "processed_at": "2024-10-24T12:00:00Z"
            }
            
            # Index in Elasticsearch
            await elastic_service.index_document(
                index=settings.GITHUB_INDEX,
                doc_id=commit_data["id"],
                document=commit_data
            )
            
        logger.info(f"Processed {len(commits)} commits from {repo_name}")
        
    except Exception as e:
        logger.error(f"Failed to process push event: {str(e)}")

async def _process_pr_event(payload: Dict[str, Any]):
    """Process pull request events"""
    try:
        elastic_service = ElasticService()
        
        action = payload.get("action", "")
        pull_request = payload.get("pull_request", {})
        repository = payload.get("repository", {})
        
        pr_data = {
            "id": f"pr_{pull_request.get('id', '')}",
            "type": "pull_request",
            "repository": repository.get("full_name", "unknown"),
            "repository_url": repository.get("html_url", ""),
            "pr_number": pull_request.get("number", 0),
            "title": pull_request.get("title", ""),
            "body": pull_request.get("body", ""),
            "state": pull_request.get("state", ""),
            "action": action,
            "author": pull_request.get("user", {}).get("login", "Unknown"),
            "created_at": pull_request.get("created_at", ""),
            "updated_at": pull_request.get("updated_at", ""),
            "url": pull_request.get("html_url", ""),
            "event_type": "pull_request",
            "processed_at": "2024-10-24T12:00:00Z"
        }
        
        await elastic_service.index_document(
            index=settings.GITHUB_INDEX,
            doc_id=pr_data["id"],
            document=pr_data
        )
        
        logger.info(f"Processed PR {action}: {pr_data['title']}")
        
    except Exception as e:
        logger.error(f"Failed to process PR event: {str(e)}")

async def _process_issue_event(payload: Dict[str, Any]):
    """Process issue events"""
    try:
        elastic_service = ElasticService()
        
        action = payload.get("action", "")
        issue = payload.get("issue", {})
        repository = payload.get("repository", {})
        
        issue_data = {
            "id": f"issue_{issue.get('id', '')}",
            "type": "issue",
            "repository": repository.get("full_name", "unknown"),
            "repository_url": repository.get("html_url", ""),
            "issue_number": issue.get("number", 0),
            "title": issue.get("title", ""),
            "body": issue.get("body", ""),
            "state": issue.get("state", ""),
            "action": action,
            "author": issue.get("user", {}).get("login", "Unknown"),
            "labels": [label.get("name", "") for label in issue.get("labels", [])],
            "created_at": issue.get("created_at", ""),
            "updated_at": issue.get("updated_at", ""),
            "url": issue.get("html_url", ""),
            "event_type": "issue",
            "processed_at": "2024-10-24T12:00:00Z"
        }
        
        await elastic_service.index_document(
            index=settings.GITHUB_INDEX,
            doc_id=issue_data["id"],
            document=issue_data
        )
        
        logger.info(f"Processed issue {action}: {issue_data['title']}")
        
    except Exception as e:
        logger.error(f"Failed to process issue event: {str(e)}")

def _verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """Verify GitHub webhook signature"""
    if not signature_header or not settings.GITHUB_WEBHOOK_SECRET:
        return False
    
    try:
        hash_object = hmac.new(
            settings.GITHUB_WEBHOOK_SECRET.encode('utf-8'),
            msg=payload_body,
            digestmod=hashlib.sha256
        )
        expected_signature = "sha256=" + hash_object.hexdigest()
        return hmac.compare_digest(expected_signature, signature_header)
    except Exception as e:
        logger.error(f"Signature verification failed: {str(e)}")
        return False

@router.get("/test")
async def test_webhook():
    """Test endpoint to verify webhook setup"""
    return {
        "status": "webhook endpoint active",
        "timestamp": "2024-10-24T12:00:00Z",
        "github_integration": "ready"
    }
