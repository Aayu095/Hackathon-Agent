'use client'

import { useState } from 'react'
import { Bot, Lightbulb, GitBranch, Presentation, ArrowRight, Github } from 'lucide-react'

interface WelcomeScreenProps {
  onStartChat: (repoUrl?: string) => void
}

export function WelcomeScreen({ onStartChat }: WelcomeScreenProps) {
  const [repoUrl, setRepoUrl] = useState('')

  const features = [
    {
      icon: <Lightbulb className="w-8 h-8 text-yellow-500" />,
      title: "Idea Validation",
      description: "Search 10,000+ past Devpost projects to validate your idea's originality and identify potential improvements."
    },
    {
      icon: <Bot className="w-8 h-8 text-blue-500" />,
      title: "Contextual RAG",
      description: "Get instant answers from hackathon rules, partner documentation, and best practices using advanced AI."
    },
    {
      icon: <GitBranch className="w-8 h-8 text-green-500" />,
      title: "Progress Tracking",
      description: "Real-time GitHub monitoring with intelligent summaries of your team's development progress."
    },
    {
      icon: <Presentation className="w-8 h-8 text-purple-500" />,
      title: "Presentation Assistant",
      description: "Auto-generate pitch decks and demo scripts based on your project's commit history and documentation."
    }
  ]

  const handleStartWithRepo = () => {
    onStartChat(repoUrl)
  }

  const handleStartWithoutRepo = () => {
    onStartChat()
  }

  return (
    <div className="flex-1 overflow-auto custom-scrollbar">
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mb-6">
            <Bot className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold gradient-text mb-4">
            🤖 Hackathon Agent
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Your AI-powered mentor that transforms how hackathon teams approach ideation, 
            development, and presentation. Built with Google Cloud AI and Elastic's hybrid search.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {features.map((feature, index) => (
            <div 
              key={index}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-200 dark:border-gray-700"
            >
              <div className="mb-4">{feature.icon}</div>
              <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Getting Started */}
        <div className="bg-white dark:bg-gray-800 rounded-xl p-8 shadow-lg border border-gray-200 dark:border-gray-700">
          <h2 className="text-2xl font-bold mb-6 text-center text-gray-900 dark:text-white">
            🚀 Get Started
          </h2>
          
          <div className="space-y-6">
            {/* Option 1: With GitHub Repository */}
            <div className="border border-gray-200 dark:border-gray-600 rounded-lg p-6">
              <div className="flex items-center mb-4">
                <Github className="w-5 h-5 text-gray-600 dark:text-gray-400 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Connect Your GitHub Repository
                </h3>
              </div>
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Link your hackathon project repository to enable progress tracking and automated insights.
              </p>
              <div className="flex gap-3">
                <input
                  type="url"
                  placeholder="https://github.com/username/repository"
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                />
                <button
                  onClick={handleStartWithRepo}
                  disabled={!repoUrl.trim()}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg font-medium transition-colors duration-200 flex items-center gap-2"
                >
                  Start <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Option 2: Without Repository */}
            <div className="text-center">
              <p className="text-gray-600 dark:text-gray-300 mb-4">
                Or start exploring without a repository
              </p>
              <button
                onClick={handleStartWithoutRepo}
                className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-lg font-medium transition-all duration-200 flex items-center gap-2 mx-auto"
              >
                <Bot className="w-5 h-5" />
                Start Chatting
              </button>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">10K+</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Devpost Projects</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 dark:text-green-400">&lt;2s</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Response Time</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600 dark:text-purple-400">40%</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Higher Success Rate</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">24/7</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">AI Assistance</div>
          </div>
        </div>
      </div>
    </div>
  )
}
