"""
GitHub integration service for progress tracking
"""

import logging
from typing import List, Dict, Any, Optional
from github import Github
import requests
from datetime import datetime, timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self):
        self.github = Github(settings.GITHUB_TOKEN) if settings.GITHUB_TOKEN else None
        self.webhook_secret = settings.GITHUB_WEBHOOK_SECRET
    
    async def health_check(self) -> bool:
        """Check GitHub API accessibility"""
        try:
            if not self.github:
                return False
            user = self.github.get_user()
            return bool(user.login)
        except Exception as e:
            logger.error(f"GitHub health check failed: {str(e)}")
            return False
    
    async def get_repository_activity(
        self, 
        repo_url: str, 
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """Get recent repository activity"""
        try:
            # Extract owner and repo name from URL
            owner, repo_name = self._parse_repo_url(repo_url)
            if not owner or not repo_name:
                return []
            
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # Get commits from the last N days
            since = datetime.now() - timedelta(days=days)
            commits = repo.get_commits(since=since)
            
            activity = []
            for commit in commits:
                activity.append({
                    "type": "commit",
                    "message": commit.commit.message,
                    "author": commit.commit.author.name,
                    "timestamp": commit.commit.author.date.isoformat(),
                    "sha": commit.sha,
                    "url": commit.html_url,
                    "files": [f.filename for f in commit.files] if commit.files else []
                })
            
            # Get recent issues
            issues = repo.get_issues(state="all", since=since)
            for issue in issues:
                activity.append({
                    "type": "issue",
                    "message": f"Issue: {issue.title}",
                    "author": issue.user.login,
                    "timestamp": issue.created_at.isoformat(),
                    "state": issue.state,
                    "url": issue.html_url,
                    "labels": [label.name for label in issue.labels]
                })
            
            # Sort by timestamp
            activity.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return activity[:20]  # Return last 20 activities
            
        except Exception as e:
            logger.error(f"Failed to get repository activity: {str(e)}")
            return []
    
    async def get_repository_stats(self, repo_url: str) -> Dict[str, Any]:
        """Get repository statistics"""
        try:
            owner, repo_name = self._parse_repo_url(repo_url)
            if not owner or not repo_name:
                return {}
            
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            # Get language statistics
            languages = repo.get_languages()
            
            # Get contributor statistics
            contributors = repo.get_contributors()
            contributor_stats = []
            for contributor in contributors:
                contributor_stats.append({
                    "login": contributor.login,
                    "contributions": contributor.contributions,
                    "avatar_url": contributor.avatar_url
                })
            
            # Get recent releases
            releases = repo.get_releases()
            recent_releases = []
            for release in releases[:3]:  # Last 3 releases
                recent_releases.append({
                    "name": release.title or release.tag_name,
                    "tag": release.tag_name,
                    "published_at": release.published_at.isoformat() if release.published_at else None,
                    "url": release.html_url
                })
            
            return {
                "name": repo.name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "open_issues": repo.open_issues_count,
                "languages": languages,
                "contributors": contributor_stats,
                "recent_releases": recent_releases,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat(),
                "default_branch": repo.default_branch
            }
            
        except Exception as e:
            logger.error(f"Failed to get repository stats: {str(e)}")
            return {}
    
    async def analyze_project_progress(self, repo_url: str) -> Dict[str, Any]:
        """Analyze project progress based on GitHub activity"""
        try:
            activity = await self.get_repository_activity(repo_url)
            stats = await self.get_repository_stats(repo_url)
            
            if not activity and not stats:
                return {"error": "Unable to analyze repository"}
            
            # Analyze commit patterns
            commit_analysis = self._analyze_commits(activity)
            
            # Analyze file changes
            file_analysis = self._analyze_file_changes(activity)
            
            # Calculate progress metrics
            progress_metrics = self._calculate_progress_metrics(activity, stats)
            
            return {
                "repository": stats.get("name", "Unknown"),
                "analysis_period": "Last 7 days",
                "commit_analysis": commit_analysis,
                "file_analysis": file_analysis,
                "progress_metrics": progress_metrics,
                "recent_activity": activity[:5],  # Last 5 activities
                "recommendations": self._generate_recommendations(activity, stats)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze project progress: {str(e)}")
            return {"error": str(e)}
    
    def _parse_repo_url(self, repo_url: str) -> tuple:
        """Parse GitHub repository URL to extract owner and repo name"""
        try:
            # Handle different URL formats
            if "github.com" in repo_url:
                parts = repo_url.split("/")
                if len(parts) >= 2:
                    owner = parts[-2]
                    repo_name = parts[-1].replace(".git", "")
                    return owner, repo_name
            return None, None
        except Exception:
            return None, None
    
    def _analyze_commits(self, activity: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze commit patterns"""
        commits = [a for a in activity if a["type"] == "commit"]
        
        if not commits:
            return {"total_commits": 0, "message": "No commits found"}
        
        # Analyze commit frequency
        commit_days = {}
        for commit in commits:
            day = commit["timestamp"][:10]  # YYYY-MM-DD
            commit_days[day] = commit_days.get(day, 0) + 1
        
        # Analyze commit messages
        message_analysis = self._analyze_commit_messages([c["message"] for c in commits])
        
        return {
            "total_commits": len(commits),
            "commit_frequency": commit_days,
            "average_per_day": len(commits) / max(len(commit_days), 1),
            "message_analysis": message_analysis,
            "most_active_author": self._get_most_active_author(commits)
        }
    
    def _analyze_file_changes(self, activity: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze file change patterns"""
        commits = [a for a in activity if a["type"] == "commit"]
        
        if not commits:
            return {"message": "No file changes found"}
        
        file_changes = {}
        file_types = {}
        
        for commit in commits:
            for file in commit.get("files", []):
                file_changes[file] = file_changes.get(file, 0) + 1
                
                # Analyze file types
                if "." in file:
                    ext = file.split(".")[-1].lower()
                    file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            "total_files_changed": len(file_changes),
            "most_changed_files": sorted(file_changes.items(), key=lambda x: x[1], reverse=True)[:5],
            "file_types": file_types,
            "development_focus": self._determine_development_focus(file_types)
        }
    
    def _calculate_progress_metrics(
        self, 
        activity: List[Dict[str, Any]], 
        stats: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate progress metrics"""
        commits = [a for a in activity if a["type"] == "commit"]
        issues = [a for a in activity if a["type"] == "issue"]
        
        return {
            "activity_score": len(activity),
            "commit_velocity": len(commits),
            "issue_activity": len(issues),
            "contributor_count": len(stats.get("contributors", [])),
            "project_maturity": self._assess_project_maturity(stats),
            "development_intensity": "High" if len(commits) > 10 else "Medium" if len(commits) > 5 else "Low"
        }
    
    def _analyze_commit_messages(self, messages: List[str]) -> Dict[str, Any]:
        """Analyze commit message patterns"""
        if not messages:
            return {}
        
        # Common patterns
        patterns = {
            "feature": ["feat", "feature", "add", "implement"],
            "fix": ["fix", "bug", "patch", "resolve"],
            "refactor": ["refactor", "clean", "improve", "optimize"],
            "docs": ["doc", "readme", "comment", "documentation"],
            "style": ["style", "format", "lint", "prettier"],
            "test": ["test", "spec", "coverage"]
        }
        
        categorized = {category: 0 for category in patterns}
        
        for message in messages:
            message_lower = message.lower()
            for category, keywords in patterns.items():
                if any(keyword in message_lower for keyword in keywords):
                    categorized[category] += 1
                    break
        
        return categorized
    
    def _get_most_active_author(self, commits: List[Dict[str, Any]]) -> str:
        """Get the most active commit author"""
        if not commits:
            return "Unknown"
        
        authors = {}
        for commit in commits:
            author = commit.get("author", "Unknown")
            authors[author] = authors.get(author, 0) + 1
        
        return max(authors.items(), key=lambda x: x[1])[0] if authors else "Unknown"
    
    def _determine_development_focus(self, file_types: Dict[str, int]) -> str:
        """Determine the main development focus based on file types"""
        if not file_types:
            return "Unknown"
        
        focus_mapping = {
            "py": "Backend Development",
            "js": "Frontend Development", 
            "ts": "Frontend Development",
            "tsx": "Frontend Development",
            "jsx": "Frontend Development",
            "html": "Frontend Development",
            "css": "Frontend Development",
            "scss": "Frontend Development",
            "md": "Documentation",
            "yml": "DevOps/Configuration",
            "yaml": "DevOps/Configuration",
            "json": "Configuration",
            "sql": "Database Development"
        }
        
        most_common_ext = max(file_types.items(), key=lambda x: x[1])[0]
        return focus_mapping.get(most_common_ext, "General Development")
    
    def _assess_project_maturity(self, stats: Dict[str, Any]) -> str:
        """Assess project maturity based on various metrics"""
        if not stats:
            return "Unknown"
        
        # Simple maturity assessment
        contributors = len(stats.get("contributors", []))
        releases = len(stats.get("recent_releases", []))
        
        if contributors >= 3 and releases >= 1:
            return "Mature"
        elif contributors >= 2 or releases >= 1:
            return "Developing"
        else:
            return "Early Stage"
    
    def _generate_recommendations(
        self, 
        activity: List[Dict[str, Any]], 
        stats: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        commits = [a for a in activity if a["type"] == "commit"]
        
        if len(commits) < 5:
            recommendations.append("Consider increasing commit frequency for better progress tracking")
        
        if not stats.get("recent_releases"):
            recommendations.append("Consider creating releases to mark project milestones")
        
        if len(stats.get("contributors", [])) == 1:
            recommendations.append("Encourage team collaboration with more contributors")
        
        if stats.get("open_issues", 0) > 10:
            recommendations.append("Focus on resolving open issues to maintain project health")
        
        return recommendations
