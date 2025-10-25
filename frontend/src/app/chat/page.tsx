'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { 
  Zap, 
  Send, 
  Menu, 
  Plus, 
  Settings, 
  LogOut, 
  Github, 
  MessageSquare,
  Sparkles,
  User,
  ChevronDown,
  Search,
  Clock,
  Lightbulb,
  BookOpen,
  TrendingUp,
  FileText,
  ExternalLink,
  CheckCircle
} from 'lucide-react'
import { apiClient, ChatMessage, ChatResponse } from '@/lib/api'
import toast, { Toaster } from 'react-hot-toast'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  sources?: any[]
  suggestions?: string[]
}

interface QuickAction {
  id: string
  icon: any
  title: string
  description: string
  action: () => void
  color: string
}

export default function ChatPage() {
  const router = useRouter()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: '👋 Hello! I\'m your AI-powered Hackathon Agent. I can help you:\n\n🎯 **Validate Ideas** - Search 10,000+ past Devpost projects\n📚 **Answer Questions** - RAG on official documentation\n📊 **Track Progress** - Monitor your GitHub repository\n🎤 **Generate Presentations** - Auto-create pitch decks\n\nWhat would you like to do?',
      timestamp: new Date()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [repoUrl, setRepoUrl] = useState('')
  const [showRepoInput, setShowRepoInput] = useState(false)
  const [currentSuggestions, setCurrentSuggestions] = useState<string[]>([])
  const [conversationId, setConversationId] = useState('1')
  const [showSettings, setShowSettings] = useState(false)

  const conversations = [
    { id: '1', title: 'Idea Validation Session', time: '2 hours ago', active: true },
    { id: '2', title: 'Progress Check', time: 'Yesterday', active: false },
    { id: '3', title: 'Presentation Help', time: '2 days ago', active: false }
  ]

  const quickActions: QuickAction[] = [
    {
      id: 'validate',
      icon: Lightbulb,
      title: 'Validate Idea',
      description: 'Search similar projects on Devpost',
      action: () => setInputValue('I want to validate my project idea: '),
      color: 'from-yellow-500/20 to-orange-500/20'
    },
    {
      id: 'docs',
      icon: BookOpen,
      title: 'Ask Documentation',
      description: 'Query hackathon rules & tech docs',
      action: () => setInputValue('How do I use '),
      color: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      id: 'progress',
      icon: TrendingUp,
      title: 'Check Progress',
      description: 'Analyze GitHub commits',
      action: () => handleProgressCheck(),
      color: 'from-green-500/20 to-emerald-500/20'
    },
    {
      id: 'presentation',
      icon: FileText,
      title: 'Generate Pitch',
      description: 'Auto-create presentation',
      action: () => handleGeneratePitch(),
      color: 'from-purple-500/20 to-pink-500/20'
    }
  ]

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    const currentInput = inputValue
    setInputValue('')
    setIsTyping(true)

    try {
      // Detect intent and call appropriate endpoint
      const intent = detectIntent(currentInput)
      
      let response: ChatResponse

      if (intent === 'idea_validation') {
        response = await apiClient.validateIdea(currentInput, messages)
        toast.success('Searched 10,000+ Devpost projects!')
      } else if (intent === 'progress' && repoUrl) {
        response = await apiClient.getProgressReport(repoUrl, messages)
        toast.success('Analyzed GitHub repository!')
      } else {
        // General chat with RAG
        response = await apiClient.sendMessage({
          message: currentInput,
          conversation_history: messages.map(m => ({
            role: m.role,
            content: m.content,
            timestamp: m.timestamp.toISOString()
          })),
          repo_url: repoUrl || undefined,
          context_type: intent
        })
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
        sources: response.sources,
        suggestions: response.suggestions
      }

      setMessages(prev => [...prev, aiMessage])
      setCurrentSuggestions(response.suggestions || [])
      setIsTyping(false)

    } catch (error: any) {
      console.error('Chat error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '❌ Sorry, I encountered an error. Please make sure the backend is running and try again.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
      setIsTyping(false)
      toast.error('Failed to get response. Check backend connection.')
    }
  }

  const detectIntent = (message: string): string => {
    const lower = message.toLowerCase()
    if (lower.includes('idea') || lower.includes('validate') || lower.includes('similar') || lower.includes('project')) {
      return 'idea_validation'
    }
    if (lower.includes('progress') || lower.includes('commit') || lower.includes('github')) {
      return 'progress'
    }
    if (lower.includes('how to') || lower.includes('documentation') || lower.includes('elastic') || lower.includes('google cloud')) {
      return 'documentation'
    }
    return 'general'
  }

  const handleProgressCheck = () => {
    if (!repoUrl) {
      setShowRepoInput(true)
      toast.error('Please connect your GitHub repository first')
      return
    }
    setInputValue('What is our current development progress?')
  }

  const handleGeneratePitch = () => {
    if (!repoUrl) {
      setShowRepoInput(true)
      toast.error('Please connect your GitHub repository first')
      return
    }
    setInputValue('Generate a pitch deck for our project based on our GitHub commits')
  }

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion)
  }

  const handleConnectRepo = () => {
    if (repoUrl.trim()) {
      toast.success('Repository connected!')
      setShowRepoInput(false)
    }
  }

  const handleNewChat = () => {
    // Clear messages and start fresh
    setMessages([{
      id: Date.now().toString(),
      role: 'assistant',
      content: '👋 Hello! I\'m your AI-powered Hackathon Agent. I can help you:\n\n🎯 **Validate Ideas** - Search 10,000+ past Devpost projects\n📚 **Answer Questions** - RAG on official documentation\n📊 **Track Progress** - Monitor your GitHub repository\n🎤 **Generate Presentations** - Auto-create pitch decks\n\nWhat would you like to do?',
      timestamp: new Date()
    }])
    setInputValue('')
    setCurrentSuggestions([])
    setConversationId(Date.now().toString())
    toast.success('New chat started!')
  }

  const handleSettingsClick = () => {
    setShowSettings(true)
  }

  return (
    <div className="h-screen bg-black text-white flex overflow-hidden">
      {/* Animated background */}
      <div className="fixed inset-0 animated-gradient opacity-30" />
      
      {/* Grid overlay */}
      <div className="fixed inset-0 bg-[linear-gradient(rgba(255,255,255,.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.02)_1px,transparent_1px)] bg-[size:100px_100px]" />

      {/* Sidebar */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.aside
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            transition={{ duration: 0.3 }}
            className="relative z-20 w-80 bg-white/5 border-r border-white/10 backdrop-blur-xl flex flex-col"
          >
            {/* Sidebar Header */}
            <div className="p-6 border-b border-white/10">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-2">
                  <Zap className="w-6 h-6 text-white" />
                  <span className="text-lg font-bold">Hackathon Agent</span>
                </div>
                <button
                  onClick={() => setSidebarOpen(false)}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors lg:hidden"
                >
                  <Menu className="w-5 h-5" />
                </button>
              </div>
              
              <button 
                onClick={handleNewChat}
                className="w-full px-4 py-3 bg-white text-black rounded-lg hover:bg-white/90 transition-all glow-white font-semibold flex items-center justify-center space-x-2"
              >
                <Plus className="w-5 h-5" />
                <span>New Chat</span>
              </button>
            </div>

            {/* Search */}
            <div className="p-4 border-b border-white/10">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/40" />
                <input
                  type="text"
                  placeholder="Search conversations..."
                  className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-white/30 transition-colors text-sm text-white placeholder-white/30"
                />
              </div>
            </div>

            {/* Conversations */}
            <div className="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-2">
              {conversations.map((conv) => (
                <button
                  key={conv.id}
                  className={`w-full p-4 rounded-lg text-left transition-all ${
                    conv.active 
                      ? 'bg-white/10 border border-white/20' 
                      : 'bg-white/5 border border-white/10 hover:bg-white/10'
                  }`}
                >
                  <div className="flex items-start justify-between mb-1">
                    <div className="flex items-center space-x-2">
                      <MessageSquare className="w-4 h-4 text-white/60" />
                      <span className="font-medium text-sm">{conv.title}</span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1 text-xs text-white/40">
                    <Clock className="w-3 h-3" />
                    <span>{conv.time}</span>
                  </div>
                </button>
              ))}
            </div>

            {/* User Profile */}
            <div className="p-4 border-t border-white/10">
              <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors cursor-pointer">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="font-medium text-sm">John Doe</div>
                    <div className="text-xs text-white/60">john@example.com</div>
                  </div>
                </div>
                <ChevronDown className="w-4 h-4" />
              </div>
              <div className="mt-3 space-y-1">
                <button 
                  onClick={handleSettingsClick}
                  className="w-full px-3 py-2 text-sm text-left hover:bg-white/10 rounded-lg transition-colors flex items-center space-x-2"
                >
                  <Settings className="w-4 h-4" />
                  <span>Settings</span>
                </button>
                <button 
                  onClick={() => router.push('/')}
                  className="w-full px-3 py-2 text-sm text-left hover:bg-white/10 rounded-lg transition-colors flex items-center space-x-2 text-red-400"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Log Out</span>
                </button>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      {/* Main Chat Area */}
      <div className="relative z-10 flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white/5 border-b border-white/10 backdrop-blur-xl p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {!sidebarOpen && (
                <button
                  onClick={() => setSidebarOpen(true)}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                >
                  <Menu className="w-5 h-5" />
                </button>
              )}
              <div>
                <h1 className="text-lg font-semibold">Idea Validation Session</h1>
                <p className="text-sm text-white/60">Powered by Elastic & Google Cloud</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <button 
                onClick={() => setShowRepoInput(!showRepoInput)}
                className={`px-4 py-2 rounded-lg transition-all text-sm font-medium flex items-center space-x-2 ${
                  repoUrl 
                    ? 'bg-green-500/20 border border-green-500/30 text-green-400' 
                    : 'bg-white/5 border border-white/10 hover:bg-white/10 glass'
                }`}
              >
                <Github className="w-4 h-4" />
                <span>{repoUrl ? 'Repo Connected' : 'Connect Repo'}</span>
              </button>
            </div>
          </div>
        </header>

        {/* Repo Connection Modal */}
        <AnimatePresence>
          {showRepoInput && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="bg-white/5 border-b border-white/10 backdrop-blur-xl p-4"
            >
              <div className="max-w-2xl mx-auto">
                <h3 className="text-sm font-semibold mb-2">Connect GitHub Repository</h3>
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={repoUrl}
                    onChange={(e) => setRepoUrl(e.target.value)}
                    placeholder="https://github.com/username/repo"
                    className="flex-1 px-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-white/30 transition-colors text-white placeholder-white/30"
                  />
                  <button
                    onClick={handleConnectRepo}
                    className="px-6 py-2 bg-white text-black rounded-lg hover:bg-white/90 transition-all font-semibold"
                  >
                    Connect
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Quick Actions */}
        {messages.length === 1 && (
          <div className="p-6 border-b border-white/10">
            <h3 className="text-sm font-semibold mb-4 text-white/80">Quick Actions</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {quickActions.map((action) => (
                <motion.button
                  key={action.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={action.action}
                  className={`p-4 bg-gradient-to-br ${action.color} border border-white/10 rounded-xl hover:border-white/20 transition-all text-left group`}
                >
                  <action.icon className="w-6 h-6 mb-2 text-white group-hover:scale-110 transition-transform" />
                  <h4 className="font-semibold text-sm mb-1">{action.title}</h4>
                  <p className="text-xs text-white/60">{action.description}</p>
                </motion.button>
              ))}
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-6">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-3xl ${message.role === 'user' ? 'order-2' : 'order-1'}`}>
                  <div className={`flex items-start space-x-3 ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                    {/* Avatar */}
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.role === 'user' 
                        ? 'bg-white text-black' 
                        : 'bg-white/10 text-white'
                    }`}>
                      {message.role === 'user' ? (
                        <User className="w-5 h-5" />
                      ) : (
                        <Sparkles className="w-5 h-5" />
                      )}
                    </div>
                    
                    {/* Message Content */}
                    <div className={`flex-1 ${message.role === 'user' ? 'text-right' : ''}`}>
                      <div className={`inline-block p-4 rounded-2xl ${
                        message.role === 'user'
                          ? 'bg-white text-black'
                          : 'bg-white/5 border border-white/10 text-white'
                      }`}>
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                      </div>
                      
                      {/* Sources */}
                      {message.sources && message.sources.length > 0 && (
                        <div className="mt-3 space-y-2">
                          <p className="text-xs font-semibold text-white/60">📚 Sources ({message.sources.length}):</p>
                          {message.sources.map((source, idx) => (
                            <div key={idx} className="bg-white/5 border border-white/10 rounded-lg p-3 text-xs">
                              <div className="flex items-start justify-between">
                                <div className="flex-1">
                                  <div className="font-semibold mb-1">{source.title}</div>
                                  {source.description && (
                                    <p className="text-white/60 mb-2">{source.description}</p>
                                  )}
                                  {source.url && (
                                    <a 
                                      href={source.url} 
                                      target="_blank" 
                                      rel="noopener noreferrer"
                                      className="text-blue-400 hover:text-blue-300 flex items-center space-x-1"
                                    >
                                      <span>View Source</span>
                                      <ExternalLink className="w-3 h-3" />
                                    </a>
                                  )}
                                </div>
                                {source.relevance_score && (
                                  <div className="ml-2 px-2 py-1 bg-white/10 rounded text-xs">
                                    {(source.relevance_score * 100).toFixed(0)}%
                                  </div>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                      
                      <div className="mt-1 text-xs text-white/40">
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing Indicator */}
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="flex items-start space-x-3">
                <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div className="bg-white/5 border border-white/10 p-4 rounded-2xl">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-white/60 rounded-full typing-indicator" style={{ animationDelay: '0s' }} />
                    <div className="w-2 h-2 bg-white/60 rounded-full typing-indicator" style={{ animationDelay: '0.2s' }} />
                    <div className="w-2 h-2 bg-white/60 rounded-full typing-indicator" style={{ animationDelay: '0.4s' }} />
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>

        {/* Suggestions */}
        {currentSuggestions.length > 0 && (
          <div className="px-6 pb-4">
            <div className="flex flex-wrap gap-2">
              {currentSuggestions.map((suggestion, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="px-3 py-2 bg-white/5 border border-white/10 rounded-lg hover:bg-white/10 transition-all text-xs text-white/80 hover:text-white"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="bg-white/5 border-t border-white/10 backdrop-blur-xl p-6">
          <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto">
            <div className="relative">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask me anything about your hackathon project..."
                className="w-full pl-6 pr-14 py-4 bg-white/5 border border-white/10 rounded-2xl focus:outline-none focus:border-white/30 transition-colors text-white placeholder-white/30"
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isTyping}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-3 bg-white text-black rounded-xl hover:bg-white/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed glow-white"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            <div className="mt-3 flex items-center justify-between">
              <p className="text-xs text-white/40">
                Powered by Elastic Hybrid Search & Google Cloud Vertex AI
              </p>
              <div className="flex items-center space-x-2 text-xs text-white/40">
                <CheckCircle className="w-3 h-3 text-green-400" />
                <span>Real-time AI</span>
              </div>
            </div>
          </form>
        </div>
      </div>
      
      {/* Settings Modal */}
      <AnimatePresence>
        {showSettings && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm"
            onClick={() => setShowSettings(false)}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={(e) => e.stopPropagation()}
              className="relative w-full max-w-3xl max-h-[85vh] overflow-hidden bg-black border border-white/10 rounded-2xl shadow-2xl"
            >
              {/* Animated gradient background - same as chat page */}
              <div className="absolute inset-0 animated-gradient opacity-30 pointer-events-none" />
              
              {/* Grid overlay - same as chat page */}
              <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.02)_1px,transparent_1px)] bg-[size:100px_100px] pointer-events-none" />

              {/* Settings Header */}
              <div className="relative z-10 bg-white/5 backdrop-blur-xl border-b border-white/10 p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Settings className="w-6 h-6 text-white" />
                    <h2 className="text-2xl font-bold">Settings</h2>
                  </div>
                  <button
                    onClick={() => setShowSettings(false)}
                    className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                  >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>

              {/* Settings Content */}
              <div className="relative z-10 p-6 space-y-6 overflow-y-auto max-h-[calc(85vh-88px)] custom-scrollbar">
                {/* User Profile Section */}
                <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                  <div className="flex items-center gap-3 mb-4">
                    <User className="w-5 h-5 text-white" />
                    <h3 className="text-lg font-semibold">User Profile</h3>
                  </div>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-white/60 mb-2">Name</label>
                      <input
                        type="text"
                        defaultValue="John Doe"
                        className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-white/30 transition-colors text-white placeholder-white/30"
                        placeholder="Your name"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-white/60 mb-2">Email</label>
                      <input
                        type="email"
                        defaultValue="john@example.com"
                        className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-white/30 transition-colors text-white placeholder-white/30"
                        placeholder="your@email.com"
                      />
                    </div>
                  </div>
                </div>

                {/* GitHub Repository */}
                <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                  <div className="flex items-center gap-3 mb-4">
                    <Github className="w-5 h-5 text-white" />
                    <h3 className="text-lg font-semibold">GitHub Repository</h3>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-white/60 mb-2">Repository URL</label>
                    <input
                      type="text"
                      value={repoUrl}
                      onChange={(e) => setRepoUrl(e.target.value)}
                      className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-white/30 transition-colors text-white placeholder-white/30 font-mono text-sm"
                      placeholder="https://github.com/username/repo"
                    />
                    <p className="text-xs text-white/40 mt-2">For progress tracking and pitch generation</p>
                  </div>
                </div>

                {/* Preferences */}
                <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                  <div className="flex items-center gap-3 mb-4">
                    <Sparkles className="w-5 h-5 text-white" />
                    <h3 className="text-lg font-semibold">Preferences</h3>
                  </div>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-white/60 mb-2">Theme</label>
                      <select className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-white/30 transition-colors text-white">
                        <option value="dark" className="bg-black">Dark</option>
                        <option value="light" className="bg-black">Light</option>
                        <option value="auto" className="bg-black">Auto</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-white/60 mb-2">Search Type</label>
                      <select className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-white/30 transition-colors text-white">
                        <option value="hybrid" className="bg-black">Hybrid (BM25 + Vector)</option>
                        <option value="semantic" className="bg-black">Semantic Only</option>
                        <option value="keyword" className="bg-black">Keyword Only</option>
                      </select>
                    </div>
                  </div>
                  <div className="mt-4 space-y-3">
                    <label className="flex items-center gap-3 cursor-pointer group">
                      <input
                        type="checkbox"
                        defaultChecked
                        className="w-4 h-4 rounded border-white/20 bg-white/5 text-white focus:ring-white focus:ring-offset-0"
                      />
                      <span className="text-sm text-white/60 group-hover:text-white/80 transition-colors">Enable notifications</span>
                    </label>
                    <label className="flex items-center gap-3 cursor-pointer group">
                      <input
                        type="checkbox"
                        defaultChecked
                        className="w-4 h-4 rounded border-white/20 bg-white/5 text-white focus:ring-white focus:ring-offset-0"
                      />
                      <span className="text-sm text-white/60 group-hover:text-white/80 transition-colors">Auto-save conversations</span>
                    </label>
                  </div>
                </div>

                {/* Save Button */}
                <div className="flex justify-end gap-3 pt-2">
                  <button
                    onClick={() => setShowSettings(false)}
                    className="px-6 py-2.5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg transition-colors text-white"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() => {
                      toast.success('Settings saved!')
                      setShowSettings(false)
                    }}
                    className="px-6 py-2.5 bg-white text-black rounded-lg hover:bg-white/90 transition-all glow-white font-semibold"
                  >
                    Save Changes
                  </button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Toast Container */}
      <Toaster 
        position="top-right"
        toastOptions={{
          style: {
            background: 'rgba(255, 255, 255, 0.1)',
            color: '#fff',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
          },
        }}
      />
    </div>
  )
}
