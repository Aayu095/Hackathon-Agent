'use client'

import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { 
  Zap, 
  Lightbulb, 
  BookOpen, 
  TrendingUp, 
  FileText, 
  Search,
  Database,
  Brain,
  GitBranch,
  Sparkles,
  ArrowRight,
  CheckCircle,
  Code,
  Cloud
} from 'lucide-react'

export default function FeaturesPage() {
  const router = useRouter()

  const features = [
    {
      icon: Lightbulb,
      title: 'Idea Validation',
      subtitle: 'Elastic Hybrid Search',
      description: 'Search 10,000+ past Devpost projects using Elastic\'s powerful hybrid search (BM25 + vector similarity). Validate originality, identify similar projects, and discover differentiation opportunities.',
      tech: ['Elastic Cloud', 'Vector Embeddings', 'BM25 Ranking'],
      demo: [
        'Input your project idea',
        'AI searches Devpost database',
        'Returns similar projects with relevance scores',
        'Provides originality assessment'
      ],
      color: 'from-yellow-500/20 to-orange-500/20',
      borderColor: 'border-yellow-500/30'
    },
    {
      icon: BookOpen,
      title: 'Contextual RAG',
      subtitle: 'Google Cloud Vertex AI',
      description: 'Ask questions about hackathon rules, partner technologies, and best practices. Our RAG system retrieves relevant documentation and generates accurate, cited answers using Vertex AI.',
      tech: ['Vertex AI Gemini', 'Retrieval Augmented Generation', 'Semantic Search'],
      demo: [
        'Ask technical questions',
        'System retrieves relevant docs',
        'Vertex AI generates answer',
        'Provides source citations'
      ],
      color: 'from-blue-500/20 to-cyan-500/20',
      borderColor: 'border-blue-500/30'
    },
    {
      icon: TrendingUp,
      title: 'Progress Agent',
      subtitle: 'GitHub Integration',
      description: 'Connect your GitHub repository and get real-time progress updates. The agent analyzes commits, tracks milestones, identifies blockers, and provides actionable insights.',
      tech: ['GitHub API', 'Commit Analysis', 'AI Summarization'],
      demo: [
        'Connect GitHub repository',
        'Agent monitors commits',
        'Analyzes development patterns',
        'Generates progress reports'
      ],
      color: 'from-green-500/20 to-emerald-500/20',
      borderColor: 'border-green-500/30'
    },
    {
      icon: FileText,
      title: 'Presentation Assistant',
      subtitle: 'Auto-Generate Pitches',
      description: 'Automatically generate pitch decks, README files, and demo scripts from your GitHub commits and project documentation. Save hours of presentation prep.',
      tech: ['Content Generation', 'Template Engine', 'Markdown Processing'],
      demo: [
        'Analyze project structure',
        'Extract key features',
        'Generate pitch outline',
        'Create README sections'
      ],
      color: 'from-purple-500/20 to-pink-500/20',
      borderColor: 'border-purple-500/30'
    }
  ]

  const techStack = [
    {
      category: 'Search & Database',
      items: [
        { name: 'Elastic Cloud', icon: Database, description: 'Hybrid search engine' },
        { name: 'Vector Embeddings', icon: Brain, description: 'Semantic similarity' }
      ]
    },
    {
      category: 'AI & ML',
      items: [
        { name: 'Vertex AI', icon: Cloud, description: 'Google Cloud AI platform' },
        { name: 'Gemini Pro', icon: Sparkles, description: 'Large language model' }
      ]
    },
    {
      category: 'Integration',
      items: [
        { name: 'GitHub API', icon: GitBranch, description: 'Repository analysis' },
        { name: 'FastAPI', icon: Code, description: 'Backend framework' }
      ]
    }
  ]

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Animated background */}
      <div className="fixed inset-0 animated-gradient opacity-50" />
      
      {/* Grid overlay */}
      <div className="fixed inset-0 bg-[linear-gradient(rgba(255,255,255,.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.03)_1px,transparent_1px)] bg-[size:100px_100px]" />

      {/* Content */}
      <div className="relative z-10">
        {/* Navigation */}
        <motion.nav
          initial={{ y: -100 }}
          animate={{ y: 0 }}
          transition={{ duration: 0.6 }}
          className="container mx-auto px-6 py-6 flex items-center justify-between"
        >
          <div className="flex items-center space-x-2">
            <Zap className="w-8 h-8 text-white" />
            <span className="text-2xl font-bold shimmer">Hackathon Agent</span>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => router.push('/landing')}
              className="px-6 py-2 text-white/80 hover:text-white transition-colors"
            >
              Home
            </button>
            <button
              onClick={() => router.push('/chat')}
              className="px-6 py-2 bg-white text-black rounded-lg hover:bg-white/90 transition-all glow-white font-medium"
            >
              Try Now
            </button>
          </div>
        </motion.nav>

        {/* Hero Section */}
        <section className="container mx-auto px-6 pt-20 pb-16">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-4xl mx-auto text-center"
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              Four Powerful <span className="shimmer">Features</span>
            </h1>
            <p className="text-xl text-white/60 mb-8">
              Real implementations using Elastic Cloud and Google Cloud Vertex AI
            </p>
            <div className="flex items-center justify-center space-x-8 text-sm text-white/60">
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                <span>Production Ready</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                <span>Real AI Integration</span>
              </div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                <span>Fully Functional</span>
              </div>
            </div>
          </motion.div>
        </section>

        {/* Features Grid */}
        <section className="container mx-auto px-6 py-16">
          <div className="space-y-24">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className={`max-w-6xl mx-auto ${index % 2 === 1 ? 'ml-auto' : ''}`}
              >
                <div className={`p-8 bg-gradient-to-br ${feature.color} border ${feature.borderColor} rounded-3xl glass`}>
                  <div className="grid md:grid-cols-2 gap-8">
                    {/* Left: Description */}
                    <div>
                      <div className="flex items-center space-x-4 mb-4">
                        <div className="w-16 h-16 bg-white/10 rounded-2xl flex items-center justify-center">
                          <feature.icon className="w-8 h-8 text-white" />
                        </div>
                        <div>
                          <h2 className="text-3xl font-bold">{feature.title}</h2>
                          <p className="text-white/60">{feature.subtitle}</p>
                        </div>
                      </div>
                      
                      <p className="text-lg text-white/80 mb-6">
                        {feature.description}
                      </p>
                      
                      <div className="mb-6">
                        <h4 className="text-sm font-semibold mb-3 text-white/80">Technology Stack:</h4>
                        <div className="flex flex-wrap gap-2">
                          {feature.tech.map((tech, idx) => (
                            <span
                              key={idx}
                              className="px-3 py-1 bg-white/10 border border-white/20 rounded-full text-xs"
                            >
                              {tech}
                            </span>
                          ))}
                        </div>
                      </div>
                      
                      <button
                        onClick={() => router.push('/chat')}
                        className="group px-6 py-3 bg-white text-black rounded-lg hover:bg-white/90 transition-all glow-white font-semibold flex items-center space-x-2"
                      >
                        <span>Try This Feature</span>
                        <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                      </button>
                    </div>
                    
                    {/* Right: Demo Flow */}
                    <div>
                      <h4 className="text-sm font-semibold mb-4 text-white/80">How It Works:</h4>
                      <div className="space-y-3">
                        {feature.demo.map((step, idx) => (
                          <div
                            key={idx}
                            className="flex items-start space-x-3 p-4 bg-white/5 border border-white/10 rounded-xl"
                          >
                            <div className="w-8 h-8 bg-white/10 rounded-full flex items-center justify-center flex-shrink-0 text-sm font-bold">
                              {idx + 1}
                            </div>
                            <p className="text-sm text-white/80 pt-1">{step}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Tech Stack */}
        <section className="container mx-auto px-6 py-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="max-w-6xl mx-auto"
          >
            <h2 className="text-4xl md:text-6xl font-bold mb-6 text-center">
              Built With <span className="shimmer">Best-in-Class</span> Technology
            </h2>
            <p className="text-xl text-white/60 mb-16 text-center">
              Production-ready stack powering real AI capabilities
            </p>
            
            <div className="grid md:grid-cols-3 gap-8">
              {techStack.map((category, idx) => (
                <div key={idx} className="space-y-4">
                  <h3 className="text-lg font-semibold text-white/80 mb-4">{category.category}</h3>
                  {category.items.map((item, itemIdx) => (
                    <div
                      key={itemIdx}
                      className="p-4 bg-white/5 border border-white/10 rounded-xl hover:bg-white/10 transition-all"
                    >
                      <div className="flex items-center space-x-3 mb-2">
                        <item.icon className="w-5 h-5 text-white" />
                        <span className="font-semibold">{item.name}</span>
                      </div>
                      <p className="text-sm text-white/60">{item.description}</p>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </motion.div>
        </section>

        {/* CTA Section */}
        <section className="container mx-auto px-6 py-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto text-center p-12 bg-white/5 border border-white/10 rounded-3xl glass"
          >
            <h2 className="text-4xl md:text-6xl font-bold mb-6">
              Ready to <span className="shimmer">Experience</span> It?
            </h2>
            <p className="text-xl text-white/60 mb-8">
              All features are fully functional and ready to impress judges
            </p>
            <button
              onClick={() => router.push('/chat')}
              className="group px-10 py-5 bg-white text-black rounded-lg hover:bg-white/90 transition-all glow-white font-bold text-xl flex items-center space-x-2 mx-auto"
            >
              <span>Start Using Now</span>
              <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
            </button>
          </motion.div>
        </section>

        {/* Footer */}
        <footer className="container mx-auto px-6 py-12 border-t border-white/10">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Zap className="w-6 h-6 text-white" />
              <span className="text-lg font-bold">Hackathon Agent</span>
            </div>
            <div className="text-white/60">
              Powered by Google Cloud & Elastic
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}
