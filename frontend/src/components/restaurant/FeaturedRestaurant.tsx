import React from 'react'
import { Star, MapPin, Clock, TrendingUp } from 'lucide-react'
import Card, { CardContent } from '@/components/ui/Card'
import Button from '@/components/ui/Button'

interface FeaturedRestaurantProps {
  restaurant: {
    id: string
    name: string
    location: string
    cuisines: string[]
    rating?: number
    cost?: number
    budgetBand?: string
    trending?: boolean
    estimatedTime?: string
  }
  onViewDetails?: (id: string) => void
}

export default function FeaturedRestaurant({ restaurant, onViewDetails }: FeaturedRestaurantProps) {
  const renderStars = (rating?: number) => {
    if (!rating) return null

    return (
      <div className="flex items-center">
        {[...Array(5)].map((_, i) => (
          <Star
            key={i}
            className={`w-4 h-4 ${
              i < Math.floor(rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'
            }`}
          />
        ))}
        <span className="ml-1 text-sm text-gray-600">{rating.toFixed(1)}</span>
      </div>
    )
  }

  const getBudgetColor = (budgetBand?: string) => {
    switch (budgetBand) {
      case 'low': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'high': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <Card variant="elevated" className="hover:shadow-xl transition-all duration-300 hover:scale-105">
      <CardContent>
        <div className="relative">
          {/* Trending Badge */}
          {restaurant.trending && (
            <div className="absolute top-2 right-2 z-10">
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                <TrendingUp className="w-3 h-3 mr-1" />
                Trending
              </span>
            </div>
          )}

          <div className="flex justify-between items-start mb-4">
            <div className="flex-1">
              <h3 className="text-xl font-bold text-gray-900 mb-2">{restaurant.name}</h3>
              
              <div className="flex items-center text-gray-600 mb-3">
                <MapPin className="w-4 h-4 mr-1" />
                <span className="text-sm">{restaurant.location}</span>
                {restaurant.estimatedTime && (
                  <>
                    <Clock className="w-4 h-4 ml-3 mr-1" />
                    <span className="text-sm">{restaurant.estimatedTime}</span>
                  </>
                )}
              </div>

              <div className="flex items-center justify-between mb-3">
                {renderStars(restaurant.rating)}
                <div className="flex items-center text-gray-600">
                  <span className="text-sm">
                    {restaurant.cost ? `Rs.${restaurant.cost}` : 'Price not available'}
                  </span>
                </div>
              </div>

              <div className="flex flex-wrap gap-1 mb-4">
                {restaurant.cuisines.map((cuisine) => (
                  <span
                    key={cuisine}
                    className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700"
                  >
                    {cuisine}
                  </span>
                ))}
              </div>

              {restaurant.budgetBand && (
                <div className="mb-4">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getBudgetColor(restaurant.budgetBand)}`}>
                    {restaurant.budgetBand.charAt(0).toUpperCase() + restaurant.budgetBand.slice(1)} Budget
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Action Button */}
          <div className="pt-4 border-t">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onViewDetails?.(restaurant.id)}
              className="w-full"
            >
              View Restaurant
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
