'use client'

import React, { useState, useEffect, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import { Search, Filter, Star, Clock, MapPin, User, ShoppingCart, ChevronDown } from 'lucide-react'

interface Restaurant {
  id: string
  name: string
  location: string
  cuisines: string[]
  rating: number | null
  cost: number | null
  budgetBand: string | null
}

export default function HomePage() {
  const router = useRouter()
  const [allRestaurants, setAllRestaurants] = useState<Restaurant[]>([])
  const [locations, setLocations] = useState<string[]>([])
  const [selectedLocation, setSelectedLocation] = useState('Bangalore')
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [selectedFilters, setSelectedFilters] = useState({
    cuisines: [] as string[],
    rating: '',
    cost: '',
    sort: 'Popularity'
  })

  useEffect(() => {
    loadLocations()
    loadRestaurants()
  }, [])

  const loadLocations = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/locations')
      if (response.ok) {
        const data = await response.json()
        setLocations(['Bangalore', ...data])
      }
    } catch (error) {
      console.error('Error loading locations:', error)
    }
  }

  const loadRestaurants = async () => {
    try {
      // Mock data with different locations
      const mockRestaurants = [
        {
          id: '1',
          name: 'The Bengaluru Cafe',
          location: 'Indiranagar',
          cuisines: ['Cafe', 'Continental', 'Italian'],
          rating: 4.5,
          cost: 800,
          budgetBand: 'high'
        },
        {
          id: '2',
          name: 'Spice Garden',
          location: 'Koramangala',
          cuisines: ['North Indian', 'Chinese', 'Mughlai'],
          rating: 4.2,
          cost: 600,
          budgetBand: 'medium'
        },
        {
          id: '3',
          name: 'Pizza Express',
          location: 'BTM Layout',
          cuisines: ['Pizza', 'Italian', 'Fast Food'],
          rating: 4.0,
          cost: 400,
          budgetBand: 'medium'
        },
        {
          id: '4',
          name: 'Sushi Master',
          location: 'Whitefield',
          cuisines: ['Japanese', 'Sushi', 'Asian'],
          rating: 4.7,
          cost: 1200,
          budgetBand: 'high'
        },
        {
          id: '5',
          name: 'Biryani House',
          location: 'Jayanagar',
          cuisines: ['Biryani', 'Mughlai', 'North Indian'],
          rating: 4.3,
          cost: 350,
          budgetBand: 'low'
        },
        {
          id: '6',
          name: 'Green Garden',
          location: 'HSR Layout',
          cuisines: ['Healthy Food', 'Salads', 'Continental'],
          rating: 4.1,
          cost: 500,
          budgetBand: 'medium'
        },
        {
          id: '7',
          name: 'JP Nagar Special',
          location: 'JP Nagar',
          cuisines: ['South Indian', 'Chinese', 'Fast Food'],
          rating: 3.8,
          cost: 300,
          budgetBand: 'low'
        },
        {
          id: '8',
          name: 'Banashankari Bites',
          location: 'Banashankari',
          cuisines: ['North Indian', 'South Indian', 'Chinese'],
          rating: 4.1,
          cost: 450,
          budgetBand: 'medium'
        },
        {
          id: '9',
          name: 'Marathahalli Meals',
          location: 'Marathahalli',
          cuisines: ['Biryani', 'Mughlai', 'Arabian'],
          rating: 4.4,
          cost: 550,
          budgetBand: 'medium'
        },
        {
          id: '10',
          name: 'Electronic City Eats',
          location: 'Electronic City',
          cuisines: ['Fast Food', 'Chinese', 'Continental'],
          rating: 3.9,
          cost: 380,
          budgetBand: 'low'
        }
      ]
      setAllRestaurants(mockRestaurants)
    } catch (error) {
      console.error('Error loading restaurants:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Filter and sort restaurants based on selected filters
  const filteredRestaurants = useMemo(() => {
    let filtered = [...allRestaurants]

    // Filter by location
    if (selectedLocation !== 'Bangalore') {
      filtered = filtered.filter(r => r.location === selectedLocation)
    }

    // Filter by cuisines
    if (selectedFilters.cuisines.length > 0) {
      filtered = filtered.filter(r => 
        selectedFilters.cuisines.some(cuisine => 
          r.cuisines.some(rc => rc.toLowerCase().includes(cuisine.toLowerCase()))
        )
      )
    }

    // Filter by rating
    if (selectedFilters.rating) {
      const minRating = parseFloat(selectedFilters.rating)
      filtered = filtered.filter(r => r.rating && r.rating >= minRating)
    }

    // Filter by cost
    if (selectedFilters.cost) {
      filtered = filtered.filter(r => r.budgetBand === selectedFilters.cost)
    }

    // Sort restaurants
    switch (selectedFilters.sort) {
      case 'Rating':
        filtered.sort((a, b) => (b.rating || 0) - (a.rating || 0))
        break
      case 'CostLow':
        filtered.sort((a, b) => (a.cost || 0) - (b.cost || 0))
        break
      case 'CostHigh':
        filtered.sort((a, b) => (b.cost || 0) - (a.cost || 0))
        break
      case 'Delivery':
        // Random delivery time for demo
        filtered.sort(() => Math.random() - 0.5)
        break
      default: // Popularity
        filtered.sort(() => Math.random() - 0.5)
    }

    return filtered
  }, [allRestaurants, selectedLocation, selectedFilters])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      router.push(`/preferences?location=${encodeURIComponent(searchQuery.trim())}`)
    }
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
    }).format(amount)
  }

  const renderStars = (rating: number | null) => {
    if (!rating) return <span className="text-gray-400">No rating</span>
    
    const fullStars = Math.floor(rating)
    const hasHalfStar = rating % 1 >= 0.5
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0)
    
    return (
      <div className="flex items-center">
        {[...Array(fullStars)].map((_, i) => (
          <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
        ))}
        {hasHalfStar && <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />}
        {[...Array(emptyStars)].map((_, i) => (
          <Star key={i} className="w-4 h-4 text-gray-300" />
        ))}
        <span className="ml-1 text-sm text-gray-600">{rating.toFixed(1)}</span>
      </div>
    )
  }

  const cuisineOptions = [
    'American', 'Andhra', 'Arabian', 'Asian', 'BBQ', 'Bakery', 'Bengali', 'Beverages',
    'Biryani', 'Burger', 'Cafe', 'Chinese', 'Continental', 'Desserts', 'European',
    'Fast Food', 'Goan', 'Gujarati', 'Healthy Food', 'Ice Cream', 'Indonesian',
    'Italian', 'Japanese', 'Juices', 'Kerala', 'Korean', 'Lebanese', 'Maharashtrian',
    'Malaysian', 'Mediterranean', 'Mexican', 'Mithai', 'Mughlai', 'North Indian',
    'Pakistani', 'Pizza', 'Rajasthani', 'Salad', 'Sandwich', 'Seafood', 'South Indian',
    'Spanish', 'Street Food', 'Sushi', 'Tamil', 'Thai', 'Tibetan', 'Wraps'
  ]

  const clearFilters = () => {
    setSelectedFilters({
      cuisines: [],
      rating: '',
      cost: '',
      sort: 'Popularity'
    })
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      {/* Header */}
      <header style={{ backgroundColor: 'white', borderBottom: '1px solid #e9ecef', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '64px' }}>
            {/* Logo */}
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <h1 style={{ fontSize: '24px', fontWeight: 'bold', color: '#e23744', margin: 0 }}>FoodieFind</h1>
            </div>

            {/* Location Selector */}
            <div style={{ display: 'flex', alignItems: 'center', border: '1px solid #dee2e6', borderRadius: '8px', padding: '8px 12px' }}>
              <MapPin style={{ width: '16px', height: '16px', color: '#e23744', marginRight: '8px' }} />
              <select 
                value={selectedLocation}
                onChange={(e) => setSelectedLocation(e.target.value)}
                style={{ border: 'none', outline: 'none', fontSize: '14px', fontWeight: '500', background: 'transparent' }}
              >
                {locations.map(location => (
                  <option key={location} value={location}>{location}</option>
                ))}
              </select>
              <ChevronDown style={{ width: '16px', height: '16px', color: '#6c757d', marginLeft: '8px' }} />
            </div>

            {/* Search Bar */}
            <div style={{ flex: 1, maxWidth: '480px', margin: '0 32px' }}>
              <div style={{ position: 'relative' }}>
                <Search style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: '#6c757d', width: '20px', height: '20px' }} />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search for restaurant, cuisine or a dish"
                  style={{
                    width: '100%',
                    paddingLeft: '44px',
                    paddingRight: '16px',
                    padding: '8px 0',
                    border: '1px solid #dee2e6',
                    borderRadius: '8px',
                    fontSize: '14px',
                    outline: 'none'
                  }}
                />
              </div>
            </div>

            {/* Right Side Actions */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <button style={{ display: 'flex', alignItems: 'center', color: '#495057', fontSize: '14px', fontWeight: '500', background: 'none', border: 'none', cursor: 'pointer' }}>
                <span style={{ marginRight: '4px' }}>Log in</span>
                <span style={{ color: '#6c757d' }}>/</span>
                <span style={{ marginLeft: '4px' }}>Sign up</span>
              </button>
              <button style={{ position: 'relative', background: 'none', border: 'none', cursor: 'pointer' }}>
                <ShoppingCart style={{ width: '24px', height: '24px', color: '#495057' }} />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px 20px' }}>
        <div style={{ display: 'flex', gap: '24px' }}>
          {/* Sidebar Filters */}
          <aside style={{ width: '256px', flexShrink: 0 }}>
            <div style={{ backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                <h3 style={{ fontSize: '18px', fontWeight: '600', margin: 0 }}>Filters</h3>
                <button 
                  onClick={clearFilters}
                  style={{ color: '#e23744', fontSize: '14px', background: 'none', border: 'none', cursor: 'pointer' }}
                >
                  Clear all
                </button>
              </div>

              {/* Cuisines Filter */}
              <div style={{ marginBottom: '24px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: '500', marginBottom: '12px' }}>Cuisines</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '192px', overflowY: 'auto' }}>
                  {cuisineOptions.slice(0, 10).map(cuisine => (
                    <label key={cuisine} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                      <input
                        type="checkbox"
                        style={{ marginRight: '8px' }}
                        checked={selectedFilters.cuisines.includes(cuisine)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setSelectedFilters(prev => ({
                              ...prev,
                              cuisines: [...prev.cuisines, cuisine]
                            }))
                          } else {
                            setSelectedFilters(prev => ({
                              ...prev,
                              cuisines: prev.cuisines.filter(c => c !== cuisine)
                            }))
                          }
                        }}
                      />
                      <span style={{ fontSize: '14px' }}>{cuisine}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Rating Filter */}
              <div style={{ marginBottom: '24px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: '500', marginBottom: '12px' }}>Rating</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {[4.0, 3.5, 3.0].map(rating => (
                    <label key={rating} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                      <input
                        type="radio"
                        name="rating"
                        style={{ marginRight: '8px' }}
                        checked={selectedFilters.rating === rating.toString()}
                        onChange={() => setSelectedFilters(prev => ({ ...prev, rating: rating.toString() }))}
                      />
                      <div style={{ display: 'flex', alignItems: 'center' }}>
                        <span style={{ fontSize: '14px', marginRight: '8px' }}>{rating}+</span>
                        <div style={{ display: 'flex' }}>
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              style={{
                                width: '12px',
                                height: '12px',
                                color: i < rating ? '#fbbf24' : '#d1d5db'
                              }}
                              fill={i < rating ? 'currentColor' : 'none'}
                            />
                          ))}
                        </div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              {/* Cost Filter */}
              <div style={{ marginBottom: '24px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: '500', marginBottom: '12px' }}>Cost for two</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {[
                    { label: 'Less than Rs.300', value: 'low' },
                    { label: 'Rs.300 to Rs.700', value: 'medium' },
                    { label: 'More than Rs.700', value: 'high' }
                  ].map(cost => (
                    <label key={cost.value} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                      <input
                        type="radio"
                        name="cost"
                        style={{ marginRight: '8px' }}
                        checked={selectedFilters.cost === cost.value}
                        onChange={() => setSelectedFilters(prev => ({ ...prev, cost: cost.value }))}
                      />
                      <span style={{ fontSize: '14px' }}>{cost.label}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Sort Filter */}
              <div style={{ marginBottom: '24px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: '500', marginBottom: '12px' }}>Sort by</h4>
                <select 
                  value={selectedFilters.sort}
                  onChange={(e) => setSelectedFilters(prev => ({ ...prev, sort: e.target.value }))}
                  style={{ width: '100%', padding: '8px', border: '1px solid #dee2e6', borderRadius: '4px', fontSize: '14px' }}
                >
                  <option value="Popularity">Popularity high to low</option>
                  <option value="Rating">Rating high to low</option>
                  <option value="CostLow">Cost low to high</option>
                  <option value="CostHigh">Cost high to low</option>
                  <option value="Delivery">Delivery time</option>
                </select>
              </div>
            </div>
          </aside>

          {/* Restaurant Grid */}
          <main style={{ flex: 1 }}>
            {/* Results Header */}
            <div style={{ marginBottom: '16px' }}>
              <h1 style={{ fontSize: '24px', fontWeight: 'bold', color: '#212529', margin: '0 0 4px 0' }}>
                {selectedFilters.cuisines.length > 0 
                  ? `${selectedFilters.cuisines.join(', ')} restaurants in ${selectedLocation}`
                  : `Best restaurants in ${selectedLocation}`
                }
              </h1>
              <p style={{ color: '#6c757d', margin: 0, fontSize: '14px' }}>
                {filteredRestaurants.length} restaurants
              </p>
            </div>

            {/* Restaurant Cards */}
            {isLoading ? (
              <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '48px 0' }}>
                <div style={{ 
                  width: '32px', 
                  height: '32px', 
                  border: '3px solid #f3f3f3',
                  borderTop: '3px solid #e23744',
                  borderRadius: '50%',
                  animation: 'spin 1s linear infinite'
                }}></div>
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '16px' }}>
                {filteredRestaurants.map((restaurant) => (
                  <div key={restaurant.id} style={{ 
                    backgroundColor: 'white', 
                    borderRadius: '8px', 
                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                    overflow: 'hidden',
                    cursor: 'pointer',
                    transition: 'box-shadow 0.2s ease'
                  }} onMouseEnter={(e) => e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)'} onMouseLeave={(e) => e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)'}>
                    {/* Restaurant Image */}
                    <div style={{ position: 'relative', height: '192px', backgroundColor: '#f8f9fa', overflow: 'hidden' }}>
                      <img
                        src={`https://picsum.photos/seed/${restaurant.id}/400/300.jpg`}
                        alt={restaurant.name}
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                      />
                      {/* Promoted Badge */}
                      <div style={{ 
                        position: 'absolute', 
                        top: '8px', 
                        left: '8px', 
                        backgroundColor: '#16a34a', 
                        color: 'white', 
                        padding: '4px 8px', 
                        borderRadius: '4px', 
                        fontSize: '12px', 
                        fontWeight: '500' 
                      }}>
                        Promoted
                      </div>
                      {/* Quick Actions */}
                      <div style={{ position: 'absolute', top: '8px', right: '8px', display: 'flex', gap: '8px' }}>
                        <button style={{ 
                          backgroundColor: 'white', 
                          borderRadius: '50%', 
                          padding: '8px', 
                          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                          border: 'none',
                          cursor: 'pointer'
                        }}>
                          <svg style={{ width: '16px', height: '16px' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                          </svg>
                        </button>
                      </div>
                    </div>
                    
                    {/* Restaurant Info */}
                    <div style={{ padding: '16px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                        <h3 style={{ fontSize: '16px', fontWeight: '600', color: '#212529', margin: 0 }}>{restaurant.name}</h3>
                        <button style={{ color: '#6c757d', background: 'none', border: 'none', cursor: 'pointer' }}>
                          <svg style={{ width: '20px', height: '20px' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                          </svg>
                        </button>
                      </div>
                      
                      <div style={{ fontSize: '14px', color: '#6c757d', marginBottom: '8px' }}>
                        {restaurant.cuisines.join(', ')}
                      </div>
                      
                      <div style={{ fontSize: '14px', color: '#6c757d', marginBottom: '8px' }}>
                        {restaurant.location}
                      </div>
                      
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div style={{ display: 'flex', alignItems: 'center' }}>
                          {renderStars(restaurant.rating)}
                          <span style={{ marginLeft: '8px', fontSize: '14px', color: '#6c757d' }}>
                            ({Math.floor(Math.random() * 1000) + 100} ratings)
                          </span>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                          <div style={{ fontSize: '16px', fontWeight: '600', color: '#212529' }}>
                            {formatCurrency(restaurant.cost * 2)}
                          </div>
                          <div style={{ fontSize: '12px', color: '#6c757d' }}>Cost for two</div>
                        </div>
                      </div>

                      {/* Delivery Info */}
                      <div style={{ 
                        marginTop: '12px', 
                        paddingTop: '12px', 
                        borderTop: '1px solid #e9ecef', 
                        display: 'flex', 
                        alignItems: 'center', 
                        justifyContent: 'space-between', 
                        fontSize: '14px' 
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', color: '#6c757d' }}>
                          <Clock style={{ width: '16px', height: '16px', marginRight: '4px' }} />
                          <span>20-30 min</span>
                        </div>
                        <div style={{ color: '#6c757d' }}>
                          Free Delivery
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* No Results */}
            {!isLoading && filteredRestaurants.length === 0 && (
              <div style={{ textAlign: 'center', padding: '48px 0' }}>
                <div style={{ color: '#6c757d', marginBottom: '16px' }}>
                  <svg style={{ width: '48px', height: '48px', margin: '0 auto' }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 style={{ fontSize: '18px', fontWeight: '500', color: '#212529', marginBottom: '8px' }}>No restaurants found</h3>
                <p style={{ color: '#6c757d', marginBottom: '16px' }}>Try adjusting your filters or search terms</p>
                <button
                  onClick={() => router.push('/preferences')}
                  style={{ 
                    padding: '8px 16px', 
                    backgroundColor: '#e23744', 
                    color: 'white', 
                    borderRadius: '6px', 
                    border: 'none',
                    cursor: 'pointer',
                    fontSize: '14px'
                  }}
                >
                  Get Personalized Recommendations
                </button>
              </div>
            )}
          </main>
        </div>
      </div>

      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}
