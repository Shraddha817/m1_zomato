'use client'

import React, { useState, useEffect, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import { Search, Filter, Star, Clock, MapPin, User, ShoppingCart, ChevronDown, Heart } from 'lucide-react'

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
      <header style={{ backgroundColor: 'white', borderBottom: '1px solid #e9ecef', boxShadow: '0 2px 4px rgba(0,0,0,0.08)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '80px' }}>
            {/* Logo */}
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#e23744', margin: 0, letterSpacing: '-1px' }}>Zomato</h1>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', flex: 1, maxWidth: '800px', margin: '0 40px' }}>
              {/* Location Selector */}
              <div style={{ display: 'flex', alignItems: 'center', border: '1px solid #dee2e6', borderRadius: '8px', padding: '12px 16px', marginRight: '16px', backgroundColor: 'white', minWidth: '180px' }}>
                <MapPin style={{ width: '18px', height: '18px', color: '#e23744', marginRight: '8px' }} />
                <select 
                  value={selectedLocation}
                  onChange={(e) => setSelectedLocation(e.target.value)}
                  style={{ border: 'none', outline: 'none', fontSize: '15px', fontWeight: '500', background: 'transparent', minWidth: '120px', cursor: 'pointer' }}
                >
                  {locations.map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
                <ChevronDown style={{ width: '16px', height: '16px', color: '#6c757d', marginLeft: '8px' }} />
              </div>

              {/* Search Bar */}
              <div style={{ flex: 1, position: 'relative' }}>
                <Search style={{ position: 'absolute', left: '18px', top: '50%', transform: 'translateY(-50%)', color: '#6c757d', width: '20px', height: '20px' }} />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search for restaurant, cuisine or a dish"
                  style={{
                    width: '100%',
                    paddingLeft: '52px',
                    paddingRight: '16px',
                    padding: '14px 0',
                    border: '1px solid #dee2e6',
                    borderRadius: '8px',
                    fontSize: '15px',
                    outline: 'none',
                    backgroundColor: '#f8f9fa'
                  }}
                />
              </div>
            </div>

            {/* Right Side Actions */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
              <button style={{ display: 'flex', alignItems: 'center', color: '#495057', fontSize: '15px', fontWeight: '500', background: 'none', border: 'none', cursor: 'pointer' }}>
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
          <aside style={{ width: '280px', flexShrink: 0 }}>
            <div style={{ backgroundColor: 'white', borderRadius: '12px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)', padding: '24px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
                <h3 style={{ fontSize: '20px', fontWeight: '600', margin: 0, color: '#212529' }}>Filters</h3>
                <button 
                  onClick={clearFilters}
                  style={{ color: '#e23744', fontSize: '14px', background: 'none', border: 'none', cursor: 'pointer', fontWeight: '500' }}
                >
                  Clear all
                </button>
              </div>

              {/* Cuisines Filter */}
              <div style={{ marginBottom: '32px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#212529' }}>Cuisines</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '240px', overflowY: 'auto' }}>
                  {cuisineOptions.slice(0, 10).map(cuisine => (
                    <label key={cuisine} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '6px 0' }}>
                      <input
                        type="checkbox"
                        style={{ marginRight: '12px', width: '16px', height: '16px', cursor: 'pointer' }}
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
                      <span style={{ fontSize: '14px', color: '#495057' }}>{cuisine}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Rating Filter */}
              <div style={{ marginBottom: '32px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#212529' }}>Rating</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  {[4.0, 3.5, 3.0].map(rating => (
                    <label key={rating} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '6px 0' }}>
                      <input
                        type="radio"
                        name="rating"
                        style={{ marginRight: '12px', width: '16px', height: '16px', cursor: 'pointer' }}
                        checked={selectedFilters.rating === rating.toString()}
                        onChange={() => setSelectedFilters(prev => ({ ...prev, rating: rating.toString() }))}
                      />
                      <div style={{ display: 'flex', alignItems: 'center' }}>
                        <span style={{ fontSize: '14px', marginRight: '10px', color: '#495057' }}>{rating}+</span>
                        <div style={{ display: 'flex' }}>
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              style={{
                                width: '14px',
                                height: '14px',
                                color: i < rating ? '#48c479' : '#e5e7eb'
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
              <div style={{ marginBottom: '32px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#212529' }}>Cost for two</h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  {[
                    { label: 'Less than Rs.300', value: 'low' },
                    { label: 'Rs.300 to Rs.700', value: 'medium' },
                    { label: 'More than Rs.700', value: 'high' }
                  ].map(cost => (
                    <label key={cost.value} style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '6px 0' }}>
                      <input
                        type="radio"
                        name="cost"
                        style={{ marginRight: '12px', width: '16px', height: '16px', cursor: 'pointer' }}
                        checked={selectedFilters.cost === cost.value}
                        onChange={() => setSelectedFilters(prev => ({ ...prev, cost: cost.value }))}
                      />
                      <span style={{ fontSize: '14px', color: '#495057' }}>{cost.label}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Sort Filter */}
              <div style={{ marginBottom: '24px' }}>
                <h4 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#212529' }}>Sort by</h4>
                <select 
                  value={selectedFilters.sort}
                  onChange={(e) => setSelectedFilters(prev => ({ ...prev, sort: e.target.value }))}
                  style={{ 
                    width: '100%', 
                    padding: '12px 16px', 
                    border: '1px solid #dee2e6', 
                    borderRadius: '8px', 
                    fontSize: '14px',
                    backgroundColor: '#f8f9fa',
                    outline: 'none',
                    cursor: 'pointer'
                  }}
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
            <div style={{ marginBottom: '20px' }}>
              <h1 style={{ fontSize: '28px', fontWeight: 'bold', color: '#212529', margin: '0 0 6px 0' }}>
                {selectedFilters.cuisines.length > 0 
                  ? `${selectedFilters.cuisines.join(', ')} restaurants in ${selectedLocation}`
                  : `Best restaurants in ${selectedLocation}`
                }
              </h1>
              <p style={{ color: '#6c757d', margin: 0, fontSize: '15px' }}>
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
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '20px' }}>
                {filteredRestaurants.map((restaurant) => (
                  <div 
                    key={restaurant.id} 
                    style={{ 
                      backgroundColor: 'white', 
                      borderRadius: '8px', 
                      padding: '20px',
                      cursor: 'pointer',
                      transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                      border: '1px solid #e9ecef'
                    }} 
                    onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateY(-2px)'
                      e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.15)'
                    }} 
                    onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateY(0)'
                      e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)'
                    }}
                  >
                    {/* Restaurant Info - Simplified */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                      <div style={{ flex: 1 }}>
                        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#212529', margin: '0 0 6px 0', lineHeight: '1.3' }}>
                          {restaurant.name}
                        </h3>
                        
                        <div style={{ fontSize: '14px', color: '#6c757d', marginBottom: '6px', lineHeight: '1.4' }}>
                          {restaurant.cuisines.join(', ')}
                        </div>
                        
                        <div style={{ fontSize: '14px', color: '#6c757d', display: 'flex', alignItems: 'center' }}>
                          <MapPin style={{ width: '14px', height: '14px', marginRight: '6px' }} />
                          {restaurant.location}
                        </div>
                      </div>
                      
                      <div style={{ textAlign: 'right', marginLeft: '20px' }}>
                        <div style={{
                          backgroundColor: '#48c479',
                          color: 'white',
                          padding: '6px 8px',
                          borderRadius: '6px',
                          fontSize: '14px',
                          fontWeight: '600',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '4px',
                          marginBottom: '8px'
                        }}>
                          <Star style={{ width: '14px', height: '14px', fill: 'currentColor' }} />
                          {restaurant.rating?.toFixed(1) || '4.0'}
                        </div>
                        
                        <div style={{ fontSize: '16px', fontWeight: '600', color: '#212529', lineHeight: '1.2' }}>
                          {formatCurrency(restaurant.cost * 2)}
                        </div>
                        <div style={{ fontSize: '12px', color: '#6c757d' }}>for two</div>
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
                <p style={{ color: '#6c757d', marginBottom: '16px', fontSize: '15px' }}>Try adjusting your filters or search terms</p>
                <button
                  onClick={() => router.push('/preferences')}
                  style={{ 
                    padding: '10px 20px', 
                    backgroundColor: '#e23744', 
                    color: 'white', 
                    borderRadius: '8px', 
                    border: 'none',
                    cursor: 'pointer',
                    fontSize: '15px',
                    fontWeight: '500'
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
