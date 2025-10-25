"""
Devpost Data Ingestion Script
Scrapes and indexes Devpost hackathon projects for idea validation
"""

import asyncio
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import json
import time
from datetime import datetime
import sys
import os

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.elastic_service import ElasticService
from app.services.vertex_service import VertexService
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DevpostScraper:
    def __init__(self):
        self.base_url = "https://devpost.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_hackathon_projects(self, hackathon_slug: str, max_pages: int = 5) -> List[Dict[str, Any]]:
        """Scrape projects from a specific hackathon"""
        projects = []
        
        for page in range(1, max_pages + 1):
            try:
                url = f"{self.base_url}/hackathons/{hackathon_slug}/project-gallery?page={page}"
                logger.info(f"Scraping page {page}: {url}")
                
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                project_cards = soup.find_all('div', class_='software-entry')
                
                if not project_cards:
                    logger.info(f"No more projects found on page {page}")
                    break
                
                for card in project_cards:
                    project = self.extract_project_info(card, hackathon_slug)
                    if project:
                        projects.append(project)
                
                # Be respectful with rate limiting
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error scraping page {page}: {str(e)}")
                continue
        
        return projects
    
    def extract_project_info(self, card_element, hackathon_slug: str) -> Dict[str, Any]:
        """Extract project information from a project card"""
        try:
            # Project title and URL
            title_elem = card_element.find('h5') or card_element.find('a', class_='link-to-software')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Project"
            
            project_url = ""
            if title_elem and title_elem.get('href'):
                project_url = self.base_url + title_elem['href']
            
            # Project description
            description_elem = card_element.find('p', class_='small')
            description = description_elem.get_text(strip=True) if description_elem else ""
            
            # Technologies/tags
            tech_elements = card_element.find_all('span', class_='cp-tag')
            technologies = [tech.get_text(strip=True) for tech in tech_elements]
            
            # Team members
            team_elem = card_element.find('div', class_='user-profile-link')
            team_members = []
            if team_elem:
                member_links = team_elem.find_all('a')
                team_members = [link.get_text(strip=True) for link in member_links]
            
            return {
                "id": f"{hackathon_slug}_{title.lower().replace(' ', '_')}",
                "title": title,
                "description": description,
                "url": project_url,
                "technologies": technologies,
                "team_members": team_members,
                "hackathon": hackathon_slug,
                "category": "hackathon_project",
                "year": datetime.now().year,
                "scraped_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error extracting project info: {str(e)}")
            return None
    
    def get_popular_projects(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Scrape popular projects from Devpost"""
        projects = []
        
        try:
            # Get projects from popular/trending page
            url = f"{self.base_url}/software/popular"
            logger.info(f"Scraping popular projects: {url}")
            
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            project_cards = soup.find_all('div', class_='software-entry')[:limit]
            
            for card in project_cards:
                project = self.extract_project_info(card, "popular")
                if project:
                    projects.append(project)
            
        except Exception as e:
            logger.error(f"Error scraping popular projects: {str(e)}")
        
        return projects

class DevpostDataIngestion:
    def __init__(self):
        self.elastic_service = ElasticService()
        self.vertex_service = VertexService()
        self.scraper = DevpostScraper()
    
    async def create_devpost_index(self):
        """Create Elasticsearch index for Devpost projects"""
        mapping = {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "description": {
                    "type": "text",
                    "analyzer": "standard"
                },
                "technologies": {
                    "type": "keyword"
                },
                "team_members": {
                    "type": "keyword"
                },
                "hackathon": {
                    "type": "keyword"
                },
                "category": {
                    "type": "keyword"
                },
                "year": {
                    "type": "integer"
                },
                "url": {
                    "type": "keyword"
                },
                "embedding": {
                    "type": "dense_vector",
                    "dims": 768
                },
                "scraped_at": {
                    "type": "date"
                }
            }
        }
        
        success = await self.elastic_service.create_index(settings.DEVPOST_INDEX, mapping)
        if success:
            logger.info(f"Created index: {settings.DEVPOST_INDEX}")
        else:
            logger.warning(f"Index {settings.DEVPOST_INDEX} might already exist")
    
    async def process_and_index_projects(self, projects: List[Dict[str, Any]]):
        """Process projects and index them with embeddings"""
        logger.info(f"Processing {len(projects)} projects...")
        
        for project in projects:
            try:
                # Generate embedding for the project
                text_for_embedding = f"{project['title']} {project['description']} {' '.join(project['technologies'])}"
                embedding = await self.vertex_service.generate_single_embedding(text_for_embedding)
                
                if embedding:
                    project['embedding'] = embedding
                
                # Index the project
                success = await self.elastic_service.index_document(
                    index=settings.DEVPOST_INDEX,
                    doc_id=project['id'],
                    document=project
                )
                
                if success:
                    logger.info(f"Indexed project: {project['title']}")
                else:
                    logger.error(f"Failed to index project: {project['title']}")
                
                # Rate limiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error processing project {project.get('title', 'Unknown')}: {str(e)}")
    
    async def run_ingestion(self):
        """Run the complete data ingestion process"""
        logger.info("Starting Devpost data ingestion...")
        
        # Create index
        await self.create_devpost_index()
        
        # Sample hackathons to scrape (you can expand this list)
        hackathons_to_scrape = [
            "google-ai-hackathon",
            "openai-hackathon", 
            "microsoft-hackathon",
            "aws-hackathon",
            "ethereum-hackathon"
        ]
        
        all_projects = []
        
        # Scrape popular projects first
        logger.info("Scraping popular projects...")
        popular_projects = self.scraper.get_popular_projects(limit=50)
        all_projects.extend(popular_projects)
        
        # Scrape specific hackathons
        for hackathon in hackathons_to_scrape:
            logger.info(f"Scraping hackathon: {hackathon}")
            try:
                projects = self.scraper.get_hackathon_projects(hackathon, max_pages=3)
                all_projects.extend(projects)
                logger.info(f"Found {len(projects)} projects from {hackathon}")
            except Exception as e:
                logger.error(f"Error scraping {hackathon}: {str(e)}")
        
        # Process and index all projects
        if all_projects:
            await self.process_and_index_projects(all_projects)
            logger.info(f"✅ Ingestion completed! Indexed {len(all_projects)} projects.")
        else:
            logger.warning("No projects found to index.")

async def main():
    """Main function to run the ingestion"""
    try:
        ingestion = DevpostDataIngestion()
        await ingestion.run_ingestion()
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
