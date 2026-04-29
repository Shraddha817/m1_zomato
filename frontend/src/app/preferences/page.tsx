'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

interface UserPreferences {
  location: string
  budgetBand?: string
  cuisines?: string[]
  minRating?: number
  additionalPreferences?: string
}

export default function PreferencesPage() {
  const router = useRouter()
  const [preferences, setPreferences] = useState<UserPreferences>({
    location: '',
    budgetBand: '',
    cuisines: [],
    minRating: 3.0,
    additionalPreferences: ''
  })
  
  const [isLoading, setIsLoading] = useState(false)
  const [cuisineInput, setCuisineInput] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    
    try {
      // Make actual API call to backend
      const response = await fetch('http://localhost:8000/api/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          location: preferences.location,
          budgetBand: preferences.budgetBand || undefined,
          cuisines: preferences.cuisines || undefined,
          minRating: preferences.minRating || undefined,
          additionalPreferences: preferences.additionalPreferences || undefined
        })
      })
      
      if (!response.ok) {
        throw new Error(`API call failed: ${response.status}`)
      }
      
      const recommendations = await response.json()
      
      // Store recommendations in sessionStorage for results page
      sessionStorage.setItem('recommendations', JSON.stringify(recommendations))
      sessionStorage.setItem('preferences', JSON.stringify(preferences))
      
      // Navigate to results
      router.push('/results')
    } catch (error) {
      console.error('Error submitting preferences:', error)
      alert('Failed to get recommendations. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCuisineAdd = () => {
    if (cuisineInput.trim() && !preferences.cuisines?.includes(cuisineInput.trim())) {
      setPreferences(prev => ({
        ...prev,
        cuisines: [...(prev.cuisines || []), cuisineInput.trim()]
      }))
      setCuisineInput('')
    }
  }

  const handleCuisineRemove = (cuisineToRemove: string) => {
    setPreferences(prev => ({
      ...prev,
      cuisines: prev.cuisines?.filter(c => c !== cuisineToRemove) || []
    }))
  }

  const budgetBands = [
    { value: 'low', label: 'Low (≤ Rs.300)', color: 'bg-green-100 text-green-800' },
    { value: 'medium', label: 'Medium (Rs.301-700)', color: 'bg-yellow-100 text-yellow-800' },
    { value: 'high', label: 'High (> Rs.700)', color: 'bg-red-100 text-red-800' }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="mb-8">
            <button
              onClick={() => router.push('/')}
              className="text-blue-600 hover:text-blue-800 mb-4"
            >
              ← Back to Home
            </button>
            
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              🍽️ Tell us your preferences
            </h1>
            <p className="text-gray-600 mb-8">
              Help us find the perfect restaurants for you by providing your preferences below.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Location Input */}
            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
                Location *
              </label>
              <input
                type="text"
                id="location"
                value={preferences.location}
                onChange={(e) => setPreferences(prev => ({ ...prev, location: e.target.value }))}
                placeholder="e.g., Banashankari, BTM, JP Nagar"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            {/* Budget Band Selection */}
            <div>
              <label htmlFor="budgetBand" className="block text-sm font-medium text-gray-700 mb-2">
                Budget Band
              </label>
              <select
                id="budgetBand"
                value={preferences.budgetBand}
                onChange={(e) => setPreferences(prev => ({ ...prev, budgetBand: e.target.value }))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">No preference</option>
                {budgetBands.map(band => (
                  <option key={band.value} value={band.value}>
                    {band.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Rating Slider */}
              <div>
                <label htmlFor="minRating" className="block text-sm font-medium text-gray-700 mb-2">
                  Minimum Rating
                </label>
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-gray-500">1.0</span>
                  <input
                    type="range"
                    id="minRating"
                    min="1"
                    max="5"
                    step="0.5"
                    value={preferences.minRating}
                    onChange={(e) => setPreferences(prev => ({ ...prev, minRating: parseFloat(e.target.value) }))}
                    className="flex-1"
                  />
                  <span className="text-sm text-gray-500">5.0</span>
                  <span className="text-sm font-medium text-gray-700 ml-2">
                    {preferences.minRating?.toFixed(1)}
                  </span>
                </div>
              </div>

              {/* Cuisine Input */}
              <div>
                <label htmlFor="cuisines" className="block text-sm font-medium text-gray-700 mb-2">
                  Cuisines
                </label>
                <div className="space-y-2">
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      id="cuisines"
                      value={cuisineInput}
                      onChange={(e) => setCuisineInput(e.target.value)}
                      placeholder="e.g., North Indian, Chinese, Italian"
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    />
                    <button
                      type="button"
                      onClick={handleCuisineAdd}
                      className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      Add
                    </button>
                  </div>
                  
                  {/* Cuisine Tags */}
                  {preferences.cuisines && preferences.cuisines.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-2">
                      {preferences.cuisines.map(cuisine => (
                        <span
                          key={cuisine}
                          className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800"
                        >
                          {cuisine}
                          <button
                            type="button"
                            onClick={() => handleCuisineRemove(cuisine)}
                            className="ml-2 text-blue-600 hover:text-blue-800"
                          >
                            ×
                          </button>
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Additional Preferences */}
            <div>
              <label htmlFor="additionalPreferences" className="block text-sm font-medium text-gray-700 mb-2">
                Additional Preferences (optional)
              </label>
              <textarea
                id="additionalPreferences"
                value={preferences.additionalPreferences}
                onChange={(e) => setPreferences(prev => ({ ...prev, additionalPreferences: e.target.value }))}
                rows={4}
                placeholder="Any specific requirements or preferences..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Submit Button */}
            <div className="pt-6">
              <button
                type="submit"
                disabled={isLoading || !preferences.location.trim()}
                className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white border-t-transparent border-r-transparent border-l-transparent mr-2"></div>
                    Getting Recommendations...
                  </div>
                ) : (
                  'Get Recommendations'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
