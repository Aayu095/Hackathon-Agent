/**
 * API Client for Hackathon Agent Backend
 * Handles all communication with FastAPI backend
 */

import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

// Debug log
console.log('🔧 API Base URL:', API_BASE_URL)
console.log('🔧 Environment:', process.env.NEXT_PUBLIC_API_URL)

class APIClient {
  private client: AxiosInstance

  constructor() {
    console.log('🔧 Creating API client with baseURL:', API_BASE_URL)
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error.response?.data || error.message)
        throw error
      }
    )
  }

  // Health Check
  async healthCheck() {
    const response = await this.client.get('/health')
    return response.data
  }

  // Chat Endpoints
  async sendMessage(data: {
    message: string
    conversation_history?: Array<{ role: string; content: string; timestamp?: string }>
    repo_url?: string
    context_type?: string
  }) {
    const response = await this.client.post('/chat/', data)
    return response.data
  }

  async validateIdea(idea: string, conversation_history?: any[]) {
    const response = await this.client.post('/chat/validate-idea', {
      message: idea,
      conversation_history: conversation_history || [],
    })
    return response.data
  }

  async getProgressReport(repo_url: string, conversation_history?: any[]) {
    const response = await this.client.post('/chat/progress-report', {
      message: 'Generate a progress report for our project',
      repo_url,
      conversation_history: conversation_history || [],
    })
    return response.data
  }

  // Search Endpoints
  async search(data: {
    query: string
    search_type?: 'hybrid' | 'semantic' | 'keyword'
    index?: string
    size?: number
  }) {
    const response = await this.client.post('/search/', {
      query: data.query,
      search_type: data.search_type || 'hybrid',
      index: data.index,
      size: data.size || 10,
    })
    return response.data
  }

  async searchDevpost(query: string, size: number = 10, searchType: string = 'hybrid') {
    const response = await this.client.get('/search/devpost', {
      params: { q: query, size, search_type: searchType },
    })
    return response.data
  }

  async searchDocumentation(query: string, size: number = 5, searchType: string = 'hybrid') {
    const response = await this.client.get('/search/documentation', {
      params: { q: query, size, search_type: searchType },
    })
    return response.data
  }

  async getSearchSuggestions(query: string, limit: number = 5) {
    const response = await this.client.get('/search/suggestions', {
      params: { q: query, limit },
    })
    return response.data
  }

  // GitHub Endpoints
  async analyzeRepository(repo_url: string) {
    const response = await this.client.post('/github/analyze', { repo_url })
    return response.data
  }

  async getRepositoryActivity(repo_url: string, days: number = 7) {
    const response = await this.client.get('/github/activity', {
      params: { repo_url, days },
    })
    return response.data
  }

  async generatePitchDeck(repo_url: string) {
    const response = await this.client.post('/github/generate-pitch', { repo_url })
    return response.data
  }

  async generateReadme(repo_url: string) {
    const response = await this.client.post('/github/generate-readme', { repo_url })
    return response.data
  }
}

// Export singleton instance
export const apiClient = new APIClient()

// Export types
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

export interface ChatResponse {
  response: string
  sources?: Array<{
    type: string
    title: string
    description?: string
    url?: string
    relevance_score?: number
    [key: string]: any
  }>
  suggestions?: string[]
  conversation_id?: string
}

export interface SearchResult {
  title: string
  description: string
  url?: string
  score: number
  source: string
  metadata?: Record<string, any>
}

export interface SearchResponse {
  results: SearchResult[]
  total: number
  query: string
  search_type: string
  took_ms?: number
}
