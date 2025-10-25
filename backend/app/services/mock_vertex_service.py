"""
Mock Vertex AI service for demo/testing without Google Cloud
Provides realistic responses for hackathon demonstration
"""

import logging
from typing import List, Dict, Any, Optional
import random

logger = logging.getLogger(__name__)

class VertexService:
    def __init__(self):
        logger.warning("🔶 Using MOCK Vertex AI service - Demo mode enabled!")
        self.model_name = "gemini-pro-mock"
        self.location = "us-central1"
        self.embedding_dim = 768
    
    async def health_check(self) -> bool:
        """Mock health check - always returns True"""
        return True
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate mock embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            # Generate deterministic embeddings based on text hash
            seed = hash(text) % 10000
            random.seed(seed)
            embedding = [random.uniform(-1, 1) for _ in range(self.embedding_dim)]
            embeddings.append(embedding)
        return embeddings
    
    async def generate_single_embedding(self, text: str) -> List[float]:
        """Generate mock embedding for a single text"""
        embeddings = await self.generate_embeddings([text])
        return embeddings[0]
    
    async def generate_response(
        self, 
        prompt: str,
        context: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """Generate mock AI response"""
        
        # Detect query type and provide appropriate response
        prompt_lower = prompt.lower()
        
        # Idea validation responses
        if any(word in prompt_lower for word in ['idea', 'validate', 'project', 'build', 'create']):
            return self._generate_idea_validation_response(prompt, context)
        
        # Documentation/technical questions
        elif any(word in prompt_lower for word in ['how', 'what', 'elastic', 'search', 'implement', 'use']):
            return self._generate_documentation_response(prompt, context)
        
        # Progress/GitHub related
        elif any(word in prompt_lower for word in ['progress', 'commit', 'github', 'repository', 'development']):
            return self._generate_progress_response(prompt, context)
        
        # Presentation/pitch related
        elif any(word in prompt_lower for word in ['pitch', 'presentation', 'demo', 'slide']):
            return self._generate_presentation_response(prompt, context)
        
        # General conversation
        else:
            return self._generate_general_response(prompt, context)
    
    def _generate_idea_validation_response(self, prompt: str, context: Optional[str]) -> str:
        """Generate idea validation response"""
        return """Based on my analysis of similar projects in the Devpost database:

**Originality Assessment: 7.5/10**

Your idea shows good potential with some unique aspects. Here's what I found:

**Similar Projects Found:**
- 3 projects with similar core concepts
- 5 projects in the same problem space
- 2 projects using similar technology stack

**Key Differentiators:**
✅ Your approach to the problem is unique
✅ Technology combination hasn't been done exactly this way
✅ Target audience is underserved

**Recommendations:**
1. **Emphasize your unique value proposition** - Focus on what makes your solution different
2. **Highlight technical innovation** - Your use of hybrid search and AI is compelling
3. **Show clear use cases** - Demonstrate specific scenarios where your solution excels

**Market Opportunity:**
The problem space is validated by existing projects, but there's room for innovation. Your approach could capture a niche market.

**Next Steps:**
- Refine your pitch to highlight differentiators
- Build a strong demo showcasing unique features
- Prepare comparisons with existing solutions

Overall, this is a solid hackathon idea with good winning potential! 🚀"""
    
    def _generate_documentation_response(self, prompt: str, context: Optional[str]) -> str:
        """Generate documentation/technical response"""
        if 'elastic' in prompt.lower() or 'search' in prompt.lower():
            return """**Implementing Hybrid Search with Elastic**

Hybrid search combines the best of both worlds: keyword-based search (BM25) and semantic vector search.

**Step 1: Set Up Your Index**
```python
# Create index with vector field
PUT /my_index
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "content": { "type": "text" },
      "embedding": { 
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}
```

**Step 2: Implement Hybrid Query**
```python
# Combine BM25 and kNN search
query = {
  "query": {
    "multi_match": {
      "query": "your search term",
      "fields": ["title", "content"]
    }
  },
  "knn": {
    "field": "embedding",
    "query_vector": [0.1, 0.2, ...],  # From your embedding model
    "k": 10,
    "num_candidates": 100
  }
}
```

**Step 3: Generate Embeddings**
Use a model like Vertex AI's textembedding-gecko or sentence-transformers to create vector embeddings.

**Best Practices:**
- Use BM25 for exact keyword matching
- Use vectors for semantic similarity
- Combine scores for best results
- Tune boost values based on your use case

**Sources:**
- Elastic Documentation: Hybrid Search Guide
- Elastic Blog: Vector Search Best Practices"""
        
        return """I can help you with that! Based on the documentation and best practices:

**Key Points:**
1. Start with understanding the core concepts
2. Follow the official documentation step-by-step
3. Test incrementally as you build
4. Use examples from the community

**Implementation Steps:**
- Set up your development environment
- Configure necessary APIs and credentials
- Implement core functionality first
- Add advanced features iteratively
- Test thoroughly before deployment

**Resources:**
- Official documentation provides detailed guides
- Community examples show real-world usage
- Stack Overflow has solutions to common issues

Would you like me to elaborate on any specific aspect?"""
    
    def _generate_progress_response(self, prompt: str, context: Optional[str]) -> str:
        """Generate progress tracking response"""
        return """**📊 Project Progress Summary**

**Recent Activity Analysis:**
Based on your GitHub repository activity over the last 7 days:

**Development Velocity:** 🟢 Strong
- 23 commits across 3 contributors
- 15 files modified
- 847 lines added, 234 removed

**Key Milestones Completed:**
✅ Backend API implementation (100%)
✅ Frontend UI components (95%)
✅ Database integration (100%)
✅ Authentication system (90%)

**Current Focus Areas:**
🔄 Testing and bug fixes (in progress)
🔄 Documentation updates (70% complete)
⏳ Deployment preparation (pending)

**Blockers Identified:**
⚠️ API rate limiting needs optimization
⚠️ Mobile responsiveness on some components

**Recommendations:**
1. **Prioritize testing** - Allocate next 2 hours to comprehensive testing
2. **Fix mobile issues** - Quick wins for better demo
3. **Prepare deployment** - Set up production environment
4. **Polish documentation** - Judges will review your README

**Team Performance:**
Your team is on track! The commit frequency and code quality suggest you're well-positioned for a strong submission.

**Next 24 Hours:**
- Complete remaining 5% of UI
- Run full integration tests
- Deploy to production
- Record demo video
- Submit to Devpost

Keep up the momentum! 🚀"""
    
    def _generate_presentation_response(self, prompt: str, context: Optional[str]) -> str:
        """Generate presentation/pitch response"""
        return """**🎯 Pitch Deck Outline - Auto-Generated**

**Slide 1: Title**
- Project Name
- Tagline: "Transforming [problem] with AI-powered [solution]"
- Team names

**Slide 2: The Problem**
- Current pain points (3-4 bullets)
- Market size/impact
- Why this matters now

**Slide 3: Our Solution**
- High-level overview
- Key innovation
- How it works (simple diagram)

**Slide 4: Technology Stack**
- Google Cloud Vertex AI - AI/ML capabilities
- Elastic Hybrid Search - Intelligent search
- Modern web stack - Scalable architecture
- Why these technologies matter

**Slide 5: Key Features**
- Feature 1: [Primary capability]
- Feature 2: [Unique differentiator]
- Feature 3: [User benefit]
- Feature 4: [Technical innovation]

**Slide 6: Demo**
- Live demonstration
- Show real use cases
- Highlight user experience

**Slide 7: Market Opportunity**
- Target users
- Growth potential
- Competitive advantages

**Slide 8: What's Next**
- Roadmap for next 3-6 months
- Scaling strategy
- Vision for impact

**Slide 9: Team**
- Brief bios
- Relevant experience
- Why you're the right team

**Slide 10: Call to Action**
- Ask (if any)
- Contact information
- Thank you

**Demo Script Suggestions:**
1. Start with the problem (30 seconds)
2. Show solution in action (90 seconds)
3. Highlight technical innovation (30 seconds)
4. Close with impact (30 seconds)

Total: ~3 minutes - perfect for hackathon pitches!"""
    
    def _generate_general_response(self, prompt: str, context: Optional[str]) -> str:
        """Generate general conversation response"""
        return f"""I'm your Hackathon Agent assistant! I can help you with:

**💡 Idea Validation**
- Search similar projects on Devpost
- Assess originality and market fit
- Suggest improvements

**📚 Technical Questions**
- Answer questions about Elastic, Google Cloud, and other technologies
- Provide code examples and best practices
- Help troubleshoot issues

**📈 Progress Tracking**
- Analyze your GitHub activity
- Identify blockers and suggest priorities
- Keep your team aligned

**🎤 Presentation Help**
- Generate pitch deck outlines
- Create demo scripts
- Suggest talking points

What would you like help with? Feel free to ask me anything about your hackathon project!"""
    
    async def generate_idea_validation_response(
        self, 
        idea_description: str,
        similar_projects: List[Dict[str, Any]]
    ) -> str:
        """Generate idea validation with similar projects context"""
        num_projects = len(similar_projects)
        
        response = f"""**🔍 Idea Validation Results**

I've analyzed your idea against {num_projects} similar projects from Devpost.

**Your Idea:** {idea_description[:200]}...

**Originality Score: {random.randint(65, 90)}/100**

**Similar Projects Found:** {num_projects}
"""
        
        if similar_projects:
            response += "\n**Top Similar Projects:**\n"
            for i, project in enumerate(similar_projects[:3], 1):
                title = project.get('_source', {}).get('title', 'Untitled Project')
                response += f"{i}. {title}\n"
        
        response += """
**Analysis:**
✅ Your concept has unique elements that differentiate it
✅ The technology stack you're using is innovative
✅ Market validation exists (similar projects show demand)
⚠️ Focus on your unique value proposition to stand out

**Recommendations:**
1. Emphasize what makes your approach different
2. Highlight technical innovations
3. Show clear use cases and benefits
4. Prepare strong demo showcasing unique features

**Competitive Advantages:**
- Novel application of existing technologies
- Better user experience
- More comprehensive solution
- Scalable architecture

This is a solid hackathon idea with good winning potential! 🚀"""
        
        return response
    
    async def generate_progress_summary(
        self, 
        github_activity: List[Dict[str, Any]]
    ) -> str:
        """Generate progress summary from GitHub activity"""
        num_activities = len(github_activity)
        
        return f"""**📊 Development Progress Report**

**Activity Summary:**
- {num_activities} recent activities tracked
- Active development in progress
- Team collaboration detected

**Recent Commits:**
Your team has been making steady progress with regular commits. The development velocity suggests you're on track for completion.

**Key Achievements:**
✅ Core functionality implemented
✅ Integration points established
✅ Testing framework in place

**Current Status:**
🔄 Active development phase
🔄 Feature completion in progress
🔄 Documentation being updated

**Recommendations:**
1. **Focus on polish** - Refine user experience
2. **Test thoroughly** - Ensure stability for demo
3. **Prepare presentation** - Start working on pitch
4. **Document well** - Judges review your README

**Timeline:**
You're in good shape! Continue current momentum and you'll have a strong submission.

**Next Steps:**
- Complete remaining features
- Run integration tests
- Record demo video
- Polish presentation

Keep up the great work! 🎯"""
    
    async def build_comprehensive_prompt(
        self,
        user_query: str,
        context_type: str,
        retrieved_context: Optional[List[Dict[str, Any]]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Build comprehensive prompt (mock - just returns user query)"""
        return user_query
