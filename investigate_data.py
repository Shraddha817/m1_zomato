#!/usr/bin/env python3
"""
Script to investigate the restaurant data to understand available locations and data structure.
"""

import os
import sys
from pathlib import Path
from collections import Counter

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from milestone1.ingestion import load_restaurants


def main():
    print("Investigating Restaurant Data")
    print("=" * 50)
    
    # Load restaurant data
    print("Loading restaurant data...")
    restaurants = load_restaurants(limit=1000)
    print(f"Loaded {len(restaurants)} restaurants")
    print()
    
    # Analyze locations
    locations = [r.location for r in restaurants if r.location]
    location_counts = Counter(locations)
    
    print(f"Found {len(location_counts)} unique locations")
    print("\nTop 20 locations by count:")
    for location, count in location_counts.most_common(20):
        print(f"   {location}: {count}")
    print()
    
    # Look for Bangalore/Bengaluru related locations
    bangalore_locations = [loc for loc in location_counts.keys() 
                          if any(keyword in loc.lower() for keyword in ['bangalore', 'bengaluru', 'bellandur'])]
    
    print("Bangalore-related locations:")
    for loc in sorted(bangalore_locations):
        print(f"   {loc}: {location_counts[loc]}")
    print()
    
    # Check budget distribution
    budget_bands = [r.budget_band for r in restaurants if r.budget_band]
    budget_counts = Counter(budget_bands)
    
    print("Budget band distribution:")
    for band, count in budget_counts.most_common():
        print(f"   {band}: {count}")
    print()
    
    # Check rating distribution
    ratings = [r.rating for r in restaurants if r.rating is not None]
    if ratings:
        print(f"Rating stats: min={min(ratings)}, max={max(ratings)}, avg={sum(ratings)/len(ratings):.2f}")
        
        # Count restaurants with rating >= 4.0
        high_rated = [r for r in ratings if r >= 4.0]
        print(f"Restaurants with rating >= 4.0: {len(high_rated)}/{len(ratings)}")
    print()
    
    # Show some sample restaurants
    print("Sample restaurants:")
    for i, restaurant in enumerate(restaurants[:5], 1):
        print(f"   {i}. {restaurant.name}")
        print(f"      Location: {restaurant.location}")
        print(f"      Rating: {restaurant.rating}")
        print(f"      Cost: {restaurant.cost}")
        print(f"      Budget Band: {restaurant.budget_band}")
        print(f"      Cuisines: {', '.join(restaurant.cuisines)}")
        print()


if __name__ == "__main__":
    main()
