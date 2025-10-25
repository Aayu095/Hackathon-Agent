'use client'

import { useState, useEffect } from 'react'
import { Settings as SettingsIcon, Save, User, Bell, Palette, Database, Github, Key } from 'lucide-react'

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    // User Settings
    userName: 'John Doe',
    userEmail: 'john@example.com',
    
    // API Settings
    elasticCloudId: '',
    elasticApiKey: '',
    githubToken: '',
    
    // Preferences
    theme: 'dark',
    notifications: true,
    autoSave: true,
    searchType: 'hybrid',
    
    // Display
    fontSize: 'medium',
    language: 'en',
  })

  const [saved, setSaved] = useState(false)

  useEffect(() => {
    // Load settings from localStorage
    const savedSettings = localStorage.getItem('hackathon-agent-settings')
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings))
    }
  }, [])

  const handleSave = () => {
    // Save to localStorage
    localStorage.setItem('hackathon-agent-settings', JSON.stringify(settings))
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  const handleChange = (key: string, value: any) => {
    setSettings(prev => ({ ...prev, [key]: value }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
      {/* Header */}
      <div className="border-b border-gray-800 bg-black/20 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center gap-3">
            <SettingsIcon className="w-8 h-8 text-purple-400" />
            <div>
              <h1 className="text-3xl font-bold">Settings</h1>
              <p className="text-gray-400 text-sm">Customize your Hackathon Agent experience</p>
            </div>
          </div>
        </div>
      </div>

      {/* Settings Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid gap-6">
          
          {/* User Profile Section */}
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <div className="flex items-center gap-3 mb-6">
              <User className="w-6 h-6 text-purple-400" />
              <h2 className="text-xl font-semibold">User Profile</h2>
            </div>
            
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Name</label>
                <input
                  type="text"
                  value={settings.userName}
                  onChange={(e) => handleChange('userName', e.target.value)}
                  className="w-full px-4 py-2 bg-gray-900/50 border border-gray-600 rounded-lg focus:outline-none focus:border-purple-500 transition-colors"
                  placeholder="Your name"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
                <input
                  type="email"
                  value={settings.userEmail}
                  onChange={(e) => handleChange('userEmail', e.target.value)}
                  className="w-full px-4 py-2 bg-gray-900/50 border border-gray-600 rounded-lg focus:outline-none focus:border-purple-500 transition-colors"
                  placeholder="your@email.com"
                />
              </div>
            </div>
          </div>

          {/* API Configuration Section */}
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <div className="flex items-center gap-3 mb-6">
              <Key className="w-6 h-6 text-purple-400" />
              <h2 className="text-xl font-semibold">API Configuration</h2>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Database className="w-4 h-4 inline mr-2" />
                  Elastic Cloud ID
                </label>
                <input
                  type="text"
                  value={settings.elasticCloudId}
                  onChange={(e) => handleChange('elasticCloudId', e.target.value)}
                  className="w-full px-4 py-2 bg-gray-900/50 border border-gray-600 rounded-lg focus:outline-none focus:border-purple-500 transition-colors font-mono text-sm"
                  placeholder="deployment-name:base64string..."
                />
                <p className="text-xs text-gray-400 mt-1">Get this from your Elastic Cloud deployment page</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Key className="w-4 h-4 inline mr-2" />
                  Elastic API Key
                </label>
                <input
                  type="password"
                  value={settings.elasticApiKey}
                  onChange={(e) => handleChange('elasticApiKey', e.target.value)}
                  className="w-full px-4 py-2 bg-gray-900/50 border border-gray-600 rounded-lg focus:outline-none focus:border-purple-500 transition-colors font-mono text-sm"
                  placeholder="Your Elastic API key..."
                />
                <p className="text-xs text-gray-400 mt-1">Create in Kibana → Stack Management → Security → API Keys</p>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Github className="w-4 h-4 inline mr-2" />
                  GitHub Personal Access Token
                </label>
                <input
                  type="password"
                  value={settings.githubToken}
                  onChange={(e) => handleChange('githubToken', e.target.value)}
                  className="w-full px-4 py-2 bg-gray-900/50 border border-gray-600 rounded-lg focus:outline-none focus:border-purple-500 transition-colors font-mono text-sm"
                  placeholder="ghp_..."
                />
                <p className="text-xs text-gray-400 mt-1">For repository analysis and progress tracking</p>
              </div>
            </div>
          </div>

          {/* Preferences Section */}
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 border border-gray-700">
            <div className="flex items-center gap-3 mb-6">
              <Palette className="w-6 h-6 text-purple-400" />
              <h2 className="text-xl font-semibold">Preferences</h2>
            </div>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Theme</label>
                <select
                  value={settings.theme}
                  onChange={(e) => handleChange('theme', e.target.value)}
                  className="w-full px-4 py-2 bg-gray-900/50 border border-gray-600 rounded-lg focus:outline-none focus:border-purple-500 transition-colors"
                >
                  <option value="dark">Dark</option>
                  <option value="light">Light</option>
                  <option value="auto">Auto</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Search Type</label>
                <select
                  value={settings.searchType}
                  onChange={(e) => handleChange('searchType', e.target.value)}
                  className="w-full px-4 py-2 bg-gray-900/50 border border-gray-600 rounded-lg focus:outline-none focus:border-purple-500 transition-colors"
                >
                  <option value="hybrid">Hybrid (BM25 + Vector)</option>
                  <option value="semantic">Semantic Only</option>
                  <option value="keyword">Keyword Only</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Font Size</label>
                <select
                  value={settings.fontSize}
                  onChange={(e) => handleChange('fontSize', e.target.value)}
                  className="w-full px-4 py-2 bg-gray-900/50 border border-gray-600 rounded-lg focus:outline-none focus:border-purple-500 transition-colors"
                >
                  <option value="small">Small</option>
                  <option value="medium">Medium</option>
                  <option value="large">Large</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Language</label>
                <select
                  value={settings.language}
                  onChange={(e) => handleChange('language', e.target.value)}
                  className="w-full px-4 py-2 bg-gray-900/50 border border-gray-600 rounded-lg focus:outline-none focus:border-purple-500 transition-colors"
                >
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                </select>
              </div>
            </div>
            
            <div className="mt-6 space-y-3">
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.notifications}
                  onChange={(e) => handleChange('notifications', e.target.checked)}
                  className="w-5 h-5 rounded border-gray-600 bg-gray-900/50 text-purple-500 focus:ring-purple-500 focus:ring-offset-0"
                />
                <span className="text-sm">Enable notifications</span>
              </label>
              
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.autoSave}
                  onChange={(e) => handleChange('autoSave', e.target.checked)}
                  className="w-5 h-5 rounded border-gray-600 bg-gray-900/50 text-purple-500 focus:ring-purple-500 focus:ring-offset-0"
                />
                <span className="text-sm">Auto-save conversations</span>
              </label>
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end gap-4">
            <button
              onClick={() => window.history.back()}
              className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-medium transition-colors"
            >
              Cancel
            </button>
            
            <button
              onClick={handleSave}
              className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 rounded-lg font-medium transition-all flex items-center gap-2 shadow-lg shadow-purple-500/50"
            >
              <Save className="w-5 h-5" />
              {saved ? 'Saved!' : 'Save Settings'}
            </button>
          </div>

          {saved && (
            <div className="bg-green-500/20 border border-green-500 rounded-lg p-4 text-center">
              <p className="text-green-400 font-medium">✓ Settings saved successfully!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
