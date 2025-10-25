'use client'

import { X, Plus, Github, Settings, HelpCircle, Bot } from 'lucide-react'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
  onNewChat: () => void
  repoUrl: string
  onRepoChange: (url: string) => void
}

export function Sidebar({ isOpen, onClose, onNewChat, repoUrl, onRepoChange }: SidebarProps) {
  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed lg:relative inset-y-0 left-0 z-50 w-80 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 transform transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-2">
              <Bot className="w-6 h-6 text-blue-600" />
              <h2 className="font-semibold text-gray-900 dark:text-white">Hackathon Agent</h2>
            </div>
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded lg:hidden"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>

          {/* New Chat Button */}
          <div className="p-4">
            <button
              onClick={onNewChat}
              className="w-full flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
            >
              <Plus className="w-4 h-4" />
              New Chat
            </button>
          </div>

          {/* Repository Section */}
          <div className="px-4 pb-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              GitHub Repository
            </label>
            <input
              type="url"
              value={repoUrl}
              onChange={(e) => onRepoChange(e.target.value)}
              placeholder="https://github.com/username/repo"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Connect your repository for progress tracking
            </p>
          </div>

          {/* Features */}
          <div className="flex-1 px-4 space-y-2">
            <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Features</h3>
            
            <div className="space-y-1">
              <div className="flex items-center gap-3 p-2 text-sm text-gray-600 dark:text-gray-400">
                <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                Idea Validation
              </div>
              <div className="flex items-center gap-3 p-2 text-sm text-gray-600 dark:text-gray-400">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                Documentation Search
              </div>
              <div className="flex items-center gap-3 p-2 text-sm text-gray-600 dark:text-gray-400">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                Progress Tracking
              </div>
              <div className="flex items-center gap-3 p-2 text-sm text-gray-600 dark:text-gray-400">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                Presentation Help
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700 space-y-2">
            <button className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors">
              <Settings className="w-4 h-4" />
              Settings
            </button>
            <button className="w-full flex items-center gap-2 px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors">
              <HelpCircle className="w-4 h-4" />
              Help & Support
            </button>
            <div className="text-xs text-gray-500 dark:text-gray-400 text-center pt-2">
              v1.0.0 • Built for AI Accelerate
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
