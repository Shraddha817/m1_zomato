import React from 'react'
import { MapPin } from 'lucide-react'

interface PopularLocationsProps {
  onLocationSelect?: (location: string) => void
}

export default function PopularLocations({ onLocationSelect }: PopularLocationsProps) {
  const locations = [
    'Banashankari',
    'BTM Layout', 
    'JP Nagar',
    'Basavanagudi',
    'Koramangala',
    'Indiranagar',
    'HSR Layout',
    'Whitefield'
  ]

  return (
    <div className="bg-gray-50 py-16">
      <div className="container mx-auto px-4">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Popular Locations</h2>
          <p className="text-gray-600">Explore restaurants in these popular areas</p>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
          {locations.map((location) => (
            <button
              key={location}
              onClick={() => onLocationSelect?.(location)}
              className="group relative p-6 bg-white rounded-lg border border-gray-200 hover:border-blue-500 hover:shadow-lg transition-all duration-300 text-left"
            >
              <div className="flex items-center mb-3">
                <MapPin className="w-5 h-5 text-blue-600 mr-2" />
                <span className="font-semibold text-gray-900">{location}</span>
              </div>
              
              <div className="text-sm text-gray-600">
                {Math.floor(Math.random() * 50) + 10} restaurants
              </div>
              
              <div className="absolute inset-0 bg-blue-600 opacity-0 group-hover:opacity-5 transition-opacity duration-300 rounded-lg"></div>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
