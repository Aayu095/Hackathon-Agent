"""
Google Vertex AI service for LLM and embeddings
"""

import logging
from typing import List, Dict, Any, Optional
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vertexai.language_models import TextEmbeddingModel
from app.core.config import settings

logger = logging.getLogger(__name__)

class VertexService:
    def __init__(self):
        # Initialize Vertex AI
        vertexai.init(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.VERTEX_AI_LOCATION
        )
        
        # Initialize models
        self.generative_model = GenerativeModel(settings.GEMINI_MODEL)
        self.embedding_model = TextEmbeddingModel.from_pretrained(settings.EMBEDDING_MODEL)
        
        self.model_name = settings.GEMINI_MODEL
        self.location = settings.VERTEX_AI_LOCATION
    
    async def health_check(self) -> bool:
        """Check if Vertex AI is accessible"""
        try:
            # Simple test generation
            response = self.generative_model.generate_content(
                "Hello",
                generation_config={
                    "max_output_tokens": 10,
                    "temperature": 0.1
                }
            )
            return bool(response.text)
        except Exception as e:
            logger.error(f"Vertex AI health check failed: {str(e)}")
            return False
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        try:
            import asyncio
            # Run sync method in thread pool to make it async
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None, self.embedding_model.get_embeddings, texts
            )
            return [embedding.values for embedding in embeddings]
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            return []
    
    async def generate_single_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        try:
            embeddings = await self.generate_embeddings([text])
            return embeddings[0] if embeddings else []
        except Exception as e:
            logger.error(f"Single embedding generation failed: {str(e)}")
            return []
    
    async def generate_response(
        self, 
        prompt: str,
        context: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        max_tokens: int = None,
        temperature: float = None
    ) -> str:
        """Generate a response using Gemini Pro"""
        try:
            # Build the full prompt
            full_prompt = self._build_prompt(prompt, context, conversation_history)
            
            # Set generation config
            generation_config = {
                "max_output_tokens": max_tokens or settings.MAX_TOKENS,
                "temperature": temperature or settings.TEMPERATURE,
                "top_p": 0.95,
                "top_k": 40
            }
            
            # Generate response asynchronously
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.generative_model.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Response generation failed: {str(e)}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again."
    
    def _build_prompt(
        self, 
        user_query: str,
        context: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Build a comprehensive prompt for the AI agent"""
        
        system_prompt = """You are an expert AI-powered Hackathon Agent designed to help teams excel in hackathons. You are knowledgeable about:

1. Hackathon best practices and winning strategies
2. Google Cloud services (Vertex AI, Cloud Run, BigQuery, etc.)
3. Elastic search and hybrid search capabilities
4. Software development and project management
5. Presentation and pitching techniques
6. Technical implementation and architecture decisions

Your role is to:
- Provide helpful, accurate, and actionable advice based on retrieved information
- Help validate project ideas by analyzing similar past projects
- Answer questions about hackathon rules and partner technologies using official documentation
- Assist with progress tracking using real-time GitHub data
- Help create compelling presentations and pitches
- Always cite your sources when providing information

IMPORTANT INSTRUCTIONS:
- When provided with relevant information from documentation, projects, or GitHub activity, USE IT to inform your responses
- Be specific and reference the retrieved information directly
- If similar projects exist, help differentiate the user's idea
- Always be encouraging while being honest about challenges
- Provide actionable next steps and specific recommendations
- Format responses clearly with headers, bullet points, and emojis for better readability"""

        prompt_parts = [system_prompt]
        
        # Add conversation history
        if conversation_history:
            prompt_parts.append("\n--- Conversation History ---")
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt_parts.append(f"{role.capitalize()}: {content}")
        
        # Add context from search results
        if context:
            prompt_parts.append(f"\n--- Relevant Information ---\n{context}")
        
        # Add current user query
        prompt_parts.append(f"\n--- Current Question ---\nUser: {user_query}")
        prompt_parts.append("\nAssistant:")
        
        return "\n".join(prompt_parts)
    
    async def generate_idea_validation_response(
        self, 
        idea_description: str,
        similar_projects: List[Dict[str, Any]]
    ) -> str:
        """Generate a response for idea validation"""
        try:
            context = self._format_similar_projects(similar_projects)
            
            prompt = f"""
Please analyze this hackathon project idea and provide validation feedback:

Project Idea: {idea_description}

Based on the similar projects found, please provide:
1. Originality assessment (is this idea unique enough?)
2. Potential challenges and pitfalls to avoid
3. Suggestions for differentiation
4. Technical feasibility assessment
5. Recommendations for improvement

Be constructive and encouraging while being honest about potential issues.
"""
            
            return await self.generate_response(prompt, context)
            
        except Exception as e:
            logger.error(f"Idea validation response generation failed: {str(e)}")
            return "I'm having trouble analyzing your idea right now. Please try again."
    
    async def generate_progress_summary(
        self, 
        github_activity: List[Dict[str, Any]]
    ) -> str:
        """Generate a progress summary from GitHub activity"""
        try:
            context = self._format_github_activity(github_activity)
            
            prompt = """
Based on the recent GitHub activity, please provide a comprehensive progress summary including:

1. Key accomplishments and milestones reached
2. Current development focus areas
3. Potential blockers or challenges
4. Recommendations for next steps
5. Overall project health assessment

Be specific about the technical progress and provide actionable insights.
"""
            
            return await self.generate_response(prompt, context)
            
        except Exception as e:
            logger.error(f"Progress summary generation failed: {str(e)}")
            return "I'm having trouble analyzing your progress right now. Please try again."
    
    def _format_similar_projects(self, projects: List[Dict[str, Any]]) -> str:
        """Format similar projects for context"""
        if not projects:
            return "No similar projects found in the database."
        
        formatted = ["Similar Projects Found:"]
        for i, project in enumerate(projects[:3], 1):
            formatted.append(f"""
{i}. {project.get('title', 'Unknown Title')}
   Description: {project.get('description', 'No description')[:200]}...
   Technologies: {', '.join(project.get('technologies', []))}
   Category: {project.get('category', 'Unknown')}
   Year: {project.get('year', 'Unknown')}
   Relevance Score: {project.get('score', 0):.2f}
""")
        
        return "\n".join(formatted)
    
    def _format_github_activity(self, activity: List[Dict[str, Any]]) -> str:
        """Format GitHub activity for context"""
        if not activity:
            return "No recent GitHub activity found."
        
        formatted = ["Recent GitHub Activity:"]
        for item in activity[:10]:  # Last 10 activities
            formatted.append(f"""
- {item.get('type', 'Unknown')}: {item.get('message', 'No message')}
  Author: {item.get('author', 'Unknown')}
  Time: {item.get('timestamp', 'Unknown')}
  Files: {', '.join(item.get('files', [])[:3])}
""")
        
        return "\n".join(formatted)
