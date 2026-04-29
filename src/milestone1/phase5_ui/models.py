from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class UIState(Enum):
    """Represents the current state of the UI"""
    INPUT = "input"  # Showing input form
    LOADING = "loading"  # Processing request
    RESULTS = "results"  # Showing recommendations
    ERROR = "error"  # Showing error state
    EMPTY = "empty"  # No results found


@dataclass(frozen=True, slots=True)
class UserInput:
    """Represents user input from the form"""
    location: str
    budget_band: str | None = None
    cuisines: list[str] | None = None
    min_rating: float | None = None
    additional_preferences_text: str | None = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for form processing"""
        return {
            "location": self.location,
            "budget_band": self.budget_band,
            "cuisines": self.cuisines or [],
            "min_rating": self.min_rating,
            "additional_preferences_text": self.additional_preferences_text
        }


@dataclass(frozen=True, slots=True)
class UIError:
    """Represents an error to display to the user"""
    title: str
    message: str
    is_retryable: bool = True


@dataclass(frozen=True, slots=True)
class LoadingInfo:
    """Information about the current loading state"""
    message: str
    step_description: str | None = None
