import React from 'react'
import { Star, MapPin, DollarSign, Clock, ChevronRight } from 'lucide-react'
import Card, { CardContent } from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import { Recommendation } from '@/lib/api'

interface RestaurantCardProps {
  recommendation: Recommendation
  onViewDetails?: (restaurant: Recommendation['restaurant']) => void
}

export default function RestaurantCard({ recommendation, onViewDetails }: RestaurantCardProps) {
  const { restaurant, rank, explanation } = recommendation

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
    <Card variant="elevated" className="hover:shadow-xl transition-shadow duration-200">
      <CardContent>
        <div className="flex justify-between items-start mb-4">
          <div className="flex-1">
            <div className="flex items-center mb-2">
              <span className="inline-flex items-center justify-center w-8 h-8 bg-blue-600 text-white rounded-full text-sm font-semibold mr-3">
                {rank}
              </span>
              <h3 className="text-xl font-semibold text-gray-900">{restaurant.name}</h3>
            </div>
            
            <div className="flex items-center text-gray-600 mb-2">
              <MapPin className="w-4 h-4 mr-1" />
              <span className="text-sm">{restaurant.location}</span>
            </div>

            <div className="flex items-center justify-between mb-3">
              {renderStars(restaurant.rating)}
              <div className="flex items-center text-gray-600">
                <DollarSign className="w-4 h-4 mr-1" />
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

        <div className="border-t pt-4">
          <div className="flex items-start mb-3">
            <div className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
            <div>
              <p className="text-sm font-medium text-gray-900 mb-1">AI Recommendation</p>
              <p className="text-sm text-gray-600 leading-relaxed">{explanation}</p>
            </div>
          </div>
        </div>

        {onViewDetails && (
          <div className="mt-4 pt-4 border-t">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onViewDetails(restaurant)}
              className="w-full"
            >
              View Details
              <ChevronRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
