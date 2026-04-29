import React from 'react'
import { ArrowLeft, Filter, SortAsc, Copy } from 'lucide-react'
import Button from '@/components/ui/Button'
import RestaurantCard from './RestaurantCard'
import { Recommendation } from '@/lib/api'
import LoadingSpinner from '@/components/ui/LoadingSpinner'

interface RestaurantListProps {
  recommendations: Recommendation[]
  loading?: boolean
  error?: string
  onBack?: () => void
  onRetry?: () => void
  onViewDetails?: (restaurant: Recommendation['restaurant']) => void
}

export default function RestaurantList({
  recommendations,
  loading = false,
  error,
  onBack,
  onRetry,
  onViewDetails
}: RestaurantListProps) {
  const [sortBy, setSortBy] = React.useState<'rank' | 'rating' | 'name'>('rank')
  const [filterBy, setFilterBy] = React.useState<'all' | 'high-rated' | 'budget-friendly'>('all')

  const sortedAndFilteredRecommendations = React.useMemo(() => {
    let filtered = [...recommendations]

    // Apply filters
    switch (filterBy) {
      case 'high-rated':
        filtered = filtered.filter(rec => rec.restaurant.rating && rec.restaurant.rating >= 4.0)
        break
      case 'budget-friendly':
        filtered = filtered.filter(rec => rec.restaurant.budgetBand === 'low' || rec.restaurant.budgetBand === 'medium')
        break
    }

    // Apply sorting
    switch (sortBy) {
      case 'rank':
        filtered.sort((a, b) => a.rank - b.rank)
        break
      case 'rating':
        filtered.sort((a, b) => (b.restaurant.rating || 0) - (a.restaurant.rating || 0))
        break
      case 'name':
        filtered.sort((a, b) => a.restaurant.name.localeCompare(b.restaurant.name))
        break
    }

    return filtered
  }, [recommendations, sortBy, filterBy])

  const handleCopyAsMarkdown = () => {
    const markdown = sortedAndFilteredRecommendations.map(rec => {
      const restaurant = rec.restaurant
      return `## ${rec.rank}. ${restaurant.name}

**Location:** ${restaurant.location}
**Cuisines:** ${restaurant.cuisines.join(', ')}
**Rating:** ${restaurant.rating ? `${restaurant.rating} ⭐` : 'Not rated'}
**Cost:** ${restaurant.cost ? `Rs.${restaurant.cost}` : 'Price not available'}
**Budget Band:** ${restaurant.budgetBand || 'Not specified'}

**AI Explanation:** ${rec.explanation}
---
`
    }).join('\n')

    navigator.clipboard.writeText(markdown)
      .then(() => {
        // Could show a toast notification here
        console.log('Copied to clipboard')
      })
      .catch(err => {
        console.error('Failed to copy:', err)
      })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <LoadingSpinner size="lg" />
          <p className="mt-4 text-gray-600">Finding the perfect restaurants for you...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center p-8">
          <div className="text-red-600 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Oops! Something went wrong
          </h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <div className="space-x-4">
            <Button onClick={onRetry} variant="primary">
              Try Again
            </Button>
            <Button onClick={onBack} variant="outline">
              Go Back
            </Button>
          </div>
        </div>
      </div>
    )
  }

  if (recommendations.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center p-8">
          <div className="text-gray-400 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            No restaurants found
          </h2>
          <p className="text-gray-600 mb-6">
            We couldn't find any restaurants matching your preferences. Try adjusting your filters.
          </p>
          <Button onClick={onBack} variant="primary">
            Go Back and Try Again
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-4">
              {onBack && (
                <Button variant="ghost" onClick={onBack}>
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back
                </Button>
              )}
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  🍽️ Restaurant Recommendations
                </h1>
                <p className="text-gray-600 mt-1">
                  {sortedAndFilteredRecommendations.length} restaurants found
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button variant="outline" onClick={handleCopyAsMarkdown} size="sm">
                <Copy className="w-4 h-4 mr-2" />
                Copy as Markdown
              </Button>
            </div>
          </div>

          {/* Filters and Sort */}
          <div className="flex flex-wrap items-center gap-4 p-4 bg-white rounded-lg shadow-sm">
            <div className="flex items-center space-x-2">
              <Filter className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700">Filter:</span>
              <select
                value={filterBy}
                onChange={(e) => setFilterBy(e.target.value as any)}
                className="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Restaurants</option>
                <option value="high-rated">High Rated (4.0+)</option>
                <option value="budget-friendly">Budget Friendly</option>
              </select>
            </div>

            <div className="flex items-center space-x-2">
              <SortAsc className="w-4 h-4 text-gray-500" />
              <span className="text-sm font-medium text-gray-700">Sort:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="rank">Rank</option>
                <option value="rating">Rating</option>
                <option value="name">Name</option>
              </select>
            </div>
          </div>
        </div>

        {/* Restaurant Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sortedAndFilteredRecommendations.map((recommendation) => (
            <RestaurantCard
              key={recommendation.restaurant.id}
              recommendation={recommendation}
              onViewDetails={onViewDetails}
            />
          ))}
        </div>

        {/* Empty State for Filtered Results */}
        {sortedAndFilteredRecommendations.length === 0 && recommendations.length > 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <Filter className="w-16 h-16 mx-auto" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              No restaurants match your filters
            </h3>
            <p className="text-gray-600 mb-4">
              Try adjusting your filter criteria to see more results.
            </p>
            <Button
              variant="outline"
              onClick={() => setFilterBy('all')}
            >
              Clear Filters
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}
