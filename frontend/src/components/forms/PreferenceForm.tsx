import React, { useState } from 'react'
import { Search, Plus, X, Info } from 'lucide-react'
import Input from '@/components/ui/Input'
import Button from '@/components/ui/Button'
import Card from '@/components/ui/Card'
import { UserPreferences } from '@/lib/api'

interface PreferenceFormProps {
  onSubmit: (preferences: UserPreferences) => void
  loading?: boolean
  initialData?: Partial<UserPreferences>
}

export default function PreferenceForm({ onSubmit, loading = false, initialData }: PreferenceFormProps) {
  const [preferences, setPreferences] = useState<UserPreferences>({
    location: initialData?.location || '',
    budgetBand: initialData?.budgetBand || '',
    cuisines: initialData?.cuisines || [],
    minRating: initialData?.minRating || 3.0,
    additionalPreferences: initialData?.additionalPreferences || ''
  })

  const [cuisineInput, setCuisineInput] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})

  const budgetBands = [
    { value: 'low', label: 'Low (≤ Rs.300)', color: 'bg-green-100 text-green-800' },
    { value: 'medium', label: 'Medium (Rs.301-700)', color: 'bg-yellow-100 text-yellow-800' },
    { value: 'high', label: 'High (> Rs.700)', color: 'bg-red-100 text-red-800' }
  ]

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!preferences.location.trim()) {
      newErrors.location = 'Location is required'
    }

    if (preferences.minRating && (preferences.minRating < 1 || preferences.minRating > 5)) {
      newErrors.minRating = 'Rating must be between 1 and 5'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    onSubmit(preferences)
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

  const handleCuisineInputKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleCuisineAdd()
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <div className="p-6">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              🍽️ Tell us your preferences
            </h2>
            <p className="text-gray-600">
              Help us find the perfect restaurants for you by providing your preferences below.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Location Input */}
            <Input
              id="location"
              label="Location *"
              placeholder="e.g., Banashankari, BTM, JP Nagar"
              value={preferences.location}
              onChange={(e) => setPreferences(prev => ({ ...prev, location: e.target.value }))}
              error={errors.location}
              helperText="Enter the area where you'd like to find restaurants"
              required
            />

            {/* Budget Band Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Budget Band
              </label>
              <div className="grid grid-cols-3 gap-2">
                {budgetBands.map(band => (
                  <button
                    key={band.value}
                    type="button"
                    onClick={() => setPreferences(prev => ({ ...prev, budgetBand: band.value }))}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      preferences.budgetBand === band.value
                        ? band.color
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {band.label}
                  </button>
                ))}
              </div>
              <p className="mt-1 text-xs text-gray-500">
                Select your preferred price range
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Rating Slider */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Minimum Rating
                </label>
                <div className="space-y-2">
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-500">1.0</span>
                    <input
                      type="range"
                      min="1"
                      max="5"
                      step="0.5"
                      value={preferences.minRating}
                      onChange={(e) => setPreferences(prev => ({ ...prev, minRating: parseFloat(e.target.value) }))}
                      className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                    <span className="text-sm text-gray-500">5.0</span>
                  </div>
                  <div className="text-center">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                      {preferences.minRating?.toFixed(1)} ⭐
                    </span>
                  </div>
                  {errors.minRating && (
                    <p className="text-sm text-red-600">{errors.minRating}</p>
                  )}
                </div>
              </div>

              {/* Cuisine Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Cuisines
                </label>
                <div className="space-y-2">
                  <div className="flex space-x-2">
                    <div className="flex-1 relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                      <input
                        type="text"
                        value={cuisineInput}
                        onChange={(e) => setCuisineInput(e.target.value)}
                        onKeyPress={handleCuisineInputKeyPress}
                        placeholder="e.g., North Indian, Chinese, Italian"
                        className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <Button
                      type="button"
                      onClick={handleCuisineAdd}
                      disabled={!cuisineInput.trim()}
                      size="sm"
                    >
                      <Plus className="w-4 h-4" />
                    </Button>
                  </div>
                  
                  {/* Cuisine Tags */}
                  {preferences.cuisines && preferences.cuisines.length > 0 && (
                    <div className="flex flex-wrap gap-2">
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
                            <X className="w-3 h-3" />
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
                Additional Preferences
                <span className="ml-1 text-gray-400">
                  <Info className="w-4 h-4 inline" />
                </span>
              </label>
              <textarea
                id="additionalPreferences"
                value={preferences.additionalPreferences}
                onChange={(e) => setPreferences(prev => ({ ...prev, additionalPreferences: e.target.value }))}
                rows={4}
                placeholder="Any specific requirements or preferences... (e.g., outdoor seating, parking, good for families)"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
              <p className="mt-1 text-xs text-gray-500">
                Optional: Tell us more about what you're looking for
              </p>
            </div>

            {/* Submit Button */}
            <div className="pt-6">
              <Button
                type="submit"
                loading={loading}
                disabled={loading || !preferences.location.trim()}
                className="w-full"
                size="lg"
              >
                {loading ? 'Getting Recommendations...' : 'Get Recommendations'}
              </Button>
            </div>
          </form>
        </div>
      </Card>
    </div>
  )
}
