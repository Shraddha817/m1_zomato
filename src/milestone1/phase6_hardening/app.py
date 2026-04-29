"""
FastAPI application for Phase 6 hardened backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_path))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import our existing modules
try:
    from milestone1.ingestion import load_restaurants
    from milestone1.phase2_preferences.models import UserPreferences
    from milestone1.phase3_integration.filtering import filter_candidates
    from milestone1.phase3_integration.prompting import build_prompt_payload
    from milestone1.phase4_recommendation.client import get_recommendations
    from milestone1.phase4_recommendation.models import Recommendation
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback for testing
    Recommendation = None
    UserPreferences = None

# Create FastAPI app
app = FastAPI(
    title="Restaurant Recommendation API",
    description="Phase 6 hardened backend for restaurant recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class UserPreferencesRequest(BaseModel):
    location: str
    budgetBand: Optional[str] = None
    cuisines: Optional[List[str]] = None
    minRating: Optional[float] = None
    additionalPreferences: Optional[str] = None

class RestaurantResponse(BaseModel):
    id: str
    name: str
    location: str
    cuisines: List[str]
    rating: Optional[float] = None
    cost: Optional[float] = None
    budgetBand: Optional[str] = None

class RecommendationResponse(BaseModel):
    restaurant: RestaurantResponse
    rank: int
    explanation: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    api_version: str

# API Routes
@app.get("/")
async def root():
    return {"message": "Restaurant Recommendation API", "version": "1.0.0"}

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        api_version="1.0.0"
    )

@app.get("/api/locations", response_model=List[str])
async def get_locations():
    """Get available locations"""
    try:
        restaurants = load_restaurants(limit=1000)
        locations = list(set(restaurant.location for restaurant in restaurants))
        return sorted(locations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load locations: {str(e)}")

@app.post("/api/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations_endpoint(preferences: UserPreferencesRequest):
    """Get restaurant recommendations based on user preferences"""
    try:
        # Convert API request to internal model
        user_prefs = UserPreferences(
            location=preferences.location,
            budget_band=preferences.budgetBand,
            cuisines=tuple(preferences.cuisines) if preferences.cuisines else (),
            min_rating=preferences.minRating,
            additional_preferences_text=preferences.additionalPreferences
        )
        
        # Load restaurants
        restaurants = load_restaurants(limit=1000)
        
        # Filter candidates
        candidates = filter_candidates(restaurants, user_prefs, limit=25)
        
        if not candidates:
            return []
        
        # Build prompt payload
        prompt_payload = build_prompt_payload(candidates, user_prefs)
        
        # Get recommendations
        recommendations = get_recommendations(prompt_payload, candidates, top_k=5)
        
        # Convert to API response format
        response = []
        for rec in recommendations:
            restaurant_response = RestaurantResponse(
                id=rec.restaurant.id,
                name=rec.restaurant.name,
                location=rec.restaurant.location,
                cuisines=list(rec.restaurant.cuisines),
                rating=rec.restaurant.rating,
                cost=rec.restaurant.cost,
                budgetBand=rec.restaurant.budget_band
            )
            
            recommendation_response = RecommendationResponse(
                restaurant=restaurant_response,
                rank=rec.rank,
                explanation=rec.explanation
            )
            response.append(recommendation_response)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@app.get("/api/restaurants/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant_details(restaurant_id: str):
    """Get detailed information about a specific restaurant"""
    try:
        restaurants = load_restaurants(limit=1000)
        restaurant = next((r for r in restaurants if r.id == restaurant_id), None)
        
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
        return RestaurantResponse(
            id=restaurant.id,
            name=restaurant.name,
            location=restaurant.location,
            cuisines=list(restaurant.cuisines),
            rating=restaurant.rating,
            cost=restaurant.cost,
            budgetBand=restaurant.budgetBand
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get restaurant details: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
