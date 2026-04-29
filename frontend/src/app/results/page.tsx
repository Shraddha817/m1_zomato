'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'

interface Restaurant {
  id: string
  name: string
  location: string
  cuisines: string[]
  rating: number | null
  cost: number | null
  budgetBand: string | null
}

interface Recommendation {
  restaurant: Restaurant
  rank: number
  explanation: string
}

interface UserPreferences {
  location: string
  budgetBand?: string
  cuisines?: string[]
  minRating?: number
  additionalPreferences?: string
}

export default function ResultsPage() {
  const router = useRouter()
  const [recommendations, setRecommendations] = useState<Recommendation[]>([])
  const [preferences, setPreferences] = useState<UserPreferences | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Load data from sessionStorage
    const storedRecommendations = sessionStorage.getItem('recommendations')
    const storedPreferences = sessionStorage.getItem('preferences')

    if (storedRecommendations) {
      try {
        setRecommendations(JSON.parse(storedRecommendations))
      } catch (error) {
        console.error('Error parsing recommendations:', error)
      }
    }

    if (storedPreferences) {
      try {
        setPreferences(JSON.parse(storedPreferences))
      } catch (error) {
        console.error('Error parsing preferences:', error)
      }
    }

    setIsLoading(false)
  }, [])

  const handleBackToPreferences = () => {
    router.push('/preferences')
  }

  const handleNewSearch = () => {
    router.push('/')
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
    }).format(amount)
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading recommendations...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <button
              onClick={handleBackToPreferences}
              className="text-blue-600 hover:text-blue-800 mb-4"
            >
              × Back to Preferences
            </button>
            
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Your Restaurant Recommendations
            </h1>
            {preferences && (
              <p className="text-gray-600">
                Based on your preferences for {preferences.location}
                {preferences.budgetBand && ` (${preferences.budgetBand} budget)`}
                {preferences.cuisines && preferences.cuisines.length > 0 && 
                  `, ${preferences.cuisines.join(', ')} cuisines`
                }
              </p>
            )}
          </div>

          {/* Recommendations */}
          {recommendations.length > 0 ? (
            <div className="space-y-6">
              {recommendations.map((rec) => (
                <div key={rec.rank} className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <span className="bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded-full mr-3">
                          #{rec.rank}
                        </span>
                        <h3 className="text-xl font-semibold text-gray-900">
                          {rec.restaurant.name}
                        </h3>
                      </div>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                        <div className="space-y-2">
                          <p className="text-gray-600">
                            <span className="font-medium">Location:</span> {rec.restaurant.location}
                          </p>
                          <p className="text-gray-600">
                            <span className="font-medium">Cuisines:</span> {rec.restaurant.cuisines.join(', ')}
                          </p>
                          {rec.restaurant.cost && (
                            <p className="text-gray-600">
                              <span className="font-medium">Cost:</span> {formatCurrency(rec.restaurant.cost)}
                            </p>
                          )}
                        </div>
                        <div className="space-y-2">
                          {rec.restaurant.rating && (
                            <p className="text-gray-600">
                              <span className="font-medium">Rating:</span> 
                              <span className="ml-2 flex items-center">
                                {'\u2605'.repeat(Math.floor(rec.restaurant.rating))}
                                {'\u2606'.repeat(5 - Math.floor(rec.restaurant.rating))}
                                <span className="ml-1">{rec.restaurant.rating.toFixed(1)}</span>
                              </span>
                            </p>
                          )}
                          {rec.restaurant.budgetBand && (
                            <p className="text-gray-600">
                              <span className="font-medium">Budget:</span> 
                              <span className={`ml-2 px-2 py-1 rounded text-sm font-medium ${
                                rec.restaurant.budgetBand === 'low' ? 'bg-green-100 text-green-800' :
                                rec.restaurant.budgetBand === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-red-100 text-red-800'
                              }`}>
                                {rec.restaurant.budgetBand}
                              </span>
                            </p>
                          )}
                        </div>
                      </div>
                      
                      {rec.explanation && (
                        <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                          <p className="text-sm text-blue-800">
                            <span className="font-medium">Why we recommend this:</span> {rec.explanation}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                No restaurants found
              </h3>
              <p className="text-gray-600 mb-6">
                We couldn't find any restaurants matching your criteria. Try adjusting your preferences.
              </p>
              <div className="space-x-4">
                <button
                  onClick={handleBackToPreferences}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Adjust Preferences
                </button>
                <button
                  onClick={handleNewSearch}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  New Search
                </button>
              </div>
            </div>
          )}

          {/* Footer Actions */}
          {recommendations.length > 0 && (
            <div className="mt-8 pt-6 border-t border-gray-200">
              <div className="flex justify-center space-x-4">
                <button
                  onClick={handleBackToPreferences}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Try Different Preferences
                </button>
                <button
                  onClick={handleNewSearch}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  New Search
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
