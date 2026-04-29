"""
Phase 5 Web Application - Restaurant Recommender
Complete UI implementation for the restaurant recommendation system.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import Phase 5 UI
from milestone1.phase5_ui.app import create_app


def main() -> None:
    """Main entry point for the web application."""
    create_app()


if __name__ == "__main__":
    main()

