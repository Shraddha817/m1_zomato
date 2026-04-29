#!/usr/bin/env python3
"""
Backend server startup script for Phase 6 hardened backend
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    try:
        import uvicorn
        from milestone1.phase6_hardening.production import ProductionHardening
        from milestone1.phase6_hardening.config import ProductionConfig
        
        print("Starting Phase 6 Backend Server...")
        print("=" * 50)
        
        # Load configuration
        config = ProductionConfig.from_env()
        print(f"Configuration loaded")
        print(f"   - API URL: {os.environ.get('XAI_BASE_URL', 'https://api.groq.com/openai/v1')}")
        print(f"   - Model: {config.xai_model}")
        print(f"   - Dataset: {config.dataset_name}")
        
        # Initialize production hardening
        print("\nInitializing production hardening...")
        hardening = ProductionHardening(config)
        
        # Setup production environment
        print("Setting up production environment...")
        hardening.setup_production_environment()
        
        # Run health checks
        print("Running health checks...")
        hardening._run_health_checks()
        
        print("\nBackend is ready!")
        print("=" * 50)
        print("Starting FastAPI server on http://localhost:8000")
        print("API Documentation: http://localhost:8000/docs")
        print("Health Check: http://localhost:8000/api/health")
        print("=" * 50)
        
        # Start the server
        uvicorn.run(
            "milestone1.phase6_hardening.app:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"ERROR Import error: {e}")
        print("Please install required packages:")
        print("pip install fastapi uvicorn python-dotenv")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR Failed to start backend: {e}")
        sys.exit(1)
