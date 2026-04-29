// API integration for Phase 6 backend

export interface UserPreferences {
  location: string
  budgetBand?: string
  cuisines?: string[]
  minRating?: number
  additionalPreferences?: string
}

export interface Restaurant {
  id: string
  name: string
  location: string
  cuisines: string[]
  rating?: number
  cost?: number
  budgetBand?: string
}

export interface Recommendation {
  restaurant: Restaurant
  rank: number
  explanation: string
}

export interface ApiResponse<T> {
  data?: T
  error?: string
  success: boolean
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message)
    this.name = 'ApiError'
  }
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new ApiError(
        errorData.error || `HTTP ${response.status}: ${response.statusText}`,
        response.status
      )
    }

    const data = await response.json()
    return {
      success: true,
      data,
    }
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error occurred',
    }
  }
}

export const api = {
  // Submit preferences and get recommendations
  async getRecommendations(preferences: UserPreferences): Promise<Recommendation[]> {
    const response = await apiRequest<Recommendation[]>('/recommendations', {
      method: 'POST',
      body: JSON.stringify(preferences),
    })

    if (!response.success || !response.data) {
      throw new ApiError(response.error || 'Failed to get recommendations')
    }

    return response.data
  },

  // Get available locations
  async getLocations(): Promise<string[]> {
    const response = await apiRequest<string[]>('/locations')
    
    if (!response.success || !response.data) {
      throw new ApiError(response.error || 'Failed to get locations')
    }

    return response.data
  },

  // Get restaurant details
  async getRestaurant(id: string): Promise<Restaurant> {
    const response = await apiRequest<Restaurant>(`/restaurants/${id}`)
    
    if (!response.success || !response.data) {
      throw new ApiError(response.error || 'Failed to get restaurant details')
    }

    return response.data
  },

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string }> {
    const response = await apiRequest<{ status: string; timestamp: string }>('/health')
    
    if (!response.success || !response.data) {
      throw new ApiError(response.error || 'Health check failed')
    }

    return response.data
  },
}

export { ApiError }
